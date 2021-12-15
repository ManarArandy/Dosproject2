from flask import Flask
from flask_restful import Api, Resource
import requests
from flask_caching import Cache

app = Flask(__name__)
api = Api(app)
#Cache
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
#-----------------------

chacheSize = 0
myArray = [None] * 50
index=0
 
catalogFlag = 1

class Search(Resource):

    @cache.memoize(50)
    def get(self, topic):

        global chacheSize
        global myArray
        global index
        global catalogFlag

        itemfound = cache.get(topic)
        if itemfound:
            return {'The item exist in the cache': itemfound},200
        else:
            if(catalogFlag):
                #Server A (Windows)
                catalogFlag = 0
                result =requests.get('http://172.16.96.99:5000/search/'+str(topic)).json() 
                cache.set(topic, result)
            else:
                #Server B (Ubuntu)
                catalogFlag = 1
                result =requests.get('http://172.16.96.104:5000/search/'+str(topic)).json()
                cache.set(topic, result)
        myArray[chacheSize] = topic
        chacheSize = chacheSize + 1

        if chacheSize > 4:
            cache.delete(myArray[index])
            index= index+1

        if(catalogFlag):
           return {'From Server B': result}
        else:  
           return {'From Server A': result}


class Info(Resource):

    @cache.memoize(50)
    def get(self, num):
        global chacheSize
        global myArray
        global index
        global catalogFlag

        itemfound = cache.get(str(num))
        if itemfound:
            return {'The item exist in the cache': itemfound},200
        else:
            if(catalogFlag):
                #Server A (Windows)
                catalogFlag = 0
                result =requests.get('http://172.16.96.99:5000/info/'+str(num)).json() 
                cache.set(str(num), result)
            else:
                #Server B (Ubuntu)
                catalogFlag = 1
                result =requests.get('http://172.16.96.104:5000/info/'+str(num)).json()
                cache.set(str(num), result)

        myArray[chacheSize] = str(num)
        chacheSize = chacheSize + 1

        if chacheSize> 4:
            cache.delete(myArray[index])
            index= index+1
        if(catalogFlag):
           return {'From Server B': result}
        else:  
           return {'From Server A': result}


api.add_resource(Search, '/search/<string:topic>')
api.add_resource(Info, '/info/<int:num>')


if __name__ == '__main__':
    app.run()
