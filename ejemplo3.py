import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

print(df)
# Loop through all columns using items()
for col_name, col_data in df.items():
    print(f"Column name: {col_name}")
    print(col_data) # col_data is a pandas Series
    # Perform operations on the column data
    print(f"Mean of column {col_name}: {col_data.mean()}")
