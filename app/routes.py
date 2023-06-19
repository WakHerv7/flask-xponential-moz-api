from flask import render_template, request, jsonify, redirect, Response
from app import app, db
from app.models import Entry
import requests
from flask_cors import CORS, cross_origin
CORS(app)

jedi = "of the jedi"

# @cross_origin()

@app.route("/moz/top_pages", methods=['POST'])
def moz_top_pages():
    target = request.get_json()['target']
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/top_pages"
    data = """{
        "target": "%s",
        "scope": "root_domain",
        "limit": 5
    }"""%(target)

    response = requests.post(url, data=data, auth=auth)
    return Response(response)

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, data=data, auth=aiohttp.BasicAuth("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")) as resp:
    #         response = await resp.text()
    #         return response
        

@app.route('/')
@app.route('/index')
def index():
    # entries = [
    #     {
    #         'id' : 1,
    #         'title': 'test title 1',
    #         'description' : 'test desc 1',
    #         'status' : True
    #     },
    #     {
    #         'id': 2,
    #         'title': 'test title 2',
    #         'description': 'test desc 2',
    #         'status': False
    #     }
    # ]
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entry(title = title, description = description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

    return "of the jedi"

@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            form = request.form
            title = form.get('title')
            description = form.get('description')
            entry.title = title
            entry.description = description
            db.session.commit()
        return redirect('/')

    return "of the jedi"



@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')

    return "of the jedi"

@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/')

    return "of the jedi"

# @app.errorhandler(Exception)
# def error_page(e):
#     return "of the jedi"