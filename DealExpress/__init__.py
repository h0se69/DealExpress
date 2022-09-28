from flask import Flask
import sqlite3

flaskObj = Flask(__name__)

# Init Database
# 
# 
# 
# 

from DealExpress import routes
from DealExpress.APIs import *