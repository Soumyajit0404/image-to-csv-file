import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('recognized_text.csv')

df.to_csv('recognized_text.txt', index=False, header=True, sep='\t')

print("DataFrame saved to recognized_text.txt")
