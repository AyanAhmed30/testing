import os
import sys
import ee
import google.auth.exceptions
from google.auth.transport.requests import Request

# Function to initialize GEE
def initialize_gee():
    service = os.getenv('SA')
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'djangoGEE', 'gee', 'ee-muzzamil1-37ebc3dece52.json')
    print(f"Using GEE credentials file at: {file}")  # Debugging line

    if not os.path.exists(file):
        print(f"Error: The file {file} does not exist.")
        return

    credentials = ee.ServiceAccountCredentials(service, file)
    try:
        ee.Initialize(credentials)
        print("GEE Initialized successfully")
    except google.auth.exceptions.RefreshError as e:
        # If the token has expired, refresh it
        request = Request()
        credentials.refresh(request)
        ee.Initialize(credentials)
        print("GEE Initialized after refreshing credentials")

def inv():
    initialize_gee()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoGEE.settings")

    # Ensure the project path is added to sys.path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'djangoGEE'))

    # Initialize GEE or refresh the token before executing Django commands
    inv()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
