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
        res = dataFrame.to_json(orient="records")
    
        # return data found in csv
        return json.loads(res),200 
  
  
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

          
          
          
     
          
          
          
        
# Add URL endpoints

api.add_resource(Info, '/info/<int:num>')
api.add_resource(Search, '/search/<string:topic>')

if __name__ == '__main__':
    app.run()
