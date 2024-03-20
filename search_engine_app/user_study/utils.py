import os
import random
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

## Save a record to MongoDB * @param {Object} record - The record to save * @returns {string} - The _id of the new document 
def save_record_to_mongo(record):
    # Create a client
    mongo_server = os.getenv("MONGO_SERVER")
    mongo_database = os.getenv("USER_STUDY_MONGO_DATABASE")
    mongo_collection = os.getenv("USER_STUDY_MONGO_COLLECTION")

    client = MongoClient(mongo_server)
    # Connect to your database
    db = client[mongo_database]
    # Choose the collection
    collection = db[mongo_collection]

    # Insert the record into the collection
    result = collection.insert_one(record)

    # Print the _id of the new document
    return result.inserted_id

## Assign one condition to a user
def assign_user_condition():
    num_conditions = int(os.getenv("NUMBER_OF_CONDITIONS"))
    condition = random.randint(1, num_conditions)
    return condition
    