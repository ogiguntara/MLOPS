# -*- coding: utf-8 -*-
"""Credit Scoring Modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15kjTszc0907MB0oAIuM2sY4LALcBJTqV
"""

#!python3

import pickle
import time

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def loadData(filename):
  cols = ['label','Age','Language','Sex','Has_Credit','Region']

  df = pd \
          .read_csv(filename)[cols]

  return df

def PreprocessingData(data):
  labelAge = StandardScaler()
  AgeScaler = labelAge.fit_transform(data[['Age']])
  pickle.dump(AgeScaler,open('labelAge.pkl','wb'))

  labelLanguage = LabelEncoder()
  LanguangeEncoder = labelLanguage.fit_transform(data[['Language']])
  pickle.dump(labelLanguage,open('labelLanguage.pkl','wb'))

  labelSex = LabelEncoder()
  SexEncoder = labelSex.fit_transform(data[['Sex']])
  pickle.dump(labelSex,open('labelSex.pkl','wb'))

  labelHasCredit = LabelEncoder()
  HasCreditEncoder = labelHasCredit.fit_transform(data[['Has_Credit']])
  pickle.dump(labelSex,open('labelHasCredit.pkl','wb'))

  labelRegion = OneHotEncoder()
  RegionEncoder = labelRegion.fit_transform(data[['Region']].values).toarray()
  pickle.dump(labelRegion,open('labelRegion.pkl','wb'))

  data['AgeScaler'] = AgeScaler
  data['LanguangeEncoder'] = LanguangeEncoder
  data['SexEncoder'] = SexEncoder
  data['HasCreditEncoder'] = HasCreditEncoder

  dfRegion = pd.DataFrame(RegionEncoder, columns=["RegionEncoder_"+str(i) for i in range(len(RegionEncoder[0]))])
  data = pd.concat([data, dfRegion], axis=1)

  X = data.drop(['Age','Language','Sex','Has_Credit','Region','label'], axis=1).values
  y = data[['label']].values

  return X,y

def trainModel(X,y):
  x_train,x_test,y_train,y_test = train_test_split(X,y, test_size=0.2, random_state=0)

  start = time.time()
  model = DecisionTreeClassifier()
  model.fit(x_train, y_train)
  pickle.dump(model, open('modelDecisionTree.pkl','wb'))
  stop = time.time()
  print(f"Model done in {stop-start} sekon \n")

  y_predict = model.predict(x_test)
  print(classification_report(y_test, y_predict))


if __name__ == "__main__":
  filename = "data_train.csv"

  data = loadData(filename)
  X,y = PreprocessingData(data)
  trainModel(X,y)