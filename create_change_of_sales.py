import pandas as pd
import numpy as np

df = pd.read_csv('modified_sales.csv')

# Calculate percentage change for each column (sale of a product of the day)
percent_change_df = df.iloc[:, 2:].pct_change(axis=1) * 100
percent_change_df = percent_change_df.round(2)

# Replace inf values with 1
percent_change_df.replace([np.inf], 100, inplace=True)

# Concatenate the first two string columns with the percent_change_df
final_df = pd.concat([df.iloc[:, :2], percent_change_df], axis=1)
final_df.to_csv('percent_change_sale.csv', index=False)
