import json
import os
import requests
import pickle
import pandas as pd
import cloudant
from cloudant import Cloudant
from docx import Document
from flask import Flask , request, make_response , render_template, session,g
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey,QueryResult

user= "9ef80d52-30b9-4e45-833a-75059db0825c-bluemix"
password= "79d7c792bb13072da32aecc7dc3777e28780d6d11619795d54d717d2abbd62e5"
host= "9ef80d52-30b9-4e45-833a-75059db0825c-bluemix.cloudant.com"
url = 'https://' + host
client = Cloudant(user, password, url=url, connect=True)    
app = Flask(__name__)
app.config['SECRET_KEY']="QWERTYUIOPASDFGHJKLZXCVBNM"

@app.route('/')
def homepage():
    return render_template('chatbotPage.html')

@app.route('/webhook',methods=['POST'])
def webhook():
    url="https://nwave-ideabot-flask-webhook-p.herokuapp.com/storedata"
    global output
    output={}
    try:
        req=request.get_json(silent=True,force=True)
        sessionId=req.get("sessionId")
        result=req.get("result")
        contexts=result.get("contexts")
        par=contexts[1].get("parameters")
        product=par.get("product")
        srcprotocol=par.get("srcprotocol")
        srcformat=par.get("srcformat")
        targetmsgformat=par.get("targetmsgformat")
        targetprotocol=par.get("targetprotocol")
        associateId=par.get("number-integer")
        operationcount=par.get("operationcount")
        int-dataformat=par.get("int-dataformat")
        Interface-type=par.get("Interface-type")
        rulecount=par.get("rulecount")
        msgfieldcount=par.get("msgfieldcount")
        exposed-as-api=par.get("exposed-as-api")
        new-existing=par.get("new-existing")
        disp-product=par.get("product.original")
        disp-srcF=par.get("srcformat.original")
        disp-srcP=par.get("srcprotocol.protocol")
        disp-targetF=par.get("targetmsgformat")
        disp-targetP=par.get("targetprotocol")
        weightage=intRegression(req)
        op={'sessionId':sessionId,
            'weightage':weightage,
            'product':product,
            'srcprotocol':srcprotocol,
            'srcformat':srcformat,
            'targetmsgformat':targetmsgformat,
            'targetprotocol':targetprotocol,
            'associateId':associateId,
            'operationcount':operationcount, 
            'int-dataformat':int-dataformat,
            'Interface-type': Interface-type,
            'rulecount':rulecount,
            'msgfieldcount':msgfieldcount,
            'exposed-as-api':exposed-as-api,
            'new-existing':new-existing,
            'disp-product':disp-product,
            'disp-srcF':disp-srcF,
            'disp-srcP':disp-srcP,
            'disp-targetF':disp-targetF,
            'disp-targetP':disp-targetP
           }
        print(op)
        session = client.session()
        print('Username: {0}'.format(session['userCtx']['name']))
        print('Databases: {0}'.format(client.all_dbs()))
        db = client['nwaveoutput']
        doc= db.create_document(op)
        doc.save()
        print(doc)
        for document in db:
            print(document)
        #send_data=requests.post(url,data={'key':weightage,'sessionId':sessionId})
       
        response="Estimated Value for the interface is :<strong> %s PD <br></strong><i>Do you need estimation for another interface ? (Yes/No) </i>" %(weightage)
    except:
        response="Sorry Bot has faced an issue! Please try after sometime!"
    
    res= {"speech": response,"displayText": "LOAD-PAGE","source": "nWave-estimation-chatbot"}
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
   
def intRegression(req):
    #Machine Learning Model
    dataset = pd.read_excel("https://github.com/s-gunalan/nWave-Flask-Demo/blob/master/dataset_integration_v2.xlsx?raw=true",skip_header=1)
    #dataset=pd.read_excel("D:/Guna/POCs/ML/nWave_effort/dataset_integration.xlsx",skip_header=1)
    Y=dataset.iloc[:, 13:]
    X=dataset.iloc[:,1:13]
    header=list(X)
    imputer = Imputer()
    dataset = imputer.fit_transform(X)
    lr=LinearRegression()
    model_int=lr.fit(X,Y)

    #Data Processing
    val=[]
    result=req.get("result")
    contexts=result.get("contexts")
    print(contexts[0])
    parameters=contexts[0].get("parameters")
    for i in header:
        str=parameters.get(i)
        print("%s %s " %(i,str))
        val.append(str)
    ds=pd.DataFrame(val).T
    print(ds)

    #Prediction
    op_lrt=lr.predict(ds)
    op=round(op_lrt[0][0],2)
    print(op)
    return op

@app.route('/getop/<sessionId>')
def getop(sessionId):
    session = client.session()
    db = client['nwaveoutput']
    query = cloudant.query.Query(db,selector={"sessionId": sessionId})
    query_result = QueryResult(query)
    generate_docx(query_result)
    print(query_result)
   
    for doc in query_result:
        print(doc['weightage'])
    
    return render_template('output.html',weightage=query_result)
    #except:
    #   return "Sorry something went wrong"
        
@app.route('/docx')
def download_docx():
    with open("static/estimate.docx", 'rb') as f:
        body = f.read()
    response = make_response(body)
    response.headers["Content-Disposition"] = "attachment; filename=estimate.docx"
    return response    

def generate_docx(query_result):
    document = Document("static/template.docx")      
    
    for doc in query_result:
        document.add_heading("Interface Details:",level=2)
        document.add_paragraph("Product           : " + doc['parameters']['product.original'])
        document.add_paragraph("Source Protocol   : " + doc['parameters']['srcprotocol.original'])
        document.add_paragraph("Source Msg Format : " + doc['parameters']['srcmsgformat.original'])
        document.add_paragraph("Target Protocol   : " + doc['parameters']['targetprotocol.original'])
        document.add_paragraph("Target Msg format :" + doc['parameters']['targetmsgformat.original'])
        
        document.add_heading("Effort Details:",level=2)       
        document.add_paragraph("Design:" + str(doc['weightage']*0.25))
        document.add_paragraph("Test:" + str(doc['weightage']*0.25))
        document.add_paragraph("Development:" + str(doc['weightage']*0.5))
        document.add_paragraph("Total Effort:" + str(doc['weightage']))
        
    document.add_heading("Consolidated Details:",level=2)    
    table = document.add_table(rows=1, cols=6, style='TableGrid')
    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'S.No'
    hdr_cells[1].text = 'Interface Details'
    hdr_cells[2].text = 'Effort'
    for doc in query_result:
        row_cells = table.add_row().cells
        
        row_cells[1].text = doc['parameters']['product.original']
        row_cells[2].text = str(doc['weightage'])
    document.add_paragraph("End of the Document")
    document.save("static/estimate.docx")
    return document


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
       	app.run(host='0.0.0.0', port=int(port), use_reloader=True, debug=True)
