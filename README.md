#关于monkeysql
monkeysql是一个用于web.py的轻量化ROM。如果想用ROM。monkeysql与数据库之间的接口既遵循web.py的数据库接口，另外也可以直接使用类似save(),delete()的函数。
###用法
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