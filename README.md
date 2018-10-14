# PantryButler
A general purpose kitchen app. You are able to:
- Save recipes and ingredients
- Add recipes to a meal plan
- Get a shopping list based off of your planned meals
- Keep an inventory of food in your kitchen
- Eventually will track food waste and trends in food consumption

PantryButler uses Flask & SQLite for the backend with SQLAlchemy handling the queries, and will probably use jQuery on the frontend.

- app.py is where the Flask routes are stored.
- initDB.py is used to initially create the DB's tables
- dbMethods.py contains the CRUD methods that will be used to interact with the database

