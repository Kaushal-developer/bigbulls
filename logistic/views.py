# Create your views here.
from re import S
import re
from django.db import reset_queries
from django.http import response
from django.shortcuts import render, HttpResponse
from ssl import CERT_REQUIRED
from urllib.parse import quote
from nsetools import Nse
from numpy.lib.histograms import histogram_bin_edges
from requests.api import get
from logistic.models import Scrips
from datetime import date
from nsepy import get_history, history
from django.http import JsonResponse
# Create your views here.
import json
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import datetime
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.graph_objects as go
from sklearn import preprocessing;
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from json import JSONEncoder
import os
from twilio.rest import Client
import urllib.request
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    # data = Scrips.objects.values("code","name")
    # final_scripts = []
    # for record in data:
    #     info={}
    #     info["code"] = record['code']
    #     info["name"] = record["name"]
    #     final_scripts.append(final_scripts)
    try:
        nse = Nse()
        scripts = nse.get_stock_codes()
        return render(request,'index.html', {'scrips':scripts})
    except Exception as e:
        return HttpResponse('invalid')

@csrf_exempt
def get_monthly_active(request):
    nse = Nse()
    monthly_active_trending = nse.get_active_monthly()
    return JsonResponse({'monthly_active_trending': monthly_active_trending})


@csrf_exempt
def get_advance_declined(request):
    nse = Nse()
    adv_dec = nse.get_advances_declines()
    return JsonResponse({'adv_dec': adv_dec})


@csrf_exempt
def get_top_gainer(request):
    nse = Nse()
    top_gainers = nse.get_top_gainers()
    return JsonResponse({'top_gainers': top_gainers})


@csrf_exempt
def get_top_loosers(request):
    nse = Nse()
    top_losers = nse.get_top_losers()
    return JsonResponse({'top_losers': top_losers})


@csrf_exempt
def get_history_data(request):
    from nsepy import get_history
    nse = Nse()
    script = request.POST.get('symbol')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if from_date and to_date and script:
        if nse.is_valid_code(script):
            history= get_history(symbol=script, start=datetime.strptime(from_date, '%Y-%m-%d'), end=datetime.strptime(to_date, '%Y-%m-%d'))
            forecast_col = 'Close'
            forecast_out = 5 #how far to forecast 
            test_size = 0.2; #the size of my test set
            X_train, X_test, Y_train, Y_test , X_lately =prepare_data(history,forecast_col,forecast_out,test_size); 
            learner = linear_model.LinearRegression(); #initializing linear regression model
            learner.fit(X_train,Y_train); #training the linear regression model
            score=learner.score(X_test,Y_test);#testing the linear regression model
            forecast= learner.predict(X_lately); #set that will contain the forecasted data
            response={};#creting json object
            response['test_score']=score
            response['forecast_set']=forecast.tolist()
            data = {}
            data['history'] = history.to_json(orient='split')
            data['response'] = json.dumps(response,cls=NumpyArrayEncoder)
            return JsonResponse(data)
        else:
            return HttpResponse("Enter correct script")
    else:
        return HttpResponse("Enter correct script")


@csrf_exempt
def get_realtime_data(request):
    nse = Nse()
    script = request.POST.get('symbol')
    print(script)
    if nse.is_valid_code(script):
        data = nse.get_quote(script)
        for info in data:
            print(info)
        return JsonResponse({'realTime':data})
    else:
        return HttpResponse("Enter correct script")


def prepare_data(df,forecast_col,forecast_out,test_size):
    label = df[forecast_col].shift(-forecast_out);#creating new column called label with the last 5 rows are nan\
    X = np.array(df[[forecast_col]]); #creating the feature array
    X = preprocessing.scale(X) #processing the feature array
    X_lately = X[-forecast_out:] #creating the column i want to use later in the predicting method
    X = X[:-forecast_out] # X that will contain the training and testing
    label.dropna(inplace=True); #dropping na values
    y = np.array(label)  # assigning Y
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=test_size) #cross validation 
    response = [X_train,X_test , Y_train, Y_test , X_lately]
    return response

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)



