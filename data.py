import json
import os
from datetime import datetime

FILE_NAME = "data.json"

def load_data():
    """Loads transactions from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_data(data):
    """Saves the transaction list to the JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

def add_transaction(amount, trans_type, category):
    """Creates a new transaction and saves it."""
    data = load_data()
    # Generate a simple ID based on the highest existing ID
    new_id = max([item.get('id', 0) for item in data], default=0) + 1
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    new_record = {
        "id": new_id,
        "amount": float(amount),
        "type": trans_type,
        "category": category,
        "date": date_str
    }
    data.append(new_record)
    save_data(data)

def delete_transaction(trans_id):
    """Deletes a transaction by ID."""
    data = load_data()
    data = [item for item in data if item["id"] != trans_id]
    save_data(data)

def update_transaction(trans_id, amount, trans_type, category):
    """Updates an existing transaction."""
    data = load_data()
    for item in data:
        if item["id"] == trans_id:
            item["amount"] = float(amount)
            item["type"] = trans_type
            item["category"] = category
            # We keep the original date
            break
    save_data(data)

def get_balance():
    """Calculates Total Income, Total Expense, and Net Balance."""
    data = load_data()
    income = sum(item["amount"] for item in data if item["type"] == "Income")
    expense = sum(item["amount"] for item in data if item["type"] == "Expense")
    return income, expense, income - expense

def get_category_summary():
    """Returns a dictionary of total expenses per category."""
    data = load_data()
    summary = {}
    for item in data:
        if item["type"] == "Expense":
            cat = item["category"]
            summary[cat] = summary.get(cat, 0) + item["amount"]
    return summary