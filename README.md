**# Vessel Booking Management System**

This is a Django-based web application for managing vessel bookings, vessels, marines, and users.

**## Prerequisites**

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- pip package manager
- PostgreSQL database (optional, you can use SQLite for development)

**## Installation**

1. **Clone the repository:**

   ```shell
   git clone https://github.com/your-username/your-project.git
   cd your-project/

1.1 **Create and activate a virtual environment (optional but recommended):**
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

2. **Install the project dependencies:**
  pip install -r requirements.txt

3. **Configure the database (SQLite is used by default):**
  python manage.py migrate
  If you want to use PostgreSQL, update the database settings in settings.py accordingly.

4. **Create a superuser account for administrative access:**
   python manage.py createsuperuser

5. **Start the development server:**
  python manage.py runserver

6. Access the application in your web browser at http://localhost:8000/.

7. **Usage:**
  Visit the admin panel at http://localhost:8000/admin/ to manage users, vessels, marines, and bookings.
  Users can log in and book vessels based on availability.

**Dependencies**
This project relies on the following Python packages:

asgiref==3.6.0
certifi==2022.12.7
charset-normalizer==3.1.0
Django==4.2
django-mathfilters==1.0.0
idna==3.4
Pillow==9.5.0
pytz==2023.3
requests==2.29.0
sqlparse==0.4.3
stripe==5.4.0
urllib3==1.26.15
utils==1.0.1
You can install them via pip as mentioned in the installation steps.

**Contributing**
Feel free to contribute to this project by opening issues or pull requests.


_________

E N J O Y
_________
