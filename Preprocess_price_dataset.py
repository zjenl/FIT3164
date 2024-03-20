import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('sell_prices.csv')

# Filter out rows where wm_yr_wk > 11377
df = df[df['wm_yr_wk'] <= 11377]

# Pivot the df using pivot_table
pivot_df = df.pivot_table(index='item_id', columns='wm_yr_wk', values='sell_price',
                          aggfunc=lambda x: round(x.mean(), 2)).reset_index()

# Rename columns to remove 'wm_yr_wk' prefix
pivot_df.columns.name = None
pivot_df.columns = [str(col) if isinstance(col, int) else col for col in pivot_df.columns]

# Create dept_id column
pivot_df['dept_id'] = pivot_df['item_id'].str.split('_').str[:2].str.join('_')

# Reorder columns to put dept_id as the second column
pivot_df = pivot_df[['item_id', 'dept_id'] + [col for col in pivot_df.columns if col != 'item_id' and col != 'dept_id']]

# Calculate mean values for each dept_id
dept_mean = pivot_df.groupby('dept_id').mean().reset_index()

# Create a new DataFrame to store the mean values for each dept_id
new_df = pd.DataFrame(columns=pivot_df.columns)

# Iterate over dept_id and append rows to new_df
for dept_id in dept_mean['dept_id']:
    # Create a row with dept_id as item_id and mean values for other columns
    row = pd.Series({'item_id': dept_id})
    for col in pivot_df.columns:
        if col != 'item_id' and col != 'dept_id':
            row[col] = round(dept_mean.loc[dept_mean['dept_id'] == dept_id, col].values[0], 2)
        elif col == 'dept_id':
            row[col] = dept_id
            # Append the row to new_df
    new_df = new_df.append(row, ignore_index=True)

# Concatenate new_df with original DataFrame
final_df = pd.concat([pivot_df, new_df], ignore_index=True)

# Save the modified DataFrame to a new CSV file
final_df.to_csv('modified_price.csv', index=False)
