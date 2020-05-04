
# For this project

import os
# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
PROJECT_ROOT = os.path.dirname(__file__)
DRIVER_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'driver'))
DRIVER_NAME = "chromedriver.exe"
DRIVER_FILE = os.path.abspath(os.path.join(DRIVER_DIR, DRIVER_NAME))
