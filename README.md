# 📊 WhatsApp Expense Tracker Bot

## 📌 Overview
The **WhatsApp Expense Tracker Bot** helps users manage expenses via WhatsApp messages. It extracts expense details using **NLP (SpaCy)**, stores transactions in **MySQL**, and sends budget alerts when spending exceeds a set limit.

## 🚀 Features
- ✅ **Expense Logging**: Extracts amount, category, and merchant details from messages.
- 📊 **Expense Summary**: Retrieves total and category-wise spending.
- 🔔 **Custom Budget Alerts**: Notifies users when they exceed their set budget.
- 📈 **Graphical Reports**: Generates spending insights using Matplotlib.
- 💾 **Database Storage**: Uses MySQL to store expenses for future analysis.
- 🔄 **Twilio Integration**: Automates WhatsApp responses.

## 🛠️ Tech Stack
- **Python** (Flask, SpaCy, Matplotlib, Twilio API)
- **MySQL** (Expense storage)
- **Regex & NLP** (Entity extraction)
- **Replit** (Deployment environment)

## 📦 Installation
```sh
# Clone the repository
git clone https://github.com/yourusername/whatsapp-expense-tracker.git
cd whatsapp-expense-tracker

# Install dependencies
pip install -r requirements.txt

# Set up MySQL database
CREATE DATABASE expenses_db;
USE expenses_db;
CREATE TABLE expenses1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    amount FLOAT,
    category VARCHAR(255),
    merchant VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

# Set environment variables (Twilio credentials, DB config)
export TWILIO_ACCOUNT_SID='your_sid'
export TWILIO_AUTH_TOKEN='your_token'
export TWILIO_PHONE_NUMBER='your_twilio_number'
export MYSQL_HOST='your_host'
export MYSQL_USER='your_user'
export MYSQL_PASSWORD='your_password'
export MYSQL_DB='expenses_db'

# Run the Flask app
python main.py
```

## 🎯 Usage
- **Add an expense:** Send a message like `Spent ₹500 on food at McDonald's`.
- **Check total spending:** Send `summary`.
- **Set budget alert:** Send `alert ₹3000`.
- **Get spending report:** Send `report`.

## 🔥 Example Interactions
📌 **User:** `Spent ₹200 on groceries at Big Bazaar`
📌 **Bot:** `✅ Logged: ₹200 for groceries at Big Bazaar.`

📌 **User:** `alert ₹5000`
📌 **Bot:** `✅ Budget alert set at ₹5000.`

📌 **User:** `summary`
📌 **Bot:** `📊 Total Spent: ₹1200 | Food: ₹600 | Transport: ₹300 | Other: ₹300`

## 🛠️ Issues & Debugging
- **Error: `NoneType` object has no attribute `group`**
  - Ensure your message contains a valid number (e.g., `alert ₹3000`).
- **500 Internal Server Error on webhook**
  - Check Twilio webhook URL configuration.
  - Verify database connectivity.

## 🎯 Future Enhancements
- 📅 **Expense Trends**: Monthly analytics & visualization.
- 🔍 **OCR Integration**: Extract expenses from receipts.
- 🛒 **Auto-Categorization**: AI-powered spending classification.
- 📤 **CSV Export**: Download expense reports.

## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Pull requests are welcome! Feel free to submit issues or feature requests.

---
🔗 **Connect with me:** [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername) 🚀

