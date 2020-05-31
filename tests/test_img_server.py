import os, io,pathlib
from PIL import Image
from flask.testing import FlaskClient
from werkzeug.datastructures import FileMultiDict
from ffis import model

def test_ping(client):
    r = client.get('/ping')
    content = r.get_json()['content']
    assert 'pong' == content

def test_receive_post(app,client:FlaskClient):

    def image(width, height,format='jpg'):
        img = Image.new('RGB',(width,height),'#4c4c91')
        with app.app_context():
            next_path = model.Image.get_next_path()
            file_path = model.Image.file_path(next_path)
        fp = io.BytesIO()
        if format == 'jpg':
            img.save(fp,format='jpeg',quality=90)
        else:
            img.save(fp,format=format)
        fp.seek(0) # 不知道为什么，如果不用这句命令，Image.open会报错
        data = {'force':'1','image':(fp,'img_1.jpg')}
        # url = '/ff/'+next_path+'@1'
        url = '/ff/'+next_path
        response = client.post(url,data=data,content_type="multipart/form-data")
        assert response.get_json()['status'] == 'success'





