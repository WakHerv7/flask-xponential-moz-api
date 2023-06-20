from flask import render_template, request, jsonify, redirect, Response
from app import app, db
from app.models import Entry
import requests
from flask_cors import CORS, cross_origin
CORS(app)

jedi = "of the jedi"

# @cross_origin()

#-------------------------------------
# TOP PAGES
#-------------------------------------
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

    if target:
        response = requests.post(url, data=data, auth=auth)
        return Response(response)


#-------------------------------------
# LINKS
#-------------------------------------
@app.route("/moz/links", methods=['POST'])
def moz_links():
    target = request.get_json()['target']
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/links"
    data = """{
            "target": "%s",
            "target_scope": "page",
            "filter": "external+nofollow",
            "limit": 5
    }"""%(target)
    if target:
        response = requests.post(url, data=data, auth=auth)
        return Response(response)


#-------------------------------------
# GLOBAL TOP PAGES
#-------------------------------------
@app.route("/moz/global_top_pages", methods=['POST'])
def moz_global_top_pages():
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/global_top_pages"
    data = """{
            "limit": 5
    }"""
    response = requests.post(url, data=data, auth=auth)
    return Response(response)
    

#-------------------------------------
# GLOBAL TOP ROOT DOMAINS
#-------------------------------------
@app.route("/moz/global_top_root_domains", methods=['POST'])
def moz_global_top_root_domains():
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/global_top_root_domains"
    data = """{
            "limit": 5
    }"""
    response = requests.post(url, data=data, auth=auth)
    return Response(response)


#-------------------------------------
# INDEX METADATA
#-------------------------------------
@app.route("/moz/index_metadata", methods=['POST'])
def moz_index_metadata():
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/index_metadata"
    data = "{}"
    response = requests.post(url, data=data, auth=auth)
    return Response(response)


#-------------------------------------
# LINK INTERSECT
#-------------------------------------
@app.route("/moz/link_intersect", methods=['POST'])
def moz_link_intersect():
    # positive_targets = [
    #     {"target": "latimes.com", "scope": "root_domain"},
    #     {"target": "blog.nytimes.com", "scope": "subdomain"}
    # ]
    positive_targets = request.get_json()['positive_targets']    
    positive_targets_text = '[]'
    i=0
    for pt in positive_targets:        
        pt = str(pt).replace('\'', '"')
        pt_text = pt+',' if i==0 else pt        
        positive_targets_text = positive_targets_text[:-1] + pt_text + positive_targets_text[-1:]
        i+=1
    
    negative_targets = request.get_json()['negative_targets']    
    negative_targets_text = '[]'
    i=0
    for nt in negative_targets:        
        nt = str(nt).replace('\'', '"')
        nt_text = nt+',' if i==0 else nt        
        negative_targets_text = negative_targets_text[:-1] + nt_text + negative_targets_text[-1:]
        i+=1
    

    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/link_intersect"
    data = """{
        "positive_targets": %s,
        "negative_targets": %s,
        "source_scope": "page",
        "sort": "source_domain_authority",
        "limit": 1
    }"""%(positive_targets_text, negative_targets_text)
    
    if positive_targets and negative_targets:
        response = requests.post(url, data=data, auth=auth)
        return Response(response)
    

#-------------------------------------
# LINK STATUS
#-------------------------------------
@app.route("/moz/link_status", methods=['POST'])
def moz_link_status():
    target = request.get_json()['target']
    sources = request.get_json()['sources']
    sources = '", "'.join(sources)
    sources_text = '[""]'
    sources_text = sources_text[:2] + sources + sources_text[2:]
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/link_status"
    data = """{
            "target": "%s",
            "sources": %s,
            "source_scope": "root_domain",
            "target_scope": "page"
    }"""%(target, sources_text)
    
    if target and sources:
        response = requests.post(url, data=data, auth=auth)
        return Response(response)


#-------------------------------------
# LINKIMG ROOT DOMAINS
#-------------------------------------
@app.route("/moz/linking_root_domains", methods=['POST'])
def moz_linking_root_domains():
    target = request.get_json()['target']
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/linking_root_domains"
    data = """{
            "target": "%s",
            "target_scope": "page",
            "filter": “external",
            "sort": "source_domain_authority",
            "limit": 5
    }"""%(target)
    
    if target:
        response = requests.post(url, data=data, auth=auth)
        return Response(response)


#-------------------------------------
# URL METRICS
#-------------------------------------
@app.route("/moz/url_metrics", methods=['POST'])
def moz_url_metrics():
    target = request.get_json()['target']
    target = '", "'.join(target)
    target_text = '[""]'
    target_text = target_text[:2] + target + target_text[2:]
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/url_metrics"
    data = """{
            "targets": %s
    }"""%(target_text)
    
    if target:
        response = requests.post(url, data=data, auth=auth)
        return Response(response)


#-------------------------------------
# USAGE DATA
#-------------------------------------
@app.route("/moz/usage_data", methods=['POST'])
def moz_usage_data():
    auth = ("mozscape-a72397d745", "b49c556e5f8d6168271989d1f81b3de7")
    url = "https://lsapi.seomoz.com/v2/usage_data"
    data = """{
        "start": "0",
        "end": "1635466367"
    }"""
    response = requests.post(url, data=data, auth=auth)
    return Response(response)



#==========================================
#==========================================



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