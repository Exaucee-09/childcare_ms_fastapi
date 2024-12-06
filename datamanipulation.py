import requests
import dask.dataframe as dd
import pandas as pd

BASE_URL = 'http://localhost:8000'

# Fetch data and save it temporarily as CSV (to process large data in chunks using Dask)
def fetch_data(endpoint, filename):
    try:
        response = requests.get(f'{BASE_URL}/{endpoint}')
        response.raise_for_status()
        data = response.json()
        # Save as CSV for Dask to process in chunks
        df = pd.DataFrame(data if isinstance(data, list) else data[endpoint])
        df.to_csv(filename, index=False)
        print(f"Fetched and saved {endpoint} data to {filename}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint} data: {e}")

# Fetch data from APIs and save to CSV
fetch_data('children', 'children.csv')
fetch_data('attendance', 'attendance.csv')

# Load the CSV files using Dask
children_ddf = dd.read_csv('children.csv')
attendance_ddf = dd.read_csv('attendance.csv')

# Merge data
merged_ddf = dd.merge(
    attendance_ddf,
    children_ddf,
    how='inner',
    left_on='child_id',
    right_on='id'
)

# Drop duplicates
merged_ddf = merged_ddf.drop_duplicates()

# Fill missing values
merged_ddf = merged_ddf.fillna({
    'status': 'absent',
    'name': 'Unknown',
    'age': 0,
    'classroom': 'N/A'
})

# Handle problematic columns: Ensure all types are consistent
for column in merged_ddf.columns:
    if merged_ddf[column].map_partitions(lambda x: x.apply(type)).eq(dict).any().compute():
        print(f"Column '{column}' contains dictionaries, converting to string.")
        merged_ddf[column] = merged_ddf[column].astype(str)

# Convert age to integer
merged_ddf['age'] = merged_ddf['age'].astype(int)

# Add a column to indicate if the child is a minor
merged_ddf['is_minor'] = merged_ddf['age'] < 18

# Add attendance_score column
merged_ddf['attendance_score'] = merged_ddf['status'].apply(
    lambda x: 10 if x == 'present' else 0,
    meta=('status', 'int')
)

# Rename column
merged_ddf = merged_ddf.rename(columns={'name': 'child_name'})

# Drop 'classroom' column
merged_ddf = merged_ddf.drop(columns=['classroom'])

# Save the processed data to a single CSV
output_file = 'processed_children_attendance_dask.csv'
merged_ddf.to_csv(output_file, single_file=True, index=False)
print(f"\nData successfully saved into '{output_file}'.")

# Additional Analysis
print("\nData Analysis:")

# Group by 'status' and count occurrences
status_counts = merged_ddf.groupby('status').size().compute()
print("\nStatus Counts:")
print(status_counts)

# Group by 'classroom' and calculate average age
if 'classroom' in merged_ddf.columns:  # Check in case the column was dropped
    average_age = merged_ddf.groupby('classroom')['age'].mean().compute()
    print("\nAverage Age by Classroom:")
    print(average_age)

# Sorting data by age in descending order
sorted_ddf = merged_ddf.nlargest(5, 'age', compute=True)
print("\nTop 5 Oldest Children:")
print(sorted_ddf.compute())

# Filtering rows for minors
minors_ddf = merged_ddf[merged_ddf['is_minor']]
print("\nFiltered Minors Data:")
print(minors_ddf.head().compute())
