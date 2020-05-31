import random,os,pathlib,io
from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime
from PIL import Image as _Image
from flask import g,current_app
from werkzeug.datastructures import FileStorage
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

    @classmethod
    def check_dir(cls,file_path):
        dir_path = os.path.join(cls.img_dir_path(),pathlib.Path(file_path))
        return os.path.isdir(dir_path)

    @classmethod
    def img_dir_path(cls):
        return os.path.join(current_app.instance_path, current_app.config['IMAGE_DIR'])

    @classmethod
    def file_path(cls,path,mode='default'):
        # todo: 加上file_args的处理，还有旋转后的file_args
        return str(pathlib.Path(cls.img_dir_path(),path))

    @classmethod
    def compress(cls,img,mode='default'):
        #todo: 去掉mode，直接传参数
        def resize(max_width,max_height):
            img1 = img.copy()
            img1.thumbnail((max_width,max_height))
            return img1

        if mode == 'default':
            width = current_app.config['MAX_IMAGE_WIDTH']
            height = current_app.config['MAX_IMAGE_HEIGHT']
            return resize(width,height)
        elif mode == 'mobi':
            length = current_app.config['MAX_IMAGE_MOBI_LENGTH']
            return resize(length,length)
        elif mode == 'thumb':
            # 旋转后的图片需要重新生成缩略图
            length = current_app.config['MAX_IMAGE_THUMB_LENGTH']
            return resize(length,length)

    @classmethod
    def process(cls,img_file):
        img:_Image.Image = _Image.open(img_file)
        if img.mode != 'RGB':
            img.convert('RGB')
        fp = io.BytesIO()
        img.save(fp, format='jpeg', quality=90)
        img1 = Image.compress(_Image.open(fp))
        return img1

    @classmethod
    def rotate(cls,img):
        # 旋转时不需要重新压缩
        # todo: test rotate
        return

    def update_record(self):
        Session.add(self)
        Session.commit()

class NextKey(db.Model):
    id = Column(Integer, primary_key=True)
    key = Column(String(2),nullable=False,unique=True) # k0/k1/k2/k3_k4
    value = Column(String(4),nullable=False)

    @classmethod
    def get(cls,key):
        return cls.query.filter_by(key=key).first()

    @classmethod
    def update(cls):
        return k4_next(current_app)

def init_key():
    Session.add(NextKey(key='k0', value='m0'))
    Session.add(NextKey(key='k1', value='00'))
    Session.add(NextKey(key='k2', value='00'))
    Session.add(NextKey(key='k3', value='00'))
    Session.add(NextKey(key='k4', value='1000'))
    Session.commit()


def k4_rand():
    return str(random.randint(0,99)).zfill(2)

def k4_next(app):
    k4 = NextKey.get('k4')
    if (k4v:=int(k4.value)) >=9999:
        k4.value = '1000'
        klist = []
        k_next(app,['k3','k2','k1','k0'],klist)

        if klist:
            img_dir_path = Image.img_dir_path()
            path = os.path.join(img_dir_path, *reversed(klist))
            os.makedirs(path, mode=app.config['DIR_MODE'],exist_ok=True)
    else:
        k4.value = str(k4v+1).zfill(4)
    Session.commit()
    #return k4

def k_next(app, keys, klist):
    k0最大值 = 'm9' # 理论最大值是'zz',一位k0对应1.9591041024e+13个子项
    k = NextKey.get(_k:=keys[0])

    if (kv:=k.value) == 'zz':
        k.value = '00'
        if _k != 'k3':
            klist.append(k.value)
        k_next(app, keys[1:], klist)
    elif kv==k0最大值 and _k=='k0':
        raise IOError("已达到最大存储数量") # reach max k0 size
    else:
        k.value = to_base36(base36to(kv)+1).zfill(2)
        if _k != 'k3':
            for i in keys:
                klist.append(NextKey.get(i).value)

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
    try:
        path = os.path.join(Image.img_dir_path(),'m0','00','00')
        os.makedirs(path,mode=app.config['DIR_MODE'],exist_ok=True) # or alt with chmod
    except OSError:
        pass
