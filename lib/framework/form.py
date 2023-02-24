from flask import request
from wtforms import Form

from app.exception import ParameterError


class BaseForm(Form):
    LANGUAGES = ['zh']

    def __init__(self, user_data=None):
        if not user_data:
            data = request.get_json(silent=True) or {}
        else:
            data = user_data

        args = request.args.to_dict()
        data.update(args)

        super().__init__(data=data, **args)

    def validate_for_api(self):
        valid = super().validate()
        if not valid:
            raise ParameterError(msg=self.errors)
        return self
