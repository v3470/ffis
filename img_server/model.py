import random
from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime
from .db import db,Session

class Image(db.Model):
    id = Column(Integer,primary_key=True)
    path = Column(String(36),nullable=False,unique=True) # len(ab/ab/ab/ab_123456.jpg)=22
    old_name = Column(String(128),nullable=True)
    time = Column(DateTime,default=datetime.now)
    count = Column(Integer, default=0,nullable=True) # visit count

    def __init__(self,path, old_name=None):
        length = self.__table__.columns.old_name.type.length
        _o = old_name
        if len(_o)>length:
            L1 = int(length/2)
            old_name = _o[:L1]+'___'+_o[length-L1+3:]
        super().__init__(path=path,old_name=old_name)

    @classmethod
    def get(cls,path):
        return Image.query.filter_by(path=path).first()

    @classmethod
    def get_next_path(cls):
        k = lambda x: NextKey.get(x).value
        k0, k1, k2, k3, k4 = k('k0'), k('k1'), k('k2'), k('k3'), k('k4')
        p = k0 + '/' + k1 + '/' + k2 + '/' + k3 + '_' + k4 + k4_rand() + '.jpg'
        return p


class NextKey(db.Model):
    id = Column(Integer, primary_key=True)
    key = Column(String(2),nullable=False) # k0/k1/k2/k3_k4
    value = Column(String(4),nullable=False)

    @classmethod
    def get(cls,key):
        return cls.query.filter_by(key=key).first()

    @classmethod
    def update(cls):
        return k4_next()

def init_key():
    Session.add(NextKey(key='k0',value='m0'))
    Session.add(NextKey(key='k1', value='00'))
    Session.add(NextKey(key='k2', value='00'))
    Session.add(NextKey(key='k3', value='00'))
    Session.add(NextKey(key='k4', value='1000'))
    Session.commit()


def k4_rand():
    return str(random.randint(0,99)).zfill(2)

def k4_next():
    k4 = NextKey.get('k4')
    if (k4v:=int(k4.value)) >=9999:
        k4.value = '1000'
        k_next(['k3','k2','k1','k0'])
    else:
        k4.value = str(k4v+1).zfill(4)
    Session.commit()
    #return k4

def k_next(key):
    k0最大值 = 'm9' # 理论最大值是'zz',一位k0对应1.9591041024e+13个子项
    k = NextKey.get(_k:=key[0])

    if (kv:=k.value) == 'zz':
        k.value = '00'
        k_next(key[1:])
    elif kv==k0最大值 and _k=='k0':
        raise IOError("已达到最大存储数量") # reach max k0 size
    else:
        k.value = to_base36(base36to(kv)+1)

def base36to(n):
    return int(n,36)

def to_base36(n):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    value = ''
    if 0 <= n < len(alphabet):
        return alphabet[n]

    while n != 0:
        n, index = divmod(n, len(alphabet))
        value = alphabet[index] + value
    return value


def create_table(T:db.Model):
    T.__table__.create(db.engine)

def init_key_dir(app):
    import os
    try:
        path = os.path.join(app.instance_path,app.config['IMAGE_DIR'],'m0','00','00')
        os.makedirs(path,mode=764) # or alt with chmod
    except OSError:
        pass


