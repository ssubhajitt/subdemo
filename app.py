"""
Flask webapp demo 1
"""
import os
from flask import Flask , request, make_response
from flask_basicauth import BasicAuth

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    if request.method=='POST':
	response="nwave chatbot is under construction."
	res= {	"speech": response,"displayText": response,"source": "nWave-estimation-chatbot"}
	res = json.dumps(res, indent=4)
	print(res)r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
