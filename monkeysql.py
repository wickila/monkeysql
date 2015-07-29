# -*- encoding: UTF-8 -*-
'''
Created on 2015年7月9日
数据库ORM封装
@author: wicki
'''
import web

db = None

def init(dburl=None, **params):
    global db
    db = web.database(dburl,**params)

def select(model,**kwargs):
    '''
            从数据库中查询数据，并且封装成数据对象返回
            ex:users = monkeysql.select(User,where="id=1")
        详细用法参见web.py数据库的select用法:http://webpy.org/cookbook/select.zh-cn
    '''
    result = []
    for dbobj in db.select(model.__tablename__,**kwargs):
        result.append(model(**dict(dbobj)))
    return result
    
def multiple_insert(model,values=[]):
    '''
        批量插入数据
        ex:
        users = [User(username="test1"),User(username="test2")]
        out = monkeysql.multiple_insert(User,users)
        print users[1].id
    '''
    out = db.multiple_insert(model.__tablename__, [value._getinsertrow() for value in values])
    for index,value in enumerate(values):
        value.id = out[index]

def multiple_delete(model,values=[]):
    '''
        批量删除数据
        ex:
        monkeysql.multiple_delete(User,users)
    '''
    db.delete(model.__tablename__,where="id in (%s)" % ",".join([value.id for value in values]))

class Model(object):
    '''
        数据模型基类，默认主键为id
    '''
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
    
    def save(self):
        '''
                    如果该数据对象是新建的或者有改变，则写入数据库，如果没改变，则不作任何操作                                    
        '''
        if not "id" in self.__dict__:
            self.id = db.insert(self.__tablename__,**self._getinsertrow())
        elif len(self._dirty)>0:
            db.update(self.__tablename__,where=('id=%d' % self.id),**self._getupdaterow())
            self._dirty = []
           
    def delete(self):
        '''
                立即从数据库中删除对象
        ''' 
        if self.id!=None:
            db.delete(self.__tablename__,where=('id=%d' % self.id))
        
    def toJSON(self):
        return self._getinsertrow()