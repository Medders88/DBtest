from flask import Flask, request, json, Response
from pymongo import MongoClient

# initialising the Flask App, Python module for easy development of web applications.

app = Flask(__name__)

class CrudAPI: #MondoDB Model for Todo CRUD Implementations
    def _init_(self, data):  #Fetch the MongoDB, making use of the request body
        self.client = MongoClient("mongodb+srv://DMedlicott:WaZWb4cmZ09skuXm@testdm.n1a1r.mongodb.net/myFirstDatabase?retryWrites=true&w=majority/")
        database = data['database']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data


    def insert_data(self, data): #Create - (1)
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = { 'Status': 'Successfully Inserted',
                   'Document_ID': str(response.inserted_id)}
        return output

    def read(self): #read
        documents = self.collection.find()
        output = [{item:data[item] for item in data if item != '_id_'} for data in documents]
        return output

    def update_data(self): #update
        filter = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filter, updated_data)
        output = {'Status' : 'Succesfully Updated' if response.modified_count > 0 else "Nothing was updated"}
        return output

    def delete_data(self, data): #Delete
        filter = data['Filter']
        response = self.collection.delete_one(filter)
        output = {'Status' : 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output


    #CRUD thourhg API - '/curdapi'
                  
@app.route('/crudapi', methods=['POST']) #Update MongoDB Document, through API and METHOD - POST
def create():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400, mimetype='application/json')
    create_obj = CrudAPI(data)
    response = create_obj.insert_data(data)
    return Response(response=json.dumps(response), status=200,
                    mimetype='applcation/json')
                  

@app.route('/crudapi', methods=['PUT']) #Update MongoDB Document, through API and METHOD - PUT
def update():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400, mimetype='application/json')
    update_obj = CrudAPI(data)
    response = update_obj.update_data(data)
    return Response(response=json.dumps(response), status=200,
                    mimetype='applcation/json')


@app.route('/crudapi', methods=['DELETE']) #Delete MongoDB Document, through API and METHOD - DELETE
def delete():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400, mimetype='application/json')
    delete_obj = CrudAPI(data)
    response = delete_obj.delete_data(data)
    return Response(response=json.dumps(response), status=200,
                    mimetype='applcation/json')

if __name__=='__main__':
    app.run(debug=True, port=5000)

