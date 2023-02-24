import logging

# Application
ENV = 'development'
HOST = '0.0.0.0'
PORT = 906
SECRET_KEY = b'\xd1\x91\xf4\x84\xc2\xfa\x97\xd4f\xaa\xec\xae\x93\xb1ev\x84S\xf7\x93D{\xd5\t'

# Logger
LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setLevel('DEBUG')
LOG_HANDLER.setFormatter(logging.Formatter('[%(asctime)s] - %(levelname)s - %(lineno)d - %(filename)s - %(message)s'))

# SQLAlchemy
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_SIZE = 300
# SQLALCHEMY_POOL_RECYCLE       = 600
