Backend Engineer Assessment — Test Data API

This project is a local backend HTTP API built using Python, Flask, and SQLite.
It provides endpoints to ingest and retrieve medical test data

>Manual input validation
?Raw SQL usage 
>Explicit transaction handling
>Structured logging
>Failure handling and consistency



Tech Stack
Language = Python (simple and readable)
Framework = Flask (lightweight and minimal for APIs)
Database  = SQLite (file based DB , for local development)
APIs = Postman

Project Structure
-app.py
-database.py
-logger.py
-README.md

How to Run Project
install dependencies- pip install flask
run the server - python app.py
server starts at - http://127.0.0.1:5000

POST/tests - create a new test record
Requested Body
{
  "test_id": "t1",
  "patient_id": "p1",
  "clinic_id": "c1",
  "test_type": "CBC",
  "result": "Normal"
}

Success Response (201)
{
  "status": "success",
  "test_id": "t1"
}

Duplicate Response(409)
{
  "status": "error",
  "message": "test_id already exists"
}

GET/tests?clinic_id=c1 - fetch all tests belonging to a clinic

Design Decision
-Flask was chosen because:
lightweight and minimal framework
perfect for small local APIs

Duplicate handling - option A 
Reject duplicates with HTTP 409 Conflict
prevents data overwrites
maintains strong data integrity

All input validation is performed manually:
JSON body must exist and be valid
all fields are required
all fields must be non-empty strings

All database write operation use explicit transactions:
BEGIN
COMMIT on success
ROLLBACK on failure

Potential failure
INPUT = missing or invalid JSON
DATABASE = DB corruption
DUPLICATE IDs = unique constraint violation
QUERY ERROR = missing clinic_id parameter

Debugging
-to debug inconsistent data:
1 inspect structured logs
2 verify commits/rollbacks
3 query SQLite database directly
4 validate duplicate handling and input validation

Production changes
MySQL/PostgreSQL = handles many users and supports scaling
Centralized logging = monitoring dashboards
ADD Security = Authorization and Security checks

