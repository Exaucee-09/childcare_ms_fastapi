# Childcare Management System

This is a Childcare Management System built using **FastAPI**. It supports CRUD operations for managing children, staff, and attendance records. Additionally, it includes functionality to process large datasets efficiently using **Dask**.

## Features
- REST API for managing childcare data (CRUD operations for children, staff, and attendance).
- Efficient processing of large datasets using `Dask`.
- Integration with CSV files for external data processing.
- Example script (`datamerge.py`) demonstrating data merging and manipulation.

## Project Structure
```plaintext
childcare-management-system/
├── app/                     # FastAPI application
│   ├── main.py              # Entry point of the FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── datageneration.py    # generating a vast amount of data at once
│   ├── database.py          # Database connection
│   ├── routers/             # API routes
│   ├── children.csv         # Example CSV file for children data
│   ├── attendance.csv       # Example CSV file for attendance data
│   └── datamanipulation.py  # Script for merging and analyzing data
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignore rules

```
## Requirements
- Python 3.8+
- FastAPI
- Dask
- Pandas
- Requests
- SQLAlchemy
- Uvicorn


## Installation and Setup
1. Clone the Repository
```bash
- git clone https://github.com/Exaucee-09/childcare-ms_fastapi
- cd childcare_ms_fastapi
```
2. Set Up a Virtual Environment
```bash
- python -m venv env
- source env/bin/activate  # On Windows: env\Scripts\activate
```
3. Install Dependencies
```bash
- pip install -r requirements.txt
```
4. Run the FastAPI Application
```bash
- uvicorn app.main:app --reload
- The API will be available at: http://127.0.0.1:8000
```

## API Documentation
FastAPI provides interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Working with the datamerge.py Script

## Scripts used

### Data splitting and merging script ***csvdata.py***
This script demonstrates how to fetch data from a local API, split it into separate files, and then merge the data back together.

#### Description
The script performs the following tasks:

- Fetches data from a local API endpoint (http://localhost:8000/children).
- Converts the received JSON data into a pandas DataFrame.
- Splits the DataFrame into two parts:
- Part 1: Contains the id and name columns.
- Part 2: Contains the classroom and age columns.
- Saves the split DataFrames into two CSV files (children_part1.csv and children_part2.csv).
- Loads the two CSV files back into DataFrames.
- Combines the loaded DataFrames into a single DataFrame.
- Saves the combined DataFrame into a final CSV file (children_combined.csv).

### Data Processing Script Overview ***datamanipulation.py***
This script retrieves data from two APIs, processes it, and saves the results to a CSV file. It utilizes Dask for handling large datasets efficiently, ensuring scalability for data-intensive operations.

#### Below are the key functionalities:

- ***API Data Retrieval***: Retrieves data from children and attendance endpoints and saves it temporarily as CSV files.

- ***Data Processing with Dask***:  Loads the CSV files using Dask, which enables handling large datasets in a memory-efficient manner.

- ***Data cleaning and Transformation***:
- Merges the data on common identifiers (child_id and id).
- Drops duplicate records and fills missing values with default placeholders.
- Converts problematic columns into consistent types (e.g., handling dictionaries as strings).
- Adds new columns, such as is_minor (indicating if a child is under 18) and attendance_score (based on attendance status).
- Ensures numerical consistency for age and adds an is_minor flag.
- Renames and drops specific columns to refine the dataset.

- ***Data Analysis and manipulation***:
- Performs group-based analysis, such as counting attendance statuses and calculating average age by classroom.
- Filters data to identify minors and sorts the data by age in descending order.

**Output:** Saves the processed data to a CSV file (processed_children_attendance.csv) for further use and analysis and also attendance.csv and children.csv.
**Note**: attendance.csv and process_children_attendance_dask.csv were not pushed on github because they are too large

## Example API Endpoints
1. Create a Child
```bash
Endpoint: POST /children/
Request:
{
  "name": "John Doe",
  "age": 5,
  "classroom": "A1"
}
```
2. Get All Children
```bash
Endpoint: GET /children/
```
3. Record Attendance
```bash
Endpoint: POST /attendance/
Request:
{
  "child_id": 1,
  "date": "2024-12-06",
  "status": "present"
}
```
## Example Script Output
When running the datamerge.py script:

- Processed data will be saved as processed_children_attendance_dask.csv.

Sample output displayed in the terminal:
```bash
Merged Data:
   child_id      date   status       name  age classroom  is_minor
0         1 2024-12-06  present  John Doe    5       A1         1
1         2 2024-12-06  absent   Jane Doe   10       B2         1
```
## Contributing
Contributions are welcome!
To contribute:

- Fork the repository.
- Create a feature branch.
- Submit a pull request.

## Author
Developed by Peace Exaucee
