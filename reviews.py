import certifi
from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
connection_string = "mongodb+srv://tina:WestCoast0608@cluster0.5okimuc.mongodb.net/"

# Connect to MongoDB
client = MongoClient(connection_string, tlsCAFile=certifi.where())
db = client["OnlineStore"]

db.create_collection("reviews", capped=True, size=5242880, max=5)

review = {
    "customerName": "John Doe",
    "rating": 5,
    "comment": "Great service and products!",
    "date": "2024-02-20",
}

db.reviews.insert_one(review)

for i in range(6, 11):
    review = {
        "customerName": f"Customer {i}",
        "rating": i % 5 + 1,
        "comment": f"Comment number {i}",
        "date": f"2024-02-{i}",
    }
    db.reviews.insert_one(review)

if __name__ == "__main__":
    all_reviews = db.reviews.find()
    for review in all_reviews:
        print(review)
