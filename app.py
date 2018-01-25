# -*- coding: utf-8 -*-
"""
Flask webapp demo 1
"""
from flask import Flask
from flask import request
from flask import make_response

app= Flask(__name__)
@app.route("/webhook",methods=['POST'])
def webhook():
    req=request.get_json(silent=True,force=True)
    print("Request:")
    print(json.dumps(req,indent=4))
    speech=process()
    res=make_response(speech)
    return res
def process():
    return {
    "speech": "Welcome to nWave Chatbot",
    "displayText": "Welcome to nWave Chatbot",
    "source": "nWave_webhook"
    }
if(__name__=='__main__'):
    app.run(use_reloader=True,debug=True)
