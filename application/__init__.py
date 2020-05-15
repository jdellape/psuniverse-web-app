from flask import Flask, render_template, request, json
from neo4j import GraphDatabase

app = Flask(__name__)

#Connect to my clouse hosted database on GrapheneDB
graph = GraphDatabase.driver(uri='bolt://hobby-fflpdbfdfleigbkekoccebel.dbs.graphenedb.com:24787',
                             auth=('admin1','b.pXilJIcGCC4b.RVfeL8DdVQco8AOg'))
session = graph.session()

@app.route("/")
@app.route("/index")

def index():
    return render_template("index.html")

@app.route("/getplayers", methods=['GET', 'POST'])
def getplayers():
    #Extract information from user input
    school = request.form.get('school')
    print(school)
    query = '''
    MATCH (p:Player)-[:GRADUATED_FROM]->(s:HighSchool) 
    WHERE toLower(s.name) CONTAINS $school
    RETURN s.name as `High School`, p.name as `Player Name`, p.yearsOnRoster as `Years on Roster`, p.homeCity as `Player City`, p.homeState as `Player State`
    ORDER BY s.name, p.name
    '''
    results = session.run(query, school=school)
    return render_template("index.html",results=results)

