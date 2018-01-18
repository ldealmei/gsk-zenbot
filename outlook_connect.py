# First connection : Clicking that link will take them to the Azure login page where they can login with their Office 365
# or Outlook.com account and grant access to our app. Finally, they will be redirected back to our app
#

import base64
import mimetypes
import os
import pprint
import uuid
import requests
import flask
import json

from flask_oauthlib.client import OAuth

import config

#
# mdp = "ksnT555):vfrbEPFZGX93#-"
# mdp_via_graph = "yctX90;|oqirOOCYEG521|*"


APP = flask.Flask(__name__, template_folder='static/templates')
APP.debug = True
APP.secret_key = 'development'
OAUTH = OAuth(APP)
MSGRAPH = OAUTH.remote_app(
    'gsk-hackathon',
    consumer_key=config.CLIENT_ID,
    consumer_secret=config.CLIENT_SECRET,
    request_token_params={'scope': config.SCOPES},
    base_url=config.RESOURCE + config.API_VERSION + '/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=config.AUTHORITY_URL + config.TOKEN_ENDPOINT,
    authorize_url=config.AUTHORITY_URL + config.AUTH_ENDPOINT)

@APP.route('/')
def homepage():
    """Render the home page."""
    return flask.render_template('homepage.html')

@APP.route('/login')
def login():
    """Prompt user to authenticate."""
    flask.session['state'] = str(uuid.uuid4())
    MSGRAPH.authorize(callback=config.REDIRECT_URI, state=flask.session['state'])

    return get_my_events()

@APP.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect Uri."""

    # if str(flask.session['state']) != str(flask.request.args['state']):
    #     raise Exception('state returned to redirect URL does not match!')
    response = MSGRAPH.authorized_response()
    flask.session['access_token'] = response['access_token']

    print(response)
    return flask.redirect('/')


@MSGRAPH.tokengetter
def get_token():
    """Called by flask_oauthlib.client to retrieve current access token."""
    return (flask.session.get('access_token'), '')

def request_headers(headers=None):
    """Return dictionary of default HTTP headers for Graph API calls.
    Optional argument is other headers to merge/override defaults."""
    default_headers = {'SdkVersion': 'sample-python-flask',
                       'x-client-SKU': 'sample-python-flask',
                       'client-request-id': str(uuid.uuid4()),
                       'return-client-request-id': 'true'}
    if headers:
        default_headers.update(headers)
    return default_headers

@APP.route('/')
def get_my_events(access_token=None, user_email=None):

    print("accessing function...")
    graph_endpoint  = 'https://graph.microsoft.com/v1.0{0}'

    get_events_url = graph_endpoint.format('/me/events')
    query_parameters = {'$top': '10',
                        '$select': 'subject,start,end',
                        '$orderby': 'start/dateTime ASC'}

    r = make_api_call('GET', get_events_url, flask.session.get('access_token'), 'remplacer@hotmail.com', parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        print(r.json())
        return r.json()

    else:
        print("{0}: {1}".format(r.status_code, r.text))
        return "{0}: {1}".format(r.status_code, r.text)

# Generic API Sending
def make_api_call(method, url, token, user_email, payload = None, parameters = None):
  # Send these headers with all API calls
  headers = { 'User-Agent' : 'python_tutorial/1.0',
              'Authorization' : 'Bearer {0}'.format(token),
              'Accept' : 'application/json',
              'X-AnchorMailbox' : user_email }

  # Use these headers to instrument calls. Makes it easier
  # to correlate requests and responses in case of problems
  # and is a recommended best practice.
  request_id = str(uuid.uuid4())
  instrumentation = { 'client-request-id' : request_id,
                      'return-client-request-id' : 'true' }

  headers.update(instrumentation)

  response = None

  if (method.upper() == 'GET'):
    print('launching request')
    response = requests.get(url, headers = headers, params = parameters)
  elif (method.upper() == 'DELETE'):
    response = requests.delete(url, headers = headers, params = parameters)
  elif (method.upper() == 'PATCH'):
    headers.update({ 'Content-Type' : 'application/json' })
    response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
  elif (method.upper() == 'POST'):
    headers.update({ 'Content-Type' : 'application/json' })
    response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

    return response

if __name__ == '__main__':
    APP.run()
