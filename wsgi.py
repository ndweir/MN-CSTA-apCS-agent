import sys

# Add your project directory to the Python path
path = '/home/MNcodecoach/mysite'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask application
from app import app as application

if __name__ == '__main__':
    application.run()
