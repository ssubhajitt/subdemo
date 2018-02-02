"""
Flask webapp demo 1
"""
from flask import Flask, request, make_response

app= Flask(__name__)
@app.route("/webhook",methods=['POST'])
def webhook():
    name = request.get("username")
    return "Welcome" + name

if(__name__=='__main__'):
    app.run(use_reloader=True,debug=True)
