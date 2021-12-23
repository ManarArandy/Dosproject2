from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import requests
import json
app = Flask(__name__)
api = Api(app)

# Info
           
class Info(Resource):

    def get(self,num):
        self.data = pd.read_csv('catalog.csv')
        data_fount=self.data.loc[self.data['id'] == num]
        
        dataFrame = pd.DataFrame(data_fount, columns = ['title','amount', 'cost'])
        convert = dataFrame.to_json(orient="records")
        #loads() is used to convert the JSON String document into the Python dictionary
        parse = json.loads(convert)
        return parse 
  
class Search(Resource):

    def get(self,topic):
        #read data file
        self.data = pd.read_csv('catalog.csv')
        #Search by topic to get all the items under this topic
        items=self.data.loc[self.data['topic'] == topic]
        #convert it to data frame and pick id and title columns
        dataFrame = pd.DataFrame(items, columns = ['id', 'title'])
        convert = dataFrame.to_json(orient="records")
        #loads() is used to convert the JSON String document into the Python dictionary
        parse = json.loads(convert)
        return parse  

          
class Update(Resource):

    def put(self,num):
        self.data = pd.read_csv('catalog.csv')
        #to get book name to use it in message
       
        titlee = self.data.loc[self.data['id'] == num]
        df = pd.DataFrame(titlee, columns=['title', 'amount', 'cost'])
        title = df.iloc[0]['title']
        
        #get entities with the this id and decrement their amount by one after purchasing successfully
        self.data.loc[self.data["amount"].loc[self.data["id"] == num].index,"amount"] = self.data["amount"] - 1
        self.data.to_csv("catalog.csv", index=False)
        
        
        #invalidate on frontendServer
        requests.get('http://172.19.233.25:5000/invalidate/'+str(num))
        #update on catalogServer on the other machine(ubunto) 
        requests.put('http://172.19.232.86:5003/update2/item_num/'+str(num)).json()
        return {'message from A':'You bought this book sucessfully'},200

class Update2(Resource):

      def put(self,num):
        self.data = pd.read_csv('catalog.csv')
        self.data.loc[self.data["amount"].loc[self.data["id"] == num].index,"amount"] = self.data["amount"] - 1
        self.data.to_csv("catalog.csv", index=False)         
          
     
          
          
          
        
# Add URL endpoints

api.add_resource(Info, '/info/<int:num>')
api.add_resource(Search, '/search/<string:topic>')
api.add_resource(Update, '/update/item_num/<int:num>')
api.add_resource(Update2, '/update2/item_num/<int:num>')
if __name__ == '__main__':
    app.run()
