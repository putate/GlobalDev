
from flask import Flask, url_for, request, Markup, render_template, flash, Markup
import os
import json
app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():    
    return render_template('home.html')
 
@app.route("/p1")
def render_page1():
    with open('global_development.json') as demographics_data:
        countries = json.load(demographics_data)
    
    if 'years' in request.args:
        return render_template('page1.html', years = get_year_options(countries), fertility_rate = get_fertility_rate(countries, request.args['years']),  birth_rate = get_birth_rate(countries, request.args['years']))
    else:
        return render_template('page1.html', years = get_year_options(countries))

@app.route("/p2")
def render_page2():
    with open('global_development.json') as demographics_data:
        countries = json.load(demographics_data)
    
    if 'countries' in request.args:
        return render_template('page2.html', countries = get_country_options(countries), net_change = get_net_change(countries, request.args['countries']), avg_pop = get_avg_pop(countries, request.args['countries']))
    else:
        return render_template('page2.html', countries = get_country_options(countries))

@app.route("/p3")
def render_page3():
    with open("global_development.json") as demographics_data:
        countries = json.load(demographics_data)
    return render_template('page3.html', inp = get_points(countries))
 
def get_points_assist(countries, year):
    ruralpop = 0
    for data in countries:
        if data["Year"] == year:
            ruralpop = ruralpop + data['Data']['Rural Development']['Rural Population']
    return ruralpop
    
def get_points(countries):
    options = ""
    years = 1980
    while years <= 2013:
        options = options + Markup("{x :new Date(" + str(years) + ",0), y:" + str(get_points_assist(countries, years)) + "},")
        years +=1    
    return options
    
    
def get_year_options(countries):
    countries1 = []
    print("RunningOPYear")
    for data in countries:
        if data["Year"] not in countries1:
            countries1.append(data["Year"])
    options = ""
    for data in countries1:
        options = options + Markup("<option value=\"" + str(data) + "\">" + str(data) + "</option>")
    return options
    
def get_country_options(countries):
    countries1 = []
    print("RunningOPCountries")
    for data in countries:
        if data["Country"] not in countries1:
            countries1.append(data["Country"])
    options = ""
    for data in countries1:
        options = options + Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options
    
def get_fertility_rate(countries, years):
    print("RunningFert")
    statement1 = "The highest fertility rate in "
    statement2 = " was "
    p = "."
    fertility_rate=0
    for data in countries:
        if data['Data']['Health']['Fertility Rate'] > fertility_rate:
            if str(data['Year']) == years:
                print("IfStat")
                fertility_rate = data['Data']['Health']['Fertility Rate']
    return (statement1 + str(years) + statement2 + str(fertility_rate) + p)
    
def get_birth_rate(countries, years):
    print("RunningFert")
    statement1 = "The highest birth rate was "
    p = "."
    fertility_rate=0
    for data in countries:
        if data['Data']['Health']['Birth Rate'] > fertility_rate:
            if str(data['Year']) == years:
                print("IfStat")
                fertility_rate = data['Data']['Health']['Birth Rate']
    return (statement1 + str(fertility_rate) + p)
    
    
    
def get_net_change(countries, countrys):
    statement1 = "The net population change in  "
    statement2 = " from 1980-2013 was "
    p = "."
    popint = 0
    popfin = 0
    for data in countries:
        if (data['Country'] == countrys) and (data['Year'] == 1980):
            popint = data['Data']['Health']['Total Population']
 
    for data in countries:
        if (data['Country'] == countrys) and (data['Year'] == 2013):
            Popfin = data['Data']['Health']['Total Population']
    return (statement1 + str(countrys) + statement2 + str(int(abs(popfin-popint))) + p)
    
def get_avg_pop(countries, countrys):
    statement1 = "The avg population growth per year of  "
    statement2 = " from 1980-2013 was "
    p = "."
    popint = 0
    for data in countries:
        if (data['Country'] == countrys):
            popint += data['Data']['Health']['Population Growth']
    return (statement1 + str(countrys) + statement2 + str(popint/33) + p)
    
if __name__=="__main__":
    app.run(debug=True)
