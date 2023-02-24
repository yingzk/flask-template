import logging
from decimal import Decimal
from datetime import date, datetime
from contextlib import contextmanager

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from app.exception import NotFoundError, ServerError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, set):
            return list(o)

        logging.error(f'{o} is not serializable')
        raise ServerError(msg='数据解析出错')


class Flask(_Flask):
    json_encoder = JSONEncoder


class Query(BaseQuery):
    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFoundError(msg=description)
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise NotFoundError(msg=description)
        return rv

    def first_and_delete(self):
        rv = self.first()
        if rv:
            rv.delete()


class SQLAlchemy(_SQLAlchemy):
    query_class = Query

    @contextmanager
    def auto_commit(self):
        try:
            yield
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.commit()


class Redprint:
    def __init__(self, name, version='v1'):
        self.name = name
        self.version = version
        self.mount = []

    def route(self, rule, **options):
        def decorator(f):
            self.mount.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = f"/{self.name}"

        for f, rule, options in self.mount:
            endpoint = f"{self.version}+{self.name}+{options.pop('endpoint', f.__name__)}"
            bp.add_url_rule(f"/{self.version}" + url_prefix + rule, endpoint, f, **options)
