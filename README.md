# Device Tracking API

A Django-based REST API project for tracking devices.

## Features

- User registration and authentication with JWT
- Device management and tracking
- API filtering and search with django-filter and Django REST framework
- Sending emails for registration and notifications

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/khimani-yug/device_tracking.git
    cd device_tracking
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```
    python manage.py migrate
    ```

5. Run the development server:
    ```
    python manage.py runserver
    ```

## Usage

- Access the API endpoints via `http://127.0.0.1:8000/api/`
- Use token-based JWT authentication for secure access

## Contributing

Feel free to fork this project and create pull requests.

## License

Specify your license here (e.g., MIT).

---

**Note:** Update and customize this README with more specific project and API details as you continue development.
