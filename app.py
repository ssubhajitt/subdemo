"""
Flask webapp demo 1
"""
import os
from flask import Flask , request
from flask_basicauth import BasicAuth

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
	if request.method=='POST':
		return "nWave Chatbot is under construction"

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
