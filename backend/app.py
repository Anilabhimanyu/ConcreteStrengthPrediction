from flask import Flask
from flask import render_template,request
# from flask_restful import Api,Resource,reqparse
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
import pickle
import os
import psycopg2
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return 'home'

TargetVariable='Strength'
Predictors=['CementComponent ','BlastFurnaceSlag','WaterComponent','SuperplasticizerComponent','CoarseAggregateComponent','FineAggregateComponent','AgeInDays']

DataForML_Numeric=pd.read_pickle(r"E:\FYP\venv\DataForML (1).pkl")

X=DataForML_Numeric[Predictors].values
PredictorScaler=MinMaxScaler()
PredictorScalerFit=PredictorScaler.fit(X)
X=PredictorScalerFit.transform(X)


# This Function can be called from any from any front end tool/website
def FunctionPredictResult(InputData):
    X=InputData
    print(X)
    X=PredictorScalerFit.transform(X)
    print("scaling after X", X)
    # Loading the Function from pickle file
    with open(r'E:\FYP\venv\Final_XGboost_model.pkl', 'rb') as fileReadStream:
        PredictionModel=pickle.load(fileReadStream)
        # Don't forget to close the filestream!
        fileReadStream.close()
            
    # Generating Predictions
    Prediction=PredictionModel.predict(X)
    PredictionResult=pd.DataFrame(Prediction, columns=['Prediction'])
    print("2. i am executed")

    return(round(PredictionResult))

# Creating the function which can take inputs and perform prediction
def FunctionGeneratePrediction(inp_CementComponent,inp_blastfurnaceslag,inp_watercomponent, inp_SuperplasticizerComponent,inp_coarseaggregatecomponent,inp_fineaggregatecomponent, inp_AgeInDays):
    # Creating a data frame for the model input
    SampleInputData=pd.DataFrame(
     data=[[inp_CementComponent,inp_blastfurnaceslag,inp_watercomponent, inp_SuperplasticizerComponent,inp_coarseaggregatecomponent,inp_fineaggregatecomponent, inp_AgeInDays]],
     columns=['CementComponent ','BlastFurnaceSlag','WaterComponent','SuperplasticizerComponent','CoarseAggregateComponent','FineAggregateComponent','AgeInDays'])

    # Calling the function defined above using the input parameters
    Predictions=FunctionPredictResult(InputData= SampleInputData)

    # Returning the predictions
    print("1. i am executed")
    return(Predictions.to_json())

# for prediction
@app.route('/predict', methods=['POST'])
def get_values():
    # inp_CementComponent,inp_blastfurnaceslag,inp_watercomponent, inp_SuperplasticizerComponent,inp_coarseaggregatecomponent,inp_fineaggregatecomponent, inp_AgeInDays):
    
    inp_CementComponent = request.args.get('inp_CementComponent')
    inp_blastfurnaceslag = request.args.get('inp_blastfurnaceslag')
    inp_watercomponent = request.args.get('inp_watercomponent')
    inp_SuperplasticizerComponent = request.args.get('inp_SuperplasticizerComponent')
    inp_coarseaggregatecomponent = request.args.get('inp_coarseaggregatecomponent')
    inp_fineaggregatecomponent = request.args.get('inp_fineaggregatecomponent')
    inp_AgeInDays = request.args.get('inp_AgeInDays')

    if not inp_CementComponent or not inp_blastfurnaceslag or not inp_watercomponent or not inp_SuperplasticizerComponent or not inp_coarseaggregatecomponent or not inp_fineaggregatecomponent or not inp_AgeInDays:
        return 'Missing input values', 400
    # Do something with the input values, such as returning them in JSON format
    print("i'm main executed----------------")

    fns=FunctionGeneratePrediction(inp_CementComponent,inp_blastfurnaceslag,inp_watercomponent, inp_SuperplasticizerComponent,inp_coarseaggregatecomponent,inp_fineaggregatecomponent, inp_AgeInDays)

    return (fns)



## database connectivity
def db_connectivity():
    conn = psycopg2.connect(database="flaskdb",
						user="postgres",
						password="34183418",
						host="localhost", port="5432")
    return conn

    # cur = conn.cursor()
    # print('connection made succesfully')

    # conn.commit()

    # cur.close()
    # conn.close()
    # return 'conn made succhessfully',200

# for registration
@app.route('/register', methods=['POST'])
def register():
    uname = request.args.get('username')
    pwd = request.args.get('password')
    if not uname or not pwd :
        return 'Missing input values', 400
    # Do something with the input values, such as returning them in JSON format
    conn = psycopg2.connect(database="flaskdb",
						user="postgres",
						password="34183418",
						host="localhost", port="5432")
    cur=conn.cursor()
    print('connection made succesfully')
    cur.execute("""select count(username) FROM users where username=%s""",(uname,))
    users_list=cur.fetchone()
    print(users_list)
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()
    if len(users_list):
        return 'user already exists'
    else:
        conn = psycopg2.connect(database="flaskdb",
            user="postgres",
            password="34183418",
            host="localhost", port="5432")
        cur=conn.cursor()
        # print('connection made succesfully')
        cur.execute("""INSERT INTO users values(%s,%s)""",(uname,pwd))
        # commit the changes
        conn.commit()
        # close the cursor and connection
        cur.close()
        conn.close()
        return 'user entered succesfully'
    
# for login
@app.route('/login', methods=['POST'])
def login():
    uname = request.args.get('username')
    pwd = request.args.get('password')
    if not uname or not pwd :
        return 'Missing input values', 400
    # Do something with the input values, such as returning them in JSON format
    conn = psycopg2.connect(database="flaskdb",
						user="postgres",
						password="34183418",
						host="localhost", port="5432")
    cur=conn.cursor()
    print('connection made succesfully')
    cur.execute("""select count(username) FROM users where username=%s and password=%s""",(uname,pwd))
    users_list=cur.fetchone()
    print(users_list)
    conn.commit()
    # close the cursor and connection
    cur.close()
    conn.close()
    if len(users_list):
        return 'logged in successfully'
    else:
        return 'credential errors are there'

# for logout
@app.route('/logout')
def logout():
    return 'logged out succesfully'
    # return render_template('home_logout.html')
if __name__ == '__main__':
    app.run(debug=True)
