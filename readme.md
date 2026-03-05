# Blogsite FastAPI

A fast, modern, and lightweight blog website built with FastAPI to help users create, read, and manage blog posts with a clean, template-driven interface.

## 🚀 Features

* **API Routing (`main.py`)**: Clean and robust endpoint routing for handling blog operations and page views.
* **Database Management (`database.py`, `models.py`)**: Structured relational data management utilizing SQLAlchemy ORM.
* **Data Validation (`schemas.py`)**: Secure data validation and serialization handling using Pydantic models.
* **Frontend Rendering (`templates/`, `static/`)**: Server-side rendering fully integrated with Jinja2 templates and custom CSS styling.

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI
* **Database**: SQLAlchemy ORM
* **Frontend**: HTML5, CSS3, Jinja2 Templating

## 📂 Project Structure

```text
blogsite-fastapi/
├── static/              # CSS, JavaScript, and static image files
├── templates/           # Jinja2 HTML templates for frontend rendering
├── database.py          # Database connection, session management, and engine setup
├── main.py              # Application entry point, API routes, and view endpoints
├── models.py            # SQLAlchemy database models (tables)
├── schemas.py           # Pydantic models for data validation and serialization
├── requirements.txt     # Python project dependencies
├── .gitignore           # Git ignore rules
└── .DS_Store            # macOS directory attributes
⚙️ Local Setup and Installation
Clone the repository:

Bash
git clone [https://github.com/abdurakhmanovjohn/blogsite-fastapi.git](https://github.com/abdurakhmanovjohn/blogsite-fastapi.git)
cd blogsite-fastapi
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Run the development server:

Bash
uvicorn main:app --reload
The application will be available at http://127.0.0.1:8000/. You can also access the interactive API documentation at http://127.0.0.1:8000/docs.