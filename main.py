from flask import Flask

from app import create_app

app = create_app()

if __name__ == '__main__':
    Flask.run(app, host=app.config['HOST'], port=app.config['PORT'], debug=True, threaded=True)
