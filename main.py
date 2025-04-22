import os
import pandas as pd
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
import re
from collections import defaultdict

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, "finances_example_export.csv")

# Initialize MCP
mcp = FastMCP("ProfessionalFinanceTracker")

# Financial data
data = {}
monthly_budget = 5000.0
categories = [
    "Food", "Coffee", "Dining", "Transport", "Rent", "Utilities",
    "Entertainment", "Shopping", "Electronics", "Healthcare",
    "Fitness", "Education", "Travel", "Groceries", "Savings"
]
expense_sources = {
    "Food": ["Whole Foods", "Trader Joe's", "Local market", "Costco"],
    "Coffee": ["Starbucks", "Blue Bottle", "Peet's Coffee", "Local cafe"],
    "Dining": ["Restaurant", "Food delivery", "Lunch break", "Business dinner"],
    "Transport": ["Uber", "Lyft", "Public transit", "Gas station", "Car maintenance"],
    "Entertainment": ["Cinema", "Concert", "Theater", "Streaming service"],
    "Shopping": ["Amazon", "Target", "Mall", "Department store"],
    "Electronics": ["Apple Store", "Best Buy", "B&H Photo", "Online tech store"],
    "Healthcare": ["Pharmacy", "Doctor visit", "Therapy session"],
    "Fitness": ["Gym membership", "Yoga studio", "Sports equipment"],
    "Groceries": ["Supermarket", "Farmer's market", "Online grocery"],
    "Travel": ["Airline tickets", "Hotel booking", "Vacation package"]
}

# Load CSV
def load_data_from_csv(file_path=CSV_FILE_PATH):
    global data
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    df = pd.read_csv(file_path)
    for month in df['month'].unique():
        month_data = df[df['month'] == month]
        data[month] = {"income": [], "expenses": []}
        for _, row in month_data[month_data['type'] == 'income'].iterrows():
            data[month]["income"].append({"source": row['category'], "amount": float(row['amount'])})
        for _, row in month_data[month_data['type'] == 'expense'].iterrows():
            data[month]["expenses"].append({
                "category": row['category'], "amount": float(row['amount']),
                "source": row['source'], "date": row['date'], "description": row['description']
            })

load_data_from_csv()

# Helpers
def current_month():
    return datetime.now().strftime("%Y-%m")

def previous_month():
    return (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

# MCP Tools
@mcp.tool()
def query_expenses(month: str = "") -> dict:
    """Query total expenses for a given month with a breakdown by category."""
    target_month = month or current_month()
    if month.lower() in ["last month", "previous month"]:
        target_month = previous_month()
    expenses = data.get(target_month, {}).get("expenses", [])
    total = sum(expense["amount"] for expense in expenses)
    category_breakdown = {}
    for expense in expenses:
        category = expense["category"]
        if category not in category_breakdown:
            category_breakdown[category] = {"total": 0.0, "expenses": []}
        category_breakdown[category]["total"] += expense["amount"]
        category_breakdown[category]["expenses"].append({
            "amount": expense["amount"],
            "source": expense["source"],
            "date": expense["date"],
            "description": expense["description"]
        })
    return {
        "month": target_month,
        "total_expenses": round(total, 2),
        "category_breakdown": {
            cat: {
                "total": round(info["total"], 2),
                "expenses": info["expenses"]
            } for cat, info in category_breakdown.items()
        }
    }

@mcp.tool()
def add_expense(description: str, date: str = "") -> dict:
    """Add an expense from a description (e.g., 'I just spent $10 on ice cream') with an optional date (YYYY-MM-DD).
       Extracts amount, categorizes the expense, and adds it to the data structure."""
    amount_match = re.search(r'\$?(\d+(?:\.\d+)?)', description)
    if not amount_match:
        return {"error": "Could not parse amount"}
    amount = float(amount_match.group(1))
    category = next((cat for cat in categories if cat.lower() in description.lower()), "Miscellaneous")
    source = None
    for cat, sources in expense_sources.items():
        for src in sources:
            if src.lower() in description.lower():
                source = src
                category = cat if category == "Miscellaneous" else category
                break
        if source:
            break
    source = source or "Unknown"
    month = current_month()
    expense_date = date or f"{month}-{datetime.now().day:02d}"
    if month not in data:
        data[month] = {"expenses": []}
    expense = {
        "category": category,
        "amount": amount,
        "source": source,
        "date": expense_date,
        "description": description
    }
    data[month]["expenses"].append(expense)
    return {
        "status": "success",
        "message": f"Added ${amount:.2f} expense for {category} at {source} on {expense_date}",
        "expense": expense
    }

@mcp.tool()
def budget_status(month: str = "") -> dict:
    """Query the remaining budget for a given month by subtracting total expenses from the monthly budget."""
    global monthly_budget
    target_month = month or current_month()
    if month.lower() in ["last month", "previous month"]:
        target_month = previous_month()
    expenses = data.get(target_month, {}).get("expenses", [])
    total_expenses = sum(expense["amount"] for expense in expenses)
    remaining = monthly_budget - total_expenses
    return {
        "month": target_month,
        "budget": monthly_budget,
        "total_expenses": round(total_expenses, 2),
        "remaining": round(remaining, 2)
    }

if __name__ == "__main__":
    mcp.run()