from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pymysql
import re
import spacy
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use("Agg")
# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


@app.route('/')
def home():
    return "WhatsApp Expense Tracker is Running!"


# MySQL Database Connection
db = pymysql.connect(
    host="host_name",
    user="username",
    password="password",
    database="db_name",
)
cursor = db.cursor()

# ✅ Table Schema (Run this in MySQL once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50),
    amount FLOAT,
    category VARCHAR(50),
    merchant VARCHAR(100),
    description TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
db.commit()


# ✅ NLP-Based Expense Extraction
def extract_expense(message):
    doc = nlp(message)
    amount, category, merchant = None, "Other", "Unknown"

    # 🔍 Extract amount using regex (handles ₹, Rs, rupees, etc.)
    amount_match = re.search(r"(?:₹|Rs\.?|rupees)?\s?(\d+)", message,
                             re.IGNORECASE)
    if amount_match:
        amount = float(amount_match.group(1))

    # 🔍 Define common categories
    categories = {
        "food": [
            "coffee", "snacks", "dinner", "lunch", "biryani", "food",
            "restaurant", "pizza", "burger", "pasta", "sushi", "fries",
            "noodles", "dosa", "ice cream", "milkshake", "tea", "cake",
            "muffin", "sandwich", "biscuit", "pav bhaji", "momos", "shawarma",
            "idli", "paratha", "rolls", "chicken", "paneer", "butter naan",
            "soft drink", "cold drink", "beverage"
        ],
        "travel": [
            "uber", "ola", "train", "bus", "taxi", "flight", "cab", "auto",
            "metro", "tram", "airline", "indigo", "air india", "go first",
            "spicejet", "emirates", "qatar airways", "visa", "passport",
            "travel insurance", "hotel booking", "resort", "airbnb", "hostel"
        ],
        "shopping": [
            "jeans", "clothes", "shoes", "electronics", "amazon", "flipkart",
            "blinkit", "nykaa", "myntra", "snapdeal", "t-shirt", "jacket",
            "watch", "earbuds", "mobile", "laptop", "tablet", "headphones",
            "fashion", "makeup", "skincare", "perfume", "wallet", "handbag",
            "sunglasses", "sportswear", "decathlon", "footwear", "home decor",
            "furniture"
        ],
        "groceries": [
            "grocery", "zepto", "bigbasket", "blinkit", "supermarket", "milk",
            "bread", "butter", "vegetables", "fruits", "cheese", "yogurt",
            "rice", "dal", "atta", "sugar", "salt", "spices", "biscuits",
            "oil", "chocolate", "dry fruits", "tea powder", "coffee beans",
            "soft drinks", "frozen food"
        ],
        "entertainment": [
            "netflix", "amazon prime", "hotstar", "spotify", "youtube premium",
            "theater", "movies", "concert", "stand-up comedy", "gaming",
            "steam", "playstation", "xbox", "board games", "escape room",
            "theme park", "amusement park", "cricket match", "football match",
            "book fair"
        ],
        "healthcare": [
            "doctor", "dentist", "hospital", "medicines", "pharmacy", "apollo",
            "medlife", "1mg", "blood test", "x-ray", "ct scan", "mri",
            "surgery", "vaccination", "first aid", "protein powder",
            "gym supplements", "fitness"
        ],
        "fitness": [
            "gym", "yoga", "zumba", "running shoes", "treadmill", "dumbbells",
            "protein shake", "fitness band", "sports equipment",
            "gym membership", "cycling", "swimming", "football", "cricket bat",
            "badminton racket"
        ],
        "education": [
            "books", "notebooks", "pens", "pencils", "coaching", "tuition",
            "online courses", "udemy", "coursera", "byjus", "unacademy",
            "chegg", "subscription", "library", "kindle", "school fees",
            "college fees", "stationery", "whiteboard", "backpack"
        ],
        "utilities": [
            "electricity bill", "water bill", "gas bill", "wifi", "broadband",
            "jio", "airtel", "vi", "bsnl", "dth", "recharge", "postpaid",
            "prepaid", "mobile bill", "loan emi", "insurance", "house rent",
            "maintenance", "property tax"
        ],
        "subscriptions": [
            "spotify", "apple music", "youtube premium", "newspaper",
            "magazine", "gym membership", "amazon prime", "hotstar", "disney+",
            "hbo max", "zee5", "playstation plus", "xbox game pass", "vpn",
            "notion premium", "cloud storage"
        ],
        "electronics": [
            "mobile", "laptop", "desktop", "mouse", "keyboard", "headphones",
            "earbuds", "power bank", "smartwatch", "tv", "tablet", "printer",
            "router", "gaming console", "ssd", "hard disk", "graphics card",
            "motherboard", "processor", "monitor"
        ],
        "home_appliances": [
            "washing machine", "refrigerator", "air conditioner", "microwave",
            "vacuum cleaner", "geyser", "dishwasher", "toaster", "iron",
            "hair dryer", "kitchen appliances", "smart home devices", "fan",
            "cooler", "heater"
        ],
        "automobile": [
            "car service", "bike service", "fuel", "petrol", "diesel", "cng",
            "car accessories", "tyres", "engine oil", "car insurance",
            "road tax", "driving license", "car wash", "helmet", "bike helmet",
            "seat cover"
        ],
        "pet_care": [
            "dog food", "cat food", "pet grooming", "veterinary",
            "pet hospital", "pet training", "pet accessories", "dog collar",
            "cat litter", "bird food", "aquarium", "fish food", "dog leash",
            "rabbit food", "hamster cage"
        ],
        "gifts": [
            "gift", "birthday gift", "anniversary gift", "wedding gift",
            "flowers", "chocolates", "gift card", "amazon gift card", "watch",
            "jewelry", "perfume", "handbag", "wallet", "photo frame",
            "greeting card"
        ],
        "investment": [
            "stocks", "mutual funds", "crypto", "bitcoin", "ethereum", "nft",
            "gold", "silver", "real estate", "ipo", "trading", "forex",
            "bonds", "index funds", "sip", "fixed deposit",
            "recurring deposit", "property"
        ]
    }

    # 🔍 Assign category based on keywords
    for cat, keywords in categories.items():
        if any(word in message.lower() for word in keywords):
            category = cat
            break

    # 🔍 Extract merchant name (Proper nouns)
    for token in doc:
        if token.pos_ == "PROPN":
            merchant = token.text

    return amount, category, merchant



# ✅ Twilio WhatsApp Webhook
@app.route("/webhook", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").lower()
    user_id = request.values.get("From")

    resp = MessagingResponse()
    reply = resp.message()

    # 🔹 Extract Expense
    amount, category, merchant = extract_expense(incoming_msg)

    if amount:
        print(
            f"DEBUG: Extracted Amount={amount}, Category={category}, Merchant={merchant}"
        )

        # ✅ Store in MySQL
        cursor.execute(
            "INSERT INTO expenses1 (user_id, amount, category, merchant, description) VALUES (%s, %s, %s, %s, %s)",
            (user_id, amount, category, merchant, incoming_msg),
        )
        db.commit()

        reply.body(
            f"✅ Expense of ₹{amount} at {merchant} added under '{category}' category!"
        )

    # 🔍 Handle Queries
    elif "how much" in incoming_msg or "total" in incoming_msg:
        if "coffee" in incoming_msg:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses1 WHERE user_id=%s AND category='food'",
                (user_id, ))
        elif "travel" in incoming_msg:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses1 WHERE user_id=%s AND category='travel'",
                (user_id, ))
        elif "food" in incoming_msg:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses1 WHERE user_id=%s AND category='food'",
                (user_id, ))
        elif "groceries" in incoming_msg:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses1 WHERE user_id=%s AND category='groceries'",
                (user_id, ))
        else:
            cursor.execute(
                "SELECT SUM(amount) FROM expenses1 WHERE user_id=%s",
                (user_id, ))

        total = cursor.fetchone()[0] or 0
        reply.body(f"💰 Your total expenses so far: ₹{total}")

    

    # 📢 Custom Alerts
    elif "alert" in incoming_msg:
        match = re.search(r"(\d+)",
                          incoming_msg)  # Extract budget amount safely

        if match:
            budget = float(match.group(1))
        else:
            reply.body(
                "⚠️ Please provide a valid budget amount in your alert message."
            )
            return str(resp)  # Exit early to prevent errors

        # Fetch total spent from the database
        cursor.execute("SELECT SUM(amount) FROM expenses1 WHERE user_id=%s",
                       (user_id, ))
        total_spent = cursor.fetchone()[0] or 0  # Prevents NoneType error

        # Compare with budget
        if total_spent > budget:
            reply.body(
                f"⚠️ Alert: You've exceeded your budget of ₹{budget}! Your total spending: ₹{total_spent}"
            )
        else:
            reply.body(
                f"✅ You're within budget! (Spent: ₹{total_spent} / Budget: ₹{budget})"
            )

    # Default response
    else:
        reply.body(
            "💬 Send me your expenses like: 'Spent 200 on coffee at Starbucks' or ask 'How much did I spend on travel?'"
        )

    return str(resp)


# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
