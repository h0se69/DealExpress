from flask import render_template, Blueprint
#from DealExpress import flaskObj

@routes.route('/', methods=["GET"])
def homePage():
    return render_template("home.html")

#Change return_template html later 
@routes.route('/searchResults', methods=['GET', 'POST'])
def searchResults():
    return render_template('home.html', title='Search Results')

#Change return_template html later 
@routes.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('home.html', title='Login')

#Change return_template html later
@routes.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    return render_template('home.html', title='Create Account')

#individual item page
@routes.route('/itemPage', methods=['GET', 'POST'])
def searchPage():
    return render_template('specified_Item.html', title='Item')