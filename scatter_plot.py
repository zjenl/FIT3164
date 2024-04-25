import pandas as pd
import matplotlib.pyplot as plt
import os


def remove_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    return data[(data >= (Q1 - 1.5 * IQR)) & (data <= (Q3 + 1.5 * IQR))]

# Get the current directory
directory = os.getcwd()

# List of CSV files in the directory starting with 'H' or 'F'
csv_files = [file for file in os.listdir(directory) if
             file.endswith('.csv') and (file.startswith('H') or file.startswith('F'))]

# Loop through each CSV file
for file in csv_files:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(directory, file))

    # Extract the second last and last columns from the DataFrame
    x_values = df.iloc[:, -2]  # Second last column
    y_values = df.iloc[:, -1]  # Last column

    y_values_no_outliers = remove_outliers(y_values)
    x_values_no_outliers = x_values[y_values_no_outliers.index]

    # Plot the scatter plot
    plt.scatter(x_values_no_outliers, y_values_no_outliers)
    plt.xlabel('% change in price')
    plt.ylabel('% change in sales')
    plt.title(file)  # Add filename to the title
    plt.show()
