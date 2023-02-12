<p align="center"><a href="https://thecodexo.com" target="_blank" rel="noopener noreferrer"><img width="250" src="https://github.com/kalanakt/Pyrogram-Telegram-Bot-Template/blob/main/pic/logo_transparent_1100x300.png" alt="Code xo logo"></a></p>

<h2>Thank you for using me 💖. Here are some examples of mongo db</h2>

<em>MongoDB is a document database with the scalability and flexibility that you want with the querying and indexing that you need</em>

<h3>Create a collection called "users"</h3>
<em>you should import pymongo library and <strong>DATABASE URL</strong></em>
<br><br>

```
import pymongo
from config import Config 

DATABASE_URI = Config.DATABASE_URI
DATABASE_NAME = Config.DATABASE_NAME

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

mycol = mydb["users"]

```

<h3>Insert Into Collection</h3>
<em>Adding new user to "users" database</em>

```

import pymongo
from config import Config 

DATABASE_URI = Config.DATABASE_URI
DATABASE_NAME = Config.DATABASE_NAME

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

mycol = mydb["users"]

mydict = { "name": "John", "userid": "76035" }

x = mycol.insert_one(mydict)

```

<h3>Filter the Result</h3>
<em>Find User from "users" database.</em>

```

import pymongo
from config import Config 

DATABASE_URI = Config.DATABASE_URI
DATABASE_NAME = Config.DATABASE_NAME

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

mycol = mydb["users"]

myquery = { "name": "katy" }

mydoc = mycol.find(myquery)

for x in mydoc:
  return x
  
```

<h3>Delete Document</h3>
<em>Delete User from "users" database.</em>

```

import pymongo
from config import Config 

DATABASE_URI = Config.DATABASE_URI
DATABASE_NAME = Config.DATABASE_NAME

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

mycol = mydb["users"]

myquery = { "name": "milly" }

mycol.delete_one(myquery) 

```

<h3>Update Collection</h3>
<em>Update User Details from "users" database.</em>

```

import pymongo
from config import Config 

DATABASE_URI = Config.DATABASE_URI
DATABASE_NAME = Config.DATABASE_NAME

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

mycol = mydb["users"]

myquery = { "name": "jhon" }
newvalues = { "$set": { "userid": "01335" } }

mycol.update_one(myquery, newvalues)

```

<p>For More Information Visit <a href="https://www.w3schools.com/python/python_mongodb_getstarted.asp">w3schools mongodb lession</a>
