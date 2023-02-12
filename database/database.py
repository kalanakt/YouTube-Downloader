import pymongo
from config import Config 

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

DATABASE_URI = Config.DATABASE_URI
DATABASE_NAME = Config.DATABASE_NAME

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

##################### sample data save, update and finding #####################

# more info: https://www.w3schools.com/python/python_mongodb_getstarted.asp

async def add_filter(chat_id, data):
    mycol = mydb["usersapites"]
    mydict = { "userid": str(chat_id), "data": str(data) }
    
    try:
        mycol.insert_one(mydict)
    except:
        logger.exception('Some error occured!', exc_info=True)
        
async def update_filter(chat_id, data):
    mycol = mydb["usersapites"]
    filter = { 'userid': str(chat_id) }
    newvalues = { "$set": { 'data': str(data) } }
    mycol.update_one(filter, newvalues)

async def find_filter(chat_id):
    mycol = mydb["usersapites"]
    myquery = { "userid": str(chat_id) }
    mydoc = mycol.find(myquery)
    for x in mydoc:
        return x
