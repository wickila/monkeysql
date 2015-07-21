# -*- encoding: UTF-8 -*-
'''
Created on 2015年7月14日

@author: wicki
'''

import monkeysql

monkeysql.init(dbn='mysql', host="127.0.0.1", db='test', user='root', pw='root')

class User(monkeysql.Model):
    __tablename__ = "user"
    def __init__(self,**kwargs):
        monkeysql.Model.__init__(self,**kwargs)
        self.username = kwargs.pop("username")
        self.nickname = kwargs.pop("nickname")
        self.level = kwargs.pop("level")

    def __repr__(self, *args, **kwargs):
        return "<User:id %d,username %s>" % (self.id,self.username)

user = User(username="test",nickname="test",level=1)
user.save()
print user
user = monkeysql.select(User,where="id=1")[0]
print user
user.username = "testafterupdate"
user.save()
#user.delete()
#print len(monkeysql.select(User,where="id=1"))