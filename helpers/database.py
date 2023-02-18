from pymongo import MongoClient

# Replace <username>, <password>, and <cluster-name> with your own values
client = MongoClient(
    "mongodb+srv://ktu:9812@cluster0.up7nbkx.mongodb.net/?retryWrites=true&w=majority")
db = client.database
collection = db.utube_collection


def u_video(video_data, video):
    post = {"video_data": video_data, "video": video}
    result = collection.insert_one(post)
    # This will print the ID of the inserted document
    return result.inserted_id


def get_u_video(video_data):
    query = {"video_data": video_data}

    # Find documents with the given title
    results = collection.find(query)

    # Print the results
    for result in results:
        return result


def delete_u_video(video_data):
    query = {"video_data": video_data}
    collection.delete_one(query)
