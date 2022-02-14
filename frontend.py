from flask import Flask, g, session, render_template, request, redirect, url_for
from requests_oauthlib import OAuth2Session
from threading import Thread
import os
import random

OAUTH2_CLIENT_ID = os.environ['DISCORD_BOT_CLIENT_ID']
OAUTH2_CLIENT_SECRET = os.environ['DISCORD_BOT_CLIENT_SECRET']

API_BASE_URL = 'https://discordapp.com/api'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'


app = Flask('')
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

def token_updater(token):
  session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
  return OAuth2Session(
    client_id=OAUTH2_CLIENT_ID,
    token=token,
    state=state,
    scope=scope,
    redirect_uri=url_for('.callback', _external=True, _scheme='https'),
    auto_refresh_kwargs={
      'client_id': OAUTH2_CLIENT_ID,
      'client_secret': OAUTH2_CLIENT_SECRET,
    },
    auto_refresh_url=TOKEN_URL,
    token_updater=token_updater
  )

@app.context_processor
def app_processor():
  def app_title():
    return "PbtA Dice"
  
  return dict(app_title=app_title)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
def login():
  scope = request.args.get(
        'scope',
        'identify guilds')
  discord = make_session(scope=scope.split(' '))
  authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
  session['oauth2_state'] = state
  return redirect(authorization_url)

@app.route('/logout')
def logout():
  return render_template('logout.html')

@app.route('/callback')
def callback():
  if request.values.get('error'):
    return request.values['error']
  discord = make_session(state=session.get('oauth2_state'))
  auth_response = request.url
  if "http:" in auth_response:
    auth_response = "https:" + auth_response[5:]
  token = discord.fetch_token(
    TOKEN_URL,
    client_secret=OAUTH2_CLIENT_SECRET,
    authorization_response=auth_response
  )
  session['oauth2_token'] = token
  return redirect(url_for('.dashboard'))

@app.route('/dashboard/', defaults={'id':None})
@app.route('/dashboard/<id>')
def dashboard(id=None):
  discord = make_session(token=session.get('oauth2_token'))
  g.user = discord.get(API_BASE_URL + '/users/@me').json()
  g.guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
  if id is not None:
    # Loads the specified guild
    g.guild = id
  return render_template('dashboard.html')

def run():
  app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def frontend():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()