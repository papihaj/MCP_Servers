# Professional Finance Tracker

The **Professional Finance Tracker** is a Python-based financial management tool that uses the `FastMCP` server framework and `pandas` to track expenses, categorize spending, and monitor budgets. It processes financial data from a CSV file and provides a server-based interface for querying expenses, adding new expenses, and checking budget status.

## Features

- **Load Financial Data**: Imports income and expense data from a CSV file (`finances_example_export.csv`).
- **Expense Tracking**: Add expenses with automatic categorization and source detection from natural language descriptions (e.g., "I spent $10 on ice cream").
- **Budget Monitoring**: View monthly budget, total expenses, and remaining funds.
- **Expense Queries**: Retrieve detailed expense breakdowns by category for a specific month.
- **Predefined Categories**: Supports categories like Food, Transport, and Entertainment, with associated sources (e.g., Starbucks, Uber).
- **Server Interface**: Powered by `FastMCP` for interactive financial data management.

## Requirements

- Python 3.8+
- Required packages:
  - `pandas`
  - `fastmcp` (custom or proprietary library for MCP server)
- A CSV file (`finances_example_export.csv`) with columns:
  - `month` (e.g., `2023-01`)
  - `type` (`income` or `expense`)
  - `category` (e.g., Food, Rent)
  - `amount` (numeric)
  - `source` (e.g., Starbucks)
  - `date` (e.g., `2023-01-15`)
  - `description` (transaction details)

## Installation

1. **Clone the Repository** (if applicable):

   ```bash
   git clone <repository-url>
   cd professional-finance-tracker
   ```

2. **Install Dependencies**: Use `uv` to install required packages:

   ```bash
   uv pip install pandas
   ```

   Note: Ensure `fastmcp` is available in your environment. If unavailable, contact the project maintainer or adapt the code for another server framework.

3. **Prepare the CSV File**: Place `finances_example_export.csv` in the script's directory, ensuring it matches the required format.

4. **Run the Application**: Start the server:

   ```bash
   python finance_tracker.py
   ```

## Usage

The application provides three main tools via the `FastMCP` server:

1. **Query Expenses** (`query_expenses(month: str = "")`):

   - Retrieves total expenses and category breakdowns for a specified month (or current month).

   - Example:

     ```python
     result = query_expenses("2023-01")
     ```

     Output:

     ```json
     {
         "month": "2023-01",
         "total_expenses": 1500.50,
         "category_breakdown": {
             "Food": {"total": 300.00, "expenses": [...]},
             "Transport": {"total": 200.50, "expenses": [...]}
         }
     }
     ```

2. **Add Expense** (`add_expense(description: str, date: str = "")`):

   - Adds an expense by parsing a description and optional date, with automatic categorization.

   - Example:

     ```python
     result = add_expense("Spent $10 on ice cream at Trader Joe's", "2023-01-15")
     ```

     Output:

     ```json
     {
         "status": "success",
         "message": "Added $10.00 expense for Food at Trader Joe's on 2023-01-15",
         "expense": {...}
     }
     ```

3. **Budget Status** (`budget_status(month: str = "")`):

   - Shows budget, total expenses, and remaining funds for a specified month.

   - Example:

     ```python
     result = budget_status("2023-01")
     ```

     Output:

     ```json
     {
         "month": "2023-01",
         "budget": 5000.0,
         "total_expenses": 1500.50,
         "remaining": 3499.50
     }
     ```

## Configuration

- **Monthly Budget**: Default is `$5000.0`. Edit `monthly_budget` in the script to change.
- **Categories and Sources**: Predefined in `categories` and `expense_sources`. Modify these variables to customize.
- **CSV File Path**: Defaults to `finances_example_export.csv` in the script's directory. Update `CSV_FILE_PATH` if needed.

## Example CSV Format

```csv
month,type,category,amount,source,date,description
2023-01,income,Salary,6000.00,Employer,2023-01-01,January salary
2023-01,expense,Food,50.00,Whole Foods,2023-01-02,Groceries
2023-01,expense,Transport,20.00,Uber,2023-01-03,Ride to work
```

## Notes

- `FastMCP` is assumed to be a custom library. If unavailable, consider using Flask or FastAPI as alternatives.
- Descriptions must include a clear amount (e.g., "$10" or "10 dollars") for parsing.
- Validate CSV structure to avoid errors.
- For large datasets, monitor memory usage and optimize `pandas` operations.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

MIT License. See `LICENSE` for details.

## Contact

For support, open an issue on the repository or contact me.
