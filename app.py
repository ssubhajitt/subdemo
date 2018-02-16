# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:53:31 2018

@author: GUNA
"""
import json
import os
from flask import Flask , request, make_response
app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    if request.method=='POST':
        req=request.get_json(silent=True,force=True)
        result=req.get("result")
        parameters=result.get("parameters")
        response=json.dumps(parameters, indent=4)
        #response="nwave chatbot is under construction"
        res= {"speech": response,"displayText": response,"source": "nWave-estimation-chatbot"}
        res = json.dumps(res, indent=4)
        print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

port = os.getenv('VCAP_APP_PORT', '5000')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
