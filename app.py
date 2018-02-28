import json
import os
import pandas as pd
from flask import Flask , request, make_response
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    req=request.get_json(silent=True,force=True)
    result=req.get("result")
    parameters=result.get("parameters")
    data=json.dumps(parameters, indent=4)
    print(data)
    mvRegression()
    response="nwave chatbot is under construction"
    res= {"speech": response,"displayText": response,"source": "nWave-estimation-chatbot"}
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def mvRegression():
    #dataset = pd.read_excel("https://github.com/s-gunalan/nWave-Flask-Demo/blob/master/dataset.xlsx?raw=true",skip_header=1)
    dataset=pd.read_excel("D:/Guna/POCs/ML/nWave_effort/dataset.xlsx",skip_header=1)
    Y=dataset.iloc[:, 14:]
    X=dataset.iloc[:,1:14]
    header=list(dataset)
    imputer = Imputer()
    dataset = imputer.fit_transform(X)
    X_tr,X_te,Y_tr,Y_te=train_test_split(X,Y,test_size=0.2)
    print (X_tr.shape,Y_tr.shape,X_te.shape,Y_te.shape)
    lr=LinearRegression()
    model_lr=lr.fit(X_tr,Y_tr)
    val=[1,8,1,1,2,2,2,1,1,3,3,1,1]
    ds=pd.DataFrame(val).T
    op_lrt=lr.predict(ds)
    weightage=op_lrt[0][0]
    print(weightage)
    return weightage




if __name__ == '__main__':
	app.run(use_reloader=True, debug=True)
