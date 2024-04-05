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

    for day_col in day_cols:
        day_index = day_cols.index(day_col)

        for _, price_row in price_df_cat.iterrows():
            price = price_row[day_col]

            if pd.notnull(price):
                sales_row = sales_df_cat[sales_df_cat['item_id'] == price_row['item_id']]
                if sales_row.empty:
                    continue

                sales = sales_row.iloc[0][day_col]

                if pd.notnull(sales):
                    previous_prices = [price_row[day_cols[day_index - i]]
                                       if day_index - i >= 0 and pd.notnull(price_row[day_cols[day_index - i]])
                                       else 0
                                       for i in range(7, -1, -1)]

                    # Check if 6 or more values in previous_prices are 0
                    if previous_prices.count(0) < 6:
                        # Append the sales change at the end
                        previous_prices.append(sales)

                        combined_rows.append(previous_prices)

    # Now, convert combined_rows into a DataFrame with appropriate column names
    column_names = ['7_days_ago', '6_days_ago', '5_days_ago', '4_days_ago', '3_days_ago', '2_days_ago', '1_days_ago',
                    '0_days_ago', 'sales_change']
    combined_df = pd.DataFrame(combined_rows, columns=column_names)

    # Save to CSV
    combined_df.to_csv(f'{dept}.csv', index=False)
