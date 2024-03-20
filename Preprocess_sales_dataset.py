import pandas as pd

df = pd.read_csv('M5_preprocessed/sales_train_evaluation.csv')

# We want to convert the sales volume from daily to weekly to match the price change
# First we will drop unnecessary columns
columns_to_remove = ['id', 'cat_id', 'store_id', 'state_id', 'd_1940', 'd_1941']
df.drop(columns=columns_to_remove, inplace=True)

# Calculate the sum of every 7 days and store them in new columns
for i in range(11101, 11354):
    start_col = 'd_' + str((i - 11101) * 7 + 1)
    end_col = 'd_' + str((i - 11101) * 7 + 7)
    df[str(i)] = df.loc[:, start_col:end_col].sum(axis=1)

# Drop the original day columns
df.drop(df.columns[2:1941], axis=1, inplace=True)

# Write the modified DataFrame to a new CSV file
df.to_csv('modified_sales.csv', index=False)

