#This file failed because of large amounts of data that had to be retrieved and I used dask in the datamanipulation.py file

import requests
import pandas as pd

#This is to fetch data from 2 different APIs, merging them, manipulating them and saving data to csv file
BASE_URL = 'http://localhost:8000'

def fetch_data(endpoint):
    try:
        response = requests.get(f'{BASE_URL}/{endpoint}')
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data if isinstance(data, list) else data[endpoint])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint} data: {e}")
        return pd.DataFrame()

children_df = fetch_data('children')
attendance_df = fetch_data('attendance')

if not children_df.empty and not attendance_df.empty:

    merged_df = pd.merge(attendance_df, children_df, how='inner', left_on='child_id', right_on='id')
    merged_df.drop_duplicates(inplace=True)
    merged_df.fillna({
        'status': 'absent',
        'name': 'Unknown',
        'age': 0,
        'classroom': 'N/A'
    }, inplace=True)
    print("Merged Data:")
    print(merged_df.head())

    # Check for problematic columns and handle them
    for column in merged_df.columns:
        if merged_df[column].map(type).eq(dict).any():
            print(f"Column '{column}' contains dictionaries, converting to string.")
            merged_df[column] = merged_df[column].apply(str)

    merged_df['age'] = merged_df['age'].astype(int)

    merged_df['is_minor'] = merged_df['age'].apply(lambda x: 1 if x < 18 else 0)

    merged_df.to_csv('processed_children_attendance.csv', index=False)
    print("\nData successfully saved into 'processed_children_attendance.csv'.")

    # Display DataFrame information
    print("\nDataFrame Information:")
    print(merged_df.info())

    # Display basic statistics
    print("\nDataFrame Description:")
    print(merged_df.describe())

    # Shape of DataFrame
    print("\nDataFrame Shape:", merged_df.shape)

    # Selecting a specific column
    print("\nSelected 'name' Column:")
    print(merged_df['name'].head())

    # Filtering rows based on a condition
    minors_df = merged_df[merged_df['is_minor'] == 1]
    print("\nFiltered Minors Data:")
    print(minors_df.head())

    #Group by 'status and calculate the count
    status_counts = merged_df.groupby('status').size()
    print("\nStatus Counts:")
    print(status_counts)

    #Group by classroom and calculate average age
    average_age = merged_df.groupby('classroom')['age'].mean()
    print("\nAverage Age by Classroom:")
    print(average_age)

    #Sorting data by age in descending order
    sorted_df = merged_df.sort_values(by='age', ascending=False)
    print("\nSorted Data:")
    print(sorted_df.head())

    #Adding attendance_score column
    merged_df['attendance_score'] = merged_df['status'].apply(lambda x:10 if x=='present' else 0)
    print("\nData with 'attendance_score' column:")
    print(merged_df.head())

    #Renaming a column
    merged_df.rename(columns={'name': 'child_name'}, inplace=True) #using inplace=True allows modification of dataframe directly without creating a copy
    print("\nData with 'rename' column:")
    print(merged_df.head())

    # Removing (dropping) a column
    merged_df.drop(columns=['classroom'], inplace=True)
    print("\nDataFrame after dropping 'classroom' column:")
    print(merged_df.head())

else:
    print("Failed to fetch data or received empty data.")

