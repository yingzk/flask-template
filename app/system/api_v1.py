from flask import jsonify

from lib.framework import Redprint

api = Redprint('system', version='v1')


@api.route('/hello')
def hello():
    return jsonify({'hello': 'world'})
