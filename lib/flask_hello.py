class FlaskHello:
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def hello(self):
        print('hello world')
        return self
