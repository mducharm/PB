from flask import Flask, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from initDB import Recipe, Ingredient, RecIng, MealPlanItem, ShoppingListItem, Inventory, InventoryTransactionHistory, Base
from dbMethods import *

app = Flask(__name__)

engine = create_engine('sqlite:///pbdb.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template("index.html", title="PantryButler")

@app.route('/recipes-ingredients/', methods=['POST'])
def recIngs():
    session = DBSession()
    # if request.method == 'POST':
    #     data = request.form['data']
    #     if data:
    #         addRecipe(data)
    try:
        recipes = session.query(Recipe)
        ingredients = session.query(Ingredient)
        recIngs = session.query(RecIng)
    except Exception as e:
        print(e)
    finally:
        session.close()
        return render_template("rec-ing.html", title="Recipes & Ingredients", recipes=recipes, ingredients=ingredients)
    

if __name__ == '__main__':
    app.run(debug=True)