# **SmartCart1**

SmartCart1 is a data scraping module designed to extract grocery product information directly from the Amazon Groceries website. It uses **BeautifulSoup** to parse HTML content, fetch product details such as names, prices, units, and availability, and stores the data for further processing.

---

## **What It Does**
- Scrapes grocery data, including:
  - Product names
  - Total prices
  - Price per unit
  - Unit measurements (e.g., lbs, oz)
  - Product availability
- Saves scraped data into a structured **CSV file** (`amazon_products1.csv`).
- Converts the CSV data into a **Pandas DataFrame** for further manipulation and analysis.
- Provides options to store the DataFrame into an **SQL database** for persistent storage.

---

## **How It Works**

### **1. Web Scraping**
- **Library Used**: BeautifulSoup (from the `bs4` package)
- **Description**:
  - Sends HTTP GET requests using the `requests` library.
  - Parses the HTML content of Amazon's grocery pages to extract relevant product details.
  - Handles navigation across multiple pages of product listings.
- **Limitations**:
  - Amazon may use dynamic content rendering or bot detection. For fully JavaScript-rendered pages, **Selenium** can be integrated as needed.

### **2. Data Handling with Pandas**
- **Library Used**: Pandas
- **Description**:
  - Converts the scraped data into a structured DataFrame for easier data analysis and manipulation.
  - The DataFrame is exported to a `CSV` file (`amazon_products1.csv`) for later use.

### **3. SQL Database Integration**
- **Purpose**:
  - Allows saving the DataFrame into an SQL database for efficient querying and analysis.
- **Supported Databases**:
  - SQLite
  - MySQL
  - PostgreSQL
- **Workflow**:
  - Use Pandas' `to_sql()` method to write the DataFrame directly into a database table.

---

## **Technical Notes**

### **Dependencies**
- **BeautifulSoup**: For scraping and parsing HTML content.
- **Requests**: For making HTTP requests.
- **Pandas**: For data manipulation and exporting to CSV or SQL.
- **SQLAlchemy (optional)**: For connecting Pandas with SQL databases.

Install dependencies with:
```bash
pip install -r requirements.txt
