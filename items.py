import json
import certifi
from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
connection_string = "mongodb+srv://tina:WestCoast0608@cluster0.5okimuc.mongodb.net/"

json_file_path = "items.json"

# Connect to MongoDB
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client["OnlineStore"]
collection = db["e-commerce"]


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def insert_products(items):
    collection.insert_many(items)


if __name__ == "__main__":
    # 1 - Insert items to MongoDB collection
    products = read_json_file(json_file_path)
    insert_products(products)
    print("Products have been inserted into MongoDB.")

    # 2 - Display all products stored in a MongoDB collection in JSON format
    all_products = collection.find({})
    products_list = list(all_products)
    json_output = json.dumps(products_list, default=str, indent=4)
    print(json_output)

    # 3 - Count the number of products in the specified category
    category_to_count = "Smartphone"
    count = collection.count_documents({"category": category_to_count})
    print(f"There are {count} products in the category '{category_to_count}'.")

    # 4 - Count the number of unique categories
    unique_categories = collection.distinct("category")
    number_of_unique_categories = len(unique_categories)
    print(f"There are {number_of_unique_categories} unique items categories.")

    # 5 - Find all unique producers
    unique_producers = collection.distinct("producer")
    print(f"List of unique producers: {[producer for producer in unique_producers]}")

    # 6 Query products by category and price range
    category = "Smartphone"
    price_range = {"$gte": 500, "$lte": 1000}
    query_and = {"$and": [{"category": category}, {"price": price_range}]}
    products = collection.find(query_and)
    print(f"Query result: {[product for product in products]}")

    query_or = {"$or": [{"model": "iPhone 14 Pro"}, {"model": "iPhone 15 Pro"}]}
    products = collection.find(query_or)
    print(f"Query result: {[product for product in products]}")

    producers = ["Asus", "LG"]
    query_in = {"producer": {"$in": producers}}
    products = collection.find(query_in)
    print(f"Query result: {[product for product in products]}")

    # 7 - Update
    criteria = {"category": "Smartphone"}
    update_changes = {"$set": {"inStock": "true"}, "$inc": {"price": 50}}
    collection.update_many(criteria, update_changes)
    print("Products updated successfully.")

    # 8 - Query to find products with the 'inStock' field
    query = {"inStock": {"$exists": True}}
    products_in_stock = collection.find(query)
    print(f"Query result: {[product for product in products_in_stock]}")

    # 9 - Update operation to increase the price
    query = {"inStock": {"$exists": True}}
    update_operation = {"$inc": {"price": 200}}
    collection.update_many(query, update_operation)
    print("Updated prices for products with 'inStock' field.")
