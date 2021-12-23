from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import json
import requests

app = Flask(__name__)
api = Api(app)

class Purchase(Resource):
    def put(self,num):
         
        info = requests.get('http://172.19.225.232:5001/info/'+str(num)).json()
        df = pd.DataFrame(info, columns = ['amount','title','cost'])
        amount = df.iloc[0]['amount']
        title = df.iloc[0]['title']
        cost = df.iloc[0]['cost']
        if (amount != 0):
           data = pd.read_csv('orders.csv')
           new_data = pd.DataFrame({
           'id'      : [num],
           'title'   : [title],
           'cost'   : [cost]
           })
           data = data.append(new_data, ignore_index = True)
           data.to_csv('orders.csv', index=False)
           # to catalog in same machine
           return requests.put('http://172.19.225.232:5001/update/item_num/'+str(num)).json()
        else:
          return {'message from A':'The operation is failed, this book is over'},200
          
         
    
# Add URL endpoints
api.add_resource(Purchase, '/purchase/<int:num>')

if __name__ == '__main__':
    app.run()
