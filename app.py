from flask import Flask, request, render_template
import requests

app = Flask(__name__)

data = []

for search in ["Long Island Tea", "Negroni", "Dry Martini", "Margarita"]:
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}')
    json_response = response.json()

    data.append(json_response["drinks"][0])

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/results', methods=['GET', 'POST'])
def results():

    search = None
    if request.method == 'GET':
        search = request.args.get('search')

    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}')

    return render_template('results.html', search=search, response=response.json())

@app.route('/drink/<name>')
def drink(name):

    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}')

    ingredients = [f"strIngredient{i}" for i in range(1, 16)]
    measures = [f"strMeasure{i}" for i in range(1, 16)]

    return render_template('drink.html', response=response.json()['drinks'][0], ingredients=ingredients, measures=measures)

if __name__ == '__main__':
    app.run()
