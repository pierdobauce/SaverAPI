'''
Created on 18 janv. 2017

@author: opbo6311
'''
import os
# Using Flask since Python doesn't have built-in session management
from flask import Flask, session, render_template
# Our target library
import requests
import json

app = Flask(__name__)

# Generate a secret random key for the session
app.secret_key = os.urandom(24)

# Define routes for the examples to actually run
@app.route('/run_get')
def run_get():
    url = 'https://api.github.com/users/runnable'

    # this issues a GET to the url. replace "get" with "post", "head",
    # "put", "patch"... to make a request using a different method
    r = requests.get(url)

    return json.dumps(r.json(), indent=4)


# Define a route for the webserver
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run( 
        host="0.0.0.0",
        port=int("80")
    )
