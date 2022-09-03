'''
    app.py
    Chris Melville
    Fantasy Track
'''
import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')


@app.route('/')
def load_homepage():
    return flask.render_template('homepage.html')

@app.route('/athletes/<conference>')
def load_athletes_page(conference):
    return flask.render_template('athletes_page.html', conference_id=conference)

@app.route('/create_manager')
def load_create_manager_page():
    return flask.render_template('create_manager.html')

@app.route('/create_league/<username>')
def load_create_league_page(username):
    return flask.render_template('create_league.html',username=username)


@app.route('/login')
def load_login_page():
    return flask.render_template('login_page.html')

@app.route('/manager_home/<username>')
def load_manager_home_page(username):
    return flask.render_template('manager_home.html', username=username)

@app.route('/league_home/<league_name>/<username>')
def load_league_home_page(league_name, username):
    return flask.render_template('league_home.html',league_name=league_name,username=username)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A fantasy track application')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
