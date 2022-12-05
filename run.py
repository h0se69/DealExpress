from DealExpress import create_app
from flask_login import LoginManager


flaskObj = create_app()


flaskObj.run(debug=True, port=8000) 