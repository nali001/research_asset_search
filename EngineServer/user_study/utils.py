import os
import random
import json
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
def assign_user_condition(userId):
    current_location = os.path.dirname(os.path.abspath(__file__))
    tasks = [json.loads(_) for _ in open(os.path.join(current_location, "target_search_tasks.jsonl")).readlines()]
    num_tasks = len(tasks)
    num_conditions = 2
    mongo_server = os.getenv("MONGO_SERVER")
    mongo_database = os.getenv("USER_STUDY_MONGO_DATABASE")
    mongo_collection = os.getenv("USER_STUDY_MONGO_COLLECTION")

    # check this user's records, whether s/he has already taken a test.
    client = MongoClient(mongo_server)
    # Connect to your database
    db = client[mongo_database]
    # Choose the collection
    collection = db[mongo_collection]

    # Find the records of this user
    # record is in the format: {'userId': 'abc', 'taskId': 1, 'taskQuestion': 'remote sensing', 'condition': 0}
    # condition 0: control, 1: treatment (with context entity from notebooks/datasets)
    records = collection.find({'userId': userId})
    records = [_ for _ in records]

    condition = -1
    task_taken = set([])
    if len(records) > 0:
        # The user has already taken a test
        tested_conditions = set([record['condition'] for record in records])
        task_taken = set([record['taskId'] for record in records])
        if len(tested_conditions) == num_conditions:
            # already took all the tests
            condition = -1
        else:
            # assign a new condition            
            condition =  random.choice(list(set(range(num_conditions)).difference(tested_conditions)))
    else:
        # The user has not taken any test
        condition = random.randint(0, num_conditions - 1)

    
    # Assign a task to the user
    task_id = random.choice(list(set([_['task_id'] for _ in tasks]).difference(task_taken)))
    task = [_ for _ in tasks if _['task_id'] == task_id][0]['task_question']
    return condition, task_id, task
    