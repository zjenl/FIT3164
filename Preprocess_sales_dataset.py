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

# Calculate mean values for each dept_id
dept_mean = df.groupby('dept_id').mean().reset_index()

# Create a new DataFrame to store the mean values for each dept_id
new_df = pd.DataFrame(columns=df.columns)

# Iterate over dept_id and append rows to new_df
for dept_id in dept_mean['dept_id']:
    # Create a row with dept_id as item_id and mean values for other columns
    row = pd.Series({'item_id': dept_id})
    for col in df.columns:
        if col != 'item_id' and col != 'dept_id':
            row[col] = round(dept_mean.loc[dept_mean['dept_id'] == dept_id, col].values[0], 2)
        elif col == 'dept_id':
            row[col] = dept_id
            # Append the row to new_df
    new_df = new_df.append(row, ignore_index=True)

# Concatenate new_df with original DataFrame
final_df = pd.concat([df, new_df], ignore_index=True)

# Save the modified DataFrame to a new CSV file
final_df.to_csv('modified_sales.csv', index=False)


