import requests
import pandas as pd

#This is the first assignment to split data into files and then merge the files
try:
    response = requests.get('http://localhost:8000/children')
    response.raise_for_status()
    data = response.json()

    children_df = pd.DataFrame(data)

    print("DataFrame shape:", children_df.shape)
    print(children_df)

    children_df_part1 = children_df[['id', 'name']]
    children_df_part2 = children_df[['classroom', 'age']]

    children_df_part1.to_csv('children_part1.csv', index=False)
    children_df_part2.to_csv('children_part2.csv', index=False)

    df_part1_loaded = pd.read_csv('children_part1.csv')
    df_part2_loaded = pd.read_csv('children_part2.csv')

    data_df_combined = pd.concat([df_part1_loaded, df_part2_loaded], axis=1)
    print("\nCombined DataFrame:")
    print(data_df_combined.head())

    data_df_combined.to_csv('children_combined.csv', index=False)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
