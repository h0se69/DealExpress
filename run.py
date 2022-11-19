from DealExpress import create_app

flaskObj = create_app()
flaskObj.run(debug=True, port=8000)