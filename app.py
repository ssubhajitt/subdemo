# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:53:31 2018

@author: GUNA
"""
import json
import os
import pandas as pd
from flask import Flask , request, make_response
from sklearn.preprocessing import Imputer
from sklearn.decomposition import PCA
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
from sklearn.metrics import precision_score, \
    recall_score, confusion_matrix, classification_report, \
    accuracy_score, f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    if request.method=='POST':
        req=request.get_json(silent=True,force=True)
        result=req.get("result")
        parameters=result.get("parameters")
        response=json.dumps(parameters, indent=4)
        print(response)
        ##Machine  Learning model
        #response="nwave chatbot is under construction"
        res= {"speech": response,"displayText": response,"source": "nWave-estimation-chatbot"}
        res = json.dumps(res, indent=4)
        print(res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r

def mvRegression(data):
    dataset = pd.read_excel("https://github.com/s-gunalan/nWave-Flask-Demo/blob/master/dataset.xlsx?raw=true",skip_header=1)
    Y=dataset.iloc[:, 14:]
    X=dataset.iloc[:,1:14]
    header=list(df)
    imputer = Imputer()
    dataset = imputer.fit_transform(X)
    X_tr,X_te,Y_tr,Y_te=train_test_split(X,Y,test_size=0.2)
    print (X_tr.shape,Y_tr.shape,X_te.shape,Y_te.shape)
    lr=LinearRegression()
    model_lr=lr.fit(X_tr,Y_tr)
    op_lrt=lr.predict(X_te)
    val=[1,8,1,1,2,2,2,1,1,3,3,1,1]
    return "None"

port = os.getenv('VCAP_APP_PORT', '5000')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),use_reloader=True, debug=True)
