import json
import os
from datetime import datetime

DataBase = "data.json"

def load_data():
    if not os.path.exists(DataBase):
        return []
    with open(DataBase, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DataBase, "w") as file:
        json.dump(data, file, indent=4)

def add_transaction(amount, trans_type, category):
    data = load_data()

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
    data = load_data()
    data = [item for item in data if item["id"] != trans_id]
    save_data(data)

def update_transaction(trans_id, amount, trans_type, category):
    data = load_data()
    for item in data:
        if item["id"] == trans_id:
            item["amount"] = float(amount)
            item["type"] = trans_type
            item["category"] = category
            break
    save_data(data)

def get_balance():
    data = load_data()
    income = sum(item["amount"] for item in data if item["type"] == "Income")
    expense = sum(item["amount"] for item in data if item["type"] == "Expense")
    return income, expense, income - expense

def get_category_summary():
    data = load_data()
    summary = {}
    for item in data:
        if item["type"] == "Expense":
            cat = item["category"]
            summary[cat] = summary.get(cat, 0) + item["amount"]
    return summary