import json
import certifi
from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
connection_string = 'mongodb+srv://tina:WestCoast0608@cluster0.5okimuc.mongodb.net/'

json_file_path = 'items.json'

# Connect to MongoDB
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client['OnlineStore']
collection = db['e-commerce']


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def insert_products(items):
    collection.insert_many(items)


if __name__ == "__main__":
    p = 'test'
    # 1 - insert items to MongoDB collection
    # products = read_json_file(json_file_path)
    # insert_products(products)
    # print("Products have been inserted into MongoDB.")

    # 2 - display all products stored in a MongoDB collection in JSON format
    all_products = collection.find({})
    products_list = list(all_products)
    json_output = json.dumps(products_list, default=str, indent=4)
    print(json_output)
