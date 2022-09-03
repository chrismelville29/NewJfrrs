'''
    api.py
    Christopher Melville

    Flask API to support tfrrs piracy

    - Leagues and managers are referred to as makeables

'''
import sys
import flask
from flask import request
import json
from os.path import exists as file_exists


def get_bigass_json_object(conference):
    return json.loads(open('data/conferences/'+conference,'r').read())

def rewrite_file(path, data):
    with open(path, 'w') as file:
        file.write(json.dumps(data))

def get_manager_leagues_json(manager):
    return json.loads(open('data/managers','r').read())[manager]

def get_league_json(league_name):
    return json.loads(open('data/leagues/'+league_name,'r').read())

def makeable_exists(key, data):
    if key in data:
        return 'found'
    return 'distinct'

def manager_exists(manager):
    if manager in json.loads(open('data/managers', 'r').read()):
        return 'found'
    return 'distinct'

def league_exists(league):
    if file_exists('data/leagues/'+league):
        return 'found'
    return 'distinct'

#include data if you want to add, have parameter none if just checking existence
def check_makeable(type, key, data):
    makeables = json.loads(open('data/'+type,'r').read())
    exists = makeable_exists(key, makeables)
    if exists == 'distinct' and data != None:
        makeables[key] = data
        rewrite_file('data/'+type, makeables)
    return exists

#include data if you want to add, have parameter none if just checking existence
def find_manager(manager_name, data):
    managers = json.loads(open('data/managers','r').read())
    exists = manager_exists(manager_name)
    if exists == 'distinct' and data != None:
        managers[manager_name] = data
        rewrite_file('data/managers', managers)
    return exists
    
def check_league(league_name, data):
    exists = league_exists(league_name)
    if exists == 'distinct' and data != None:
        rewrite_file('data/leagues/'+league_name,data)
        add_manager_to_league(data['creator'],league_name)
    return exists



#returns found if the manager was in the league, absent if not
def manager_in_league(manager_name, league_name):
    manager = json.loads(open('data/managers','r').read())[manager_name]
    if league_name in manager:
        return 'redundant'
    add_manager_to_league(manager_name, league_name)
    return 'added'

def add_manager_to_league(manager_name, league_name):
    managers = json.loads(open('data/managers','r').read())
    league = json.loads(open('data/leagues/'+league_name,'r').read())
    managers[manager_name][league_name] = league['conference']
    league['managers'].append(manager_name)
    rewrite_file('data/leagues/'+league_name,league)
    rewrite_file('data/managers',managers)


api = flask.Blueprint('api', __name__)

@api.route('/conferences/<conference>/athletes/<sort_distance>')
def get_players(conference, sort_distance):
    sort_key = lambda athlete: (athlete['relevant_prs'][sort_distance],athlete['name'])
    return json.dumps(sorted(get_bigass_json_object(conference)['athletes'],key = sort_key))


@api.route('/check_manager', methods = ['POST'])
def check_manager():
    input = request.json
    data_to_add = None
    if input['create'] == 'yes':
        data_to_add = {}
    return json.dumps({'status':find_manager(input['username'], data_to_add)})


@api.route('/create_league', methods = ['POST'])
def create_league():
    input = request.json
    empty_league = {'name':input['name'],'creator':input['creator'],'conference':input['conference'],'managers':[],'weeks':[]}
    status = check_league(input['name'],empty_league)
    return json.dumps({'status':status})

@api.route('/join_league', methods = ['POST'])
def join_league():
    input = request.json
    if check_league(input['league_name'],None) == 'distinct':
        return json.dumps({'status':'league_not_found'})
    return json.dumps({'status':manager_in_league(input['manager_name'],input['league_name'])})

@api.route('/managers/<manager>')
def get_leagues(manager):
    return get_manager_leagues_json(manager)

@api.route('/leagues/<league_name>')
def get_league(league_name):
    return get_league_json(league_name)



