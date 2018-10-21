from flask import Flask, render_template, request, url_for
from dbMethods import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", title="PantryButler")

@app.route('/recipes-ingredients/', methods=['POST'])
def recIngs():
    data = request.form['data']
    print(data)
    return render_template("rec-ing.html", title="Recipes & Ingredients")

if __name__ == '__main__':
    app.run(debug=True)