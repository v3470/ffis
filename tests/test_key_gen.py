from ffis.model import NextKey,Image
from ffis import db
import pytest
import os
from pathlib import Path

def test_k4_next(app):
    with app.app_context():
        k = lambda x: NextKey.get(x)
        k0,k1,k2,k3,k4 = k('k0'), k('k1'), k('k2'), k('k3'), k('k4')
        assert k0.value == 'm0'
        assert k1.value == '00'
        assert k2.value == '00'
        assert k3.value == '00'
        k4.value = '9999'
        NextKey.update()
        assert k4.value == '1000'
        assert k3.value == '01'
        assert k2.value == '00'
        assert k1.value == '00'
        assert k0.value == 'm0'


def test_k3_next(app):
    with app.app_context():
        k = lambda x: NextKey.get(x)
        k0,k1,k2,k3,k4 = k('k0'), k('k1'), k('k2'), k('k3'), k('k4')
        assert k0.value == 'm0'
        assert k1.value == '00'
        assert k2.value == '00'
        assert k3.value == '00'
        k4.value = '9999'
        k3.value = 'zz'
        NextKey.update()
        assert k4.value == '1000'
        assert k3.value == '00'
        assert k2.value == '01'
        assert os.path.isdir(Path(Image.img_dir_path(),'m0','00','01'))
        k4.value = '9999'
        k3.value = 'zz'
        NextKey.update()
        assert os.path.isdir(Path(Image.img_dir_path(), 'm0', '00', '02'))

def test_k0_next(app):
    with app.app_context():
        k = lambda x: NextKey.get(x)
        k0,k1,k2,k3,k4 = k('k0'), k('k1'), k('k2'), k('k3'), k('k4')
        k4.value = '9999'
        k3.value = 'zz'
        k2.value = 'zz'
        k1.value = 'zz'
        NextKey.update()
        assert k4.value == '1000'
        assert k3.value == '00'
        assert k2.value == '00'
        assert k1.value == '00'
        assert k0.value == 'm1'
        assert os.path.isdir(Path(Image.img_dir_path(),'m1','00','00'))
