from flask import render_template
from DealExpress import flaskObj

#home page
@flaskObj.route('/', methods=["GET"])
def homePage():
    return render_template("home.html")

#Change return_template html later 
@flaskObj.route('/searchResults', methods=['GET', 'POST'])
def searchResults():
    return render_template('home.html', title='Search Results')

#Change return_template html later 
@flaskObj.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('home.html', title='Login')

#Change return_template html later
@flaskObj.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    return render_template('home.html', title='Create Account')

#individual item page
@flaskObj.route('/itemPage', methods=['GET', 'POST'])
def searchPage():
    return render_template('specified_Item.html', title='Item')