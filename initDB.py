import os, sys
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class RecIng(Base):
    __tablename__ = 'rec_ing'
    id = Column(Integer, primary_key=True)
    rec_id = Column(Integer, ForeignKey('recipes.id'))
    ing_id = Column(Integer, ForeignKey('ingredients.id'))
    amount = Column(Integer)
    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship('Ingredient', back_populates='recipes')

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    ingredients = relationship("RecIng", back_populates="recipe")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    recipes = relationship("RecIng", back_populates='ingredient')

class MealPlanItem(Base):
    __tablename__ = 'mealplan'
    id = Column(Integer, primary_key=True)
    rec_id = Column(Integer, ForeignKey('recipes.id'))
    amount = Column(Integer)
    recipe = relationship('Recipe')

class ShoppingListItem(Base):
    __tablename__ = 'shoppinglist'
    id = Column(Integer, primary_key=True)
    ing_id = Column(Integer, ForeignKey('ingredients.id'))
    amount = Column(Integer)
    ingredient = relationship('Ingredient')

class Inventory(Base):
    __tablename__ = 'inventory'
    ing_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    amount = Column(Integer)
    ingredient = relationship('Ingredient')

class InventoryTransactionHistory(Base):
    __tablename__ = 'inv_transactions'
    ing_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    added_or_subtracted = Column(Boolean, unique=False) 
    # added = True, subtracted = False
    # probably needs amounts too

engine = create_engine('sqlite:///pbdb.db')

Base.metadata.create_all(engine)