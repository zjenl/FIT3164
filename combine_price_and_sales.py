import pandas as pd

price_change_df = pd.read_csv('percent_change_price.csv')
sales_change_df = pd.read_csv('percent_change_sale.csv')

# Ensure day columns are interpreted as strings
price_change_df.columns = price_change_df.columns.astype(str)
sales_change_df.columns = sales_change_df.columns.astype(str)

# Get a list of unique departments
departments = price_change_df['dept_id'].unique()

for dept in departments:
    combined_rows = []  # This will store the combined rows of % price and % sales change

    # Filter data for the current category
    price_df_cat = price_change_df[price_change_df['dept_id'] == dept]
    sales_df_cat = sales_change_df[sales_change_df['dept_id'] == dept]

    day_cols = [col for col in price_df_cat if col.startswith('1')]

    # For each day, match up % price and % sales change, excluding nulls
    for day_col in day_cols:
        for _, price_row in price_df_cat.iterrows():
            price = price_row[day_col]

            if pd.notnull(price) and price != 0:
                # Find corresponding sales change
                sales_row = sales_df_cat[sales_df_cat['item_id'] == price_row['item_id']]
                if sales_row.empty:
                    continue  # Skip if no matching item_id in sales data

                sales = sales_row.iloc[0][day_col]

                # Exclude rows with null values
                if pd.notnull(sales):
                    combined_rows.append([price, sales])

    # Create a DataFrame for the combined data
    combined_df = pd.DataFrame(combined_rows, columns=['price_change', 'sales_change'])

    # Save to CSV
    combined_df.to_csv(f'{dept}.csv', index=False)
