import os
import traceback

from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from lib.framework import Flask
from app.exception import APIException, ServerError

from sqlalchemy.exc import DatabaseError

env = os.environ.get('ENV', 'development')


def create_app():
    app = Flask(__name__)

    # load config
    app.config.from_object('config.base')
    app.config.from_object(f'config.{env}')

    # set logger config
    app.logger.removeHandler(app.logger.handlers[0])
    app.logger.addHandler(app.config['LOG_HANDLER'])

    # register blueprints
    from app.system import bp as system_bp

    app.register_blueprint(system_bp)

    # register plugins
    from .plugin import db

    db.init_app(app)
    Migrate(app, db)

    # register hooks
    @app.errorhandler(Exception)
    def framework_error(e):
        app.logger.error(traceback.format_exc())

        if isinstance(e, APIException):
            return e
        elif isinstance(e, HTTPException):
            print('asd')
            return APIException(code=e.code, msg=e.description)
        elif isinstance(e, DatabaseError):
            app.logger.error('SQLAlchemy出错')
            db.session.rollback()
            return ServerError()
        else:
            if app.config['DEBUG']:
                raise e from None
            else:
                app.logger.error('UNKNOWN ERROR')
                return ServerError(msg='UNKNOWN ERROR')

    app.logger.info('=' * 30)
    app.logger.info(f'CURRENT ENV：{env}')
    app.logger.info('=' * 30)

    return app
