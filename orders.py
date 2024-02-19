import json

import certifi
from bson import ObjectId
from pymongo import MongoClient

from main import connection_string

json_file_path = "orders.json"

# Connect to MongoDB
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client["OnlineStore"]
orders_collection = db["orders"]


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def insert_orders(orders):
    orders_collection.insert_many(orders)


if __name__ == "__main__":
    # 1 - Insert orders to MongoDB collection
    orders = read_json_file(json_file_path)
    insert_orders(orders=orders)
    print("Orders have been inserted into MongoDB.")

    # 2 - Display all orders stored in a MongoDB collection in JSON format
    all_orders = orders_collection.find({})
    orders_list = list(all_orders)
    json_output = json.dumps(orders_list, default=str, indent=4)
    print(json_output)

    # 3 - Query to find orders with total_sum greater than min_total_sum
    min_total_sum = 1000
    query = {"total_sum": {"$gt": min_total_sum}}
    orders = orders_collection.find(query)
    print(f"Query result: {[order for order in orders]}")

    # 4 - Query by customer's details
    customer_name = "John"
    customer_surname = "Doe"
    query = {"customer.name": customer_name, "customer.surname": customer_surname}
    orders = orders_collection.find(query)
    print(f"Query result: {[order for order in orders]}")

    # 5 - Specify the ObjectId(s) and find the orders
    item_ids_to_find = "65d37a70eef8738e96f6c2ff"
    query = {"items_id": item_ids_to_find}
    orders = orders_collection.find(query)
    print(f"Query result: {[order for order in orders]}")

    # 6 - Update orders with specific items
    item_id_to_find = "65d37a70eef8738e96f6c2ff"
    item_id_to_add = "65d37a70eef8738e96f6c2fd"
    increase_amount = 1200
    result = orders_collection.update_many(
        {"items_id": item_id_to_find},
        {"$push": {"items_id": item_id_to_add}, "$inc": {"total_sum": increase_amount}},
    )
    print(f"Orders updated: {result.modified_count}")

    # 7 - Get items quantity in specific order
    order_id = ObjectId("65d381a3bcc147c826341e44")
    order = orders_collection.find_one({"_id": order_id})
    number_of_items = len(order["items_id"])
    print(f"Items number: {number_of_items}")

    # 8 - Get specific order information
    min_total_cost = 1000
    query = {"total_sum": {"$gt": min_total_cost}}
    projection = {
        "_id": 0,  # Exclude the order ID from the results
        "customer": 1,
        "payment.cardId": 1,
    }
    orders = orders_collection.find(query, projection)
    print(f"Query result: {[order for order in orders]}")

    # 9 - Remove item in specific orders
    item_id_to_remove = "65d37a70eef8738e96f6c2ff"
    result = orders_collection.update_many(
        filter={
            "date": {"$gte": "2024-02-20T00:00:00Z", "$lte": "2024-02-25T23:59:59Z"}
        },
        update={"$pull": {"items_id": item_id_to_remove}},
    )
    print(f"Number of orders updated: {result.modified_count}")

    # 10 - Update surname in all orders
    result = orders_collection.update_many(
        {}, {"$set": {"customer.surname": "Shevchenko"}}
    )
    print(f"Number of orders updated: {result.modified_count}")

    # 11 - Joins
    customer_name = "John"
    customer_surname = "Doe"

    pipeline = [
        {
            "$match": {
                "customer.name": customer_name,
                "customer.surname": customer_surname,
            }
        },
        {"$unwind": "$items_id"},
        {
            "$lookup": {
                "from": "items",
                "localField": "items_id",
                "foreignField": "_id",
                "as": "item_details",
            }
        },
        {"$unwind": "$item_details"},
        {
            "$group": {
                "_id": "$_id",
                "customer": {"$first": "$customer"},
                "items": {
                    "$push": {
                        "name": "$item_details.name",
                        "price": "$item_details.price",
                    }
                },
            }
        },
        {"$project": {"_id": 0, "customer": 1, "items": 1}},
    ]
    # Execute the aggregation pipeline
    orders_with_items = db.orders.aggregate(pipeline)
    print(f"Query result: {[order for order in orders_with_items]}")
