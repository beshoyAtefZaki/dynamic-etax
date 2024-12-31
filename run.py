import os
import requests
import threading
import time
import sqlite3

def run_server():
    os.system("python manage.py runserver 8005")
    print("+ running")


run_server()