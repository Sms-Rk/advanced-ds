import pymongo

def handle(req):
    # Parse the request body and extract the data to be inserted into MongoDB
    data = req.decode('utf-8')
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://mongodb:27017/')
    # Access the 'test' database
    db = client['test']
    # Insert the data into the 'data' collection
    db.data.insert_one({'data': data})
    # Close the MongoDB connection
    client.close()
    # Return a success message
    return "Data inserted successfully"
