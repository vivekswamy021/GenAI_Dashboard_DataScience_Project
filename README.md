# Restaurant Management Dashboard

This is a Streamlit-based dashboard for visualizing and analyzing restaurant management data. The dashboard reads data from a CSV file (`test_data.csv`), processes it, and presents various insights related to restaurant sales, staff performance, and item popularity.

## Prerequisites

Before running the code, ensure you have the required Python libraries installed. You can do this by running the following command:

```bash

pip install -r requirements.txt

```

## Running the Dashboard

To run the dashboard, execute the script `restaurant_management_dashboard.py`. The dashboard will be accessible in your web browser.

```bash

streamlit run restaurant_management_dashboard.py

```

## Overview

The Restaurant Management Dashboard provides the following insights:

1\. **Total Sales and Monthly Sales:**

   - Select a month to view the total sale for that month.

   - Visualize monthly sales for each food/drink item.

2\. **Category-wise Analysis:**

   - Select a category to view the total sale for that category.

   - Visualize daily sales for the selected category by day of the week.

3\. **Staff Performance:**

   - Minimum serve time for each drinks staff and kitchen staff.

   - Visualize the minimum serve time for each staff in the menu.

4\. **Top 5 Most Sold Items:**

   - View the top 5 most sold food and drink items.

5\. **Category Distribution:**

   - Pie charts displaying the distribution of food and drink items by category.

## Data Processing

The dashboard processes the provided CSV data (`test_data.csv`) by extracting date, hour, minute, and other relevant information from the 'Order_Time' column. It also formats the 'Serve_Time' column for better readability.

## Usage

- Select options from dropdowns to filter data and view specific insights.

- Interactive charts provide a dynamic view of the data.

- The dashboard offers a user-friendly interface for exploring restaurant management metrics.

Check out the Restaurant Management Dashboard!

<img width="1815" height="884" alt="Screenshot 2025-10-13 134241" src="https://github.com/user-attachments/assets/4fb9a13d-9d9c-49a6-a2b8-0d959a48a5ad" />
