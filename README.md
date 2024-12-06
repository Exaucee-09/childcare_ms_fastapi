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
- 1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/childcare-management-system.git
cd childcare-management-system
- 2. Set Up a Virtual Environment
bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
- 3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
- 4. Run the FastAPI Application
bash
Copy code
uvicorn app.main:app --reload
The API will be available at: http://127.0.0.1:8000

## API Documentation
FastAPI provides interactive API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Working with the datamerge.py Script
The datamerge.py script processes large datasets using Dask. It fetches data from the FastAPI application and CSV files for merging and manipulation.

## Input Data
Ensure the FastAPI server is running.
Place the children.csv and attendance.csv files in the data/ directory.

- Running the Script
Run the script from the terminal:
bash
Copy code
python data/datamerge.py

## Features in the Script
- Merges data from children and attendance APIs.
- Handles missing values using default values.
- Adds computed columns like is_minor and attendance_score.
- Saves processed data to processed_children_attendance_dask.csv.

## Example API Endpoints
- 1. Create a Child
Endpoint: POST /children/
Request:

json
Copy code
{
  "name": "John Doe",
  "age": 5,
  "classroom": "A1"
}
- 2. Get All Children
Endpoint: GET /children/

- 3. Record Attendance
Endpoint: POST /attendance/
Request:

json
Copy code
{
  "child_id": 1,
  "date": "2024-12-06",
  "status": "present"
}

## Example Script Output
When running the datamerge.py script:

Processed data will be saved as processed_children_attendance_dask.csv.
Sample output displayed in the terminal:
plaintext
Copy code
Merged Data:
   child_id      date   status       name  age classroom  is_minor
0         1 2024-12-06  present  John Doe    5       A1         1
1         2 2024-12-06  absent   Jane Doe   10       B2         1

## Contributing
Contributions are welcome!
To contribute:

- Fork the repository.
- Create a feature branch.
- Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Author
Developed by Peace Exaucee
