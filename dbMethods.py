from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from initDB import Recipe, Ingredient, RecIng, MealPlanItem, ShoppingListItem, Inventory, InventoryTransactionHistory, Base

engine = create_engine('sqlite:///pbdb.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# Misc

def get_or_create(session, model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except NoResultFound:
        return model(**kwargs), False

# CRUD Methods

# Create
def addRecipe(recipeName):
    session = DBSession()
    rec, exists = get_or_create(session, Recipe, name=recipeName.lower())
    if exists != True:
        try:
            session.add(rec)
            session.commit()
            print("Insert success")
        except Exception as e:
            session.rollback()
            print("Insert failed")
            print(e)
        finally:
            session.close()
    else:
        print("Recipe already exists.")
        return "Recipe already exists."
        session.close()

def addIngredient(ingredientName):
    session = DBSession()
    ing, exists = get_or_create(session, Ingredient, name=ingredientName.lower())
    if exists != True:
        try:
            session.add(ing)
            session.commit()
            print("Insert success")
        except Exception as e:
            session.rollback()
            print("Insert failed")
            print(e)
        finally:
            session.close()
    else:
        print("Ingredient already exists.")
        return "Ingredient already exists."
        session.close()

def addRecIng(recipe, ingredient, amount):
    # adds entry to rec_ing table
    # if the recipe, ingredient, and/or rec-ing association do not already exists,
    # these are created and added to the appropriate table

    session = DBSession()
    rec, recExists = get_or_create(session, Recipe, name=recipe.lower())
    ing, ingExists = get_or_create(session, Ingredient, name=ingredient.lower())

    if recExists != True: #adds and commits recipe if it does not exists
        session.add(rec) 
        session.commit()

    if ingExists != True: #adds and commits ingredient if it does not exists
        session.add(ing)
        session.commit()

    # gets pre-existing rec_ing entry or creates one
    assoc_table_entry, recIngExists = get_or_create(session, RecIng, rec_id=rec.id, ing_id=ing.id)
    if recIngExists != True: # commits if it does not exist
        assoc_table_entry.ingredient = ing
        assoc_table_entry.amount = amount
        rec.ingredients.append(assoc_table_entry)
        try:
            session.add(assoc_table_entry)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
    else: # updates amount in rec_ing if it already exists in table
        try:
            assoc_table_entry.amount += amount
            session.add(assoc_table_entry)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

def addRecToPlan(recipe):
    # adds recipe to mealplan table
    # if recipe already in table, increases amount of rec by 1

    session = DBSession()
    rec, exists = get_or_create(session, Recipe, name=recipe.lower())
    plan_item, exists2 = get_or_create(session, MealPlanItem, rec_id=rec.id, recipe=rec)
    if exists2 != True:
        plan_item.amount = 1
    else:
        plan_item.amount += 1

    try: 
        session.add(plan_item)
        session.commit()
        print("Recipe added to meal plan")
    except:
        session.rollback()
        print("Recipe not added to meal plan")
    finally:
        session.close()

def addPlanToList():
    # adds ingredients for all recipes in mealplan to shoppinglist

    session = DBSession()

    # query for MealPlanItem, RecIng, & Ingredient tables
    # pulls the RecIng & Ingredient records matching MealPlan rec id
    q = session.query(MealPlanItem, RecIng, Ingredient).filter(MealPlanItem.rec_id == RecIng.rec_id).filter(Ingredient.id == RecIng.ing_id)
    
    for meal, ri, ing in q:
        print("recipe id: " + str(meal.rec_id), "amount: " + str(meal.amount), "ing id:" + str(ing.id))
        list_item, itemExists = get_or_create(session, ShoppingListItem, ing_id=ing.id, ingredient=ing)
        if itemExists != True: # if item not already on shopping list, add it
            try:
                print("item not in list, added")
                list_item.amount = ri.amount * meal.amount # list amount = # in recipe * # of recipes in meal plan
                session.add(list_item)
                session.commit()
            except:
                print("unable to add item to list")
                session.rollback()
        else:
            try: # if item already in shopping list, update amount
                print("item in list, amount updated")
                list_item.amount += ri.amount * meal.amount # note: will need to subtract anything in inventory
                session.add(list_item)
                session.commit()
            except:
                print("unable to update amount of pre-existing shopping list item")
                session.rollback()
                
    session.close()

def addListToInventory():
    # adds ingredients from shopping list to inventory
    # useful after going on a shopping trip
    session = DBSession()
    shoppinglist = session.query(ShoppingListItem)
    for item in shoppinglist:
        print("get or create {}".format(item.ingredient.name))
        inv_item, exists = get_or_create(session, Inventory, ing_id=item.ing_id, ingredient=item.ingredient)
        if exists != True:
            try:
                print("does not exist, creating...")
                inv_item.amount = item.amount
                session.add(inv_item)
                session.commit()
            except:
                session.rollback()
        else:
            try:
                print("exists in inv, updating amount...")
                inv_item.amount += item.amount
                session.add(inv_item)
                session.commit()
            except:
                session.rollback()
    session.close()

# def addIngToInventory(ingredient):
    # needs to add to both Inventory and InventoryTransationHistory

# def addIngToInventory2(ingredient):
    # adds to Inventory, but not InventoryTransationHistory


# addRecIng("pizza", "cheese", 3)
# addRecIng("pizza", "tomato sauce", 1)

# addRecToPlan("pizza")

# addPlanToList()

# Read

def view_all_ingredients():
    # returns array of all ingredients in ingredients table
    session = DBSession()
    q = session.query(Ingredient)
    ings = []
    for ing in q:
        ings += ing.name
        print(ing.name)
    return ings
    session.close()

def view_all_recipes():
    # returns array of all ingredients in ingredients table
    session = DBSession()
    q = session.query(Recipe)
    recs = []
    for rec in q:
        recs += rec.name
        print(rec.name)
    return recs
    session.close()

def view_recipe_ingredients(rec_name=None, rec_id=None):
    # returns all ingredients from RecIng associated with recipe
    # accepts recipe as string or by id
    session = DBSession()
    if rec_name != None:
        q = session.query(RecIng, Recipe, Ingredient).filter(Recipe.name == rec_name).filter(Recipe.id == RecIng.rec_id).filter(Ingredient.id == RecIng.ing_id)
    elif rec_id != None:
        q = session.query(RecIng, Recipe, Ingredient).filter(Recipe.id == rec_id).filter(Recipe.id == RecIng.rec_id).filter(Ingredient.id == RecIng.ing_id)
    else:
        return None

    for x in q:
        print(x[2].name)

    session.close()

def view_mealplan():
    session = DBSession()
    q = session.query(MealPlanItem)
    meals = {}
    for meal in q:
        meals[meal.rec_id] = {"name": meal.recipe.name, "amount": meal.amount}
        print(meals)
    return meals
    session.close()

def view_shoppinglist():
    session = DBSession()
    q = session.query(ShoppingListItem)
    ingredients = {}
    for item in q:
        ingredients[item.ing_id] = {"name": item.ingredient.name, "amount": item.amount}
    return ingredients
    session.close()

def view_inventory():
    session = DBSession()
    q = session.query(Inventory)
    inv_items = {}
    for item in q:
        inv_items[item.ing_id] = {"name": item.ingredient.name, "amount": item.amount}
    print(inv_items)
    return inv_items
    session.close()

addListToInventory()


# Update

# def change_recipe_name(recipeName, newRecipeName):

# def change_recIng_amount(recipe, ingredient, newAmount):

# def use_inv_item():
    # deletes from inventory, but also adds inv transation



# Delete

# def del_recipe(recipe):

# def del_ingredient(ingredient):

# def del_recIng(recipe, ingredient):

# def del_ing_from_shoppinglist(ingredient):

# def del_rec_from_mealplan(rec):

# def del_ing_from_inv(ing):
    # does not keep transaction history of deletion; use in case of inv discrepancies

# def clear_shoppinglist():

# def clear_mealplan():

