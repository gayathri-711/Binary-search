# DS Mini Project (Python/Flask)

This workspace was converted to a minimal Flask-based Python project that serves the existing `index.html` and `student.html` and exposes a small JSON REST API for student records stored in `student_data.json`.

Quick start (Windows, cmd.exe):

1. Create a virtual environment and activate it:

```
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the app:

```
python app.py
```

Open http://127.0.0.1:5000/ in your browser. The `index.html` and `student.html` in the workspace root will be served.

API endpoints:
- GET  /api/students          -> list students
- POST /api/students          -> create student {name, age, grade}
- GET  /api/students/<id>     -> retrieve single student
- PUT  /api/students/<id>     -> update fields {name, age, grade}
- DELETE /api/students/<id>   -> delete student

Notes:
- The server uses a simple file `student_data.json` for persistence. For production, replace with a proper DB.
- For testing, you can override the data file by setting the `STUDENT_DATA_FILE` environment variable before running, e.g. `set STUDENT_DATA_FILE=C:\temp\mydata.json`.

Running tests:

```
# inside activated venv
pip install -r requirements.txt
python -m pytest -q
```

Docker (optional)
-----------------

You can run the app in Docker Desktop. The container will read/write the data file at `/data/student_data.json`; the provided `docker-compose.yml` binds it to the project file `./student_data.json` so data persists between container restarts.

Build and run with docker-compose (recommended):

```cmd
docker compose up --build -d
```

Or build and run with plain docker:

```cmd
docker build -t ds-mini-project .
docker run -p 5000:5000 -e STUDENT_DATA_FILE=/data/student_data.json -v %cd%\student_data.json:/data/student_data.json ds-mini-project
```

Then open http://127.0.0.1:5000/ in your browser. To stop the compose stack:

```cmd
docker compose down
```

Notes:
- If `student_data.json` does not exist on the host before starting, docker-compose will create an empty file but ensure your host directory is writable by Docker Desktop.
- For production use replace the builtin server with a WSGI server (gunicorn) and secure the deployment.
