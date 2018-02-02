"""
Flask webapp demo 1
"""
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def Welcome():
	return 'Welcome to my app running on Bluemix!'

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
