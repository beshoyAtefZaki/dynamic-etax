import os
import requests
import threading
import time
import sqlite3

def run_server():
    os.system("python manage.py runserver")
    print("+ running")