from lib.framework.model import BaseModel


class SystemModelBase(BaseModel):
    __abstract__ = True

    def init(self):
        pass
