import pandas as pd

df = pd.read_csv('modified_price.csv')

# Calculate percentage change for each column (price of a product of the day)
percent_change_df = df.iloc[:, 2:].pct_change(axis=1) * 100
percent_change_df = percent_change_df.round(2)

# Percentage of price changes
percent_change_df['fluctuation'] = (percent_change_df.notna().sum(axis=1)-(percent_change_df == 0).sum(axis=1))/253*100
percent_change_df['fluctuation'] = percent_change_df['fluctuation'].round(2)

# Concatenate the first two string columns with the percent_change_df
final_df = pd.concat([df.iloc[:, :2], percent_change_df], axis=1)

# Save the modified DataFrame to a new CSV file
final_df.to_csv('percent_change_price.csv', index=False)
