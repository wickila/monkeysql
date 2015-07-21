# -*- encoding: UTF-8 -*-
'''
Created on 2015年7月9日
数据库ORM封装
#TO-DO：
    1,批量插入数据
@author: wicki
'''
import web

db = None

def init(dburl=None, **params):
    global db
    db = web.database(dburl,**params)

def insert(model,**kwargs):
    return db.insert(model.__tablename__,**kwargs)
'''
    从数据库中查询数据，并且封装成数据对象返回
'''
def select(model,**kwargs):
    result = []
    for dbobj in db.select(model.__tablename__,**kwargs):
        result.append(model(**dict(dbobj)))
    return result

def update(model,**kwargs):
    db.update(model.__tablename__,**kwargs)
    
def delete(model,**kwargs):
    db.delete(model.__tablename__,**kwargs)

class Model(object):
    def __init__(self,**kwargs):
        if not db:
            raise Exception("please init database first!!!")
        self._dirty = []
        if "id" in kwargs:
            self.id = kwargs.pop("id")
    
    def __setattr__(self, *args, **kwargs):  
        key = args[0]
        value = args[1]
        if key in self.__dict__ and getattr(self, key)!=value:
            self._dirty.append(key)
        return object.__setattr__(self, *args, **kwargs)  
    
    def _getinsertrow(self):
        params = [param for param in self.__dict__ if ((not callable(param)) and param.find("_")!=0)]
        keyvalues = {}
        for param in params:
            keyvalues[param] = getattr(self, param)
        return keyvalues
    
    def _getupdaterow(self):
        keyvalues = {}
        for key in self._dirty:
            keyvalues[key] = getattr(self, key)
        return keyvalues
    '''
        如果该数据对象是新建的或者有改变，则写入数据库，如果没改变，则不作任何操作
    '''
    def save(self):
        if not "id" in self.__dict__:
            self.id = insert(self,**self._getinsertrow())
        elif len(self._dirty)>0:
            update(self,where=('id=%d' % self.id),**self._getupdaterow())
            self._dirty = []
    '''
        立即从数据库中删除对象
    '''        
    def delete(self):
        if self.id!=None:
            delete(self,where=('id=%d' % self.id))
        
    def toJSON(self):
        return self._getinsertrow()