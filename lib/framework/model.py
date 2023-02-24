from datetime import datetime
from abc import abstractmethod

from flask import current_app, g
from sqlalchemy import orm, Column, DateTime, text
from sqlalchemy.ext.declarative import declared_attr

from app.plugin import db


class BaseModel(db.Model):
    __abstract__ = True

    indexs = []

    createTime = Column(DateTime, default=datetime.now, nullable=False, comment='创建时间', name='create_time',
                        server_default=text("CURRENT_TIMESTAMP"))
    updateTime = Column(DateTime, default=datetime.now, nullable=False, comment='更新时间', name='update_time',
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    @abstractmethod
    def init(self):
        pass

    def __repr__(self):
        vs = vars(self)
        [vs.pop(item) for item in ['fields', '_sa_instance_state'] if item in vs]

        return str(vs)

    @orm.reconstructor
    def __init__(self, **kwargs):
        self.fields = ['id', 'createTime']
        [setattr(self, k, v) for k, v in kwargs.items()]
        self.init()

    @declared_attr
    def __table_args__(cls):
        return (
            *cls.indexs,
            {
                'extend_existing': True,
                'mysql_engine'   : 'InnoDB',
                'comment'        : cls.__doc__
            }
        )

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except Exception as e:
            if current_app.config['DEBUG']:
                raise e from None
            current_app.logger.error('解析字段错误')

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            if key in self.fields:
                self.fields.remove(key)
        return self

    def append(self, *keys):
        self.fields.extend(keys)
        return self

    def flush_obj(self):
        db.session.add(self)
        db.session.flush()
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        current_app.logger.info(f'【资源删除】{self}')
        db.session.delete(self)
        db.session.commit()

    def update(self, data: dict):
        if 'id' in data:
            del data['id']

        for key, value in data.items():
            if value is not None:
                setattr(self, key, value)

        if 'updaterId' in dir(self) and g.user:
            setattr(self, 'updaterId', g.user.id)

        return self.save()
