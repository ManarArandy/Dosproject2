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
  


          
        
# Add URL endpoints

api.add_resource(Info, '/info/<int:num>')


if __name__ == '__main__':
    app.run()
