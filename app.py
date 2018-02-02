"""
Flask webapp demo 1
"""
from flask import Flask, request, make_response

app= Flask(__name__)
@app.route("/webhook",methods=['GET'])
def webhook():
    return "Welcome TO nWave Chatbot flask webservice"

if(__name__=='__main__'):
    app.run(use_reloader=True,debug=True)
