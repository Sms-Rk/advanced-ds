import os
from pymongo import MongoClient
from urllib.parse import quote_plus

def get_uri():
    #password=""
    #with open("/var/openfaas/secrets/mongo-db-password") as f:
    #    password = f.read()

    return "mongodb://%s:%s@%s" % (
    quote_plus("root"), quote_plus("9TlJZ7I5Lt"), os.getenv("mongo_host"))

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    uri = get_uri()
    client = MongoClient(uri)

    db = client['openfaas']

    followers = db.followers
    follower={"username": "Sms-Rk"}
    res = followers.insert_one(follower)

    return "Record inserted: {}".format(res.inserted_id)