from pathlib import Path
from flask import abort,render_template
from flask import current_app as app
from flask.testing import FlaskClient
from flask import Response
from werkzeug.exceptions import NotFound
from werkzeug import FileStorage
from flask import request, flash, jsonify, send_file

from .model import Image,NextKey
from .db import Session


@app.errorhandler(404)
def hello_world(e: NotFound):
    if request.path.startswith('/ff'):
        return 'Hello World?',404
    return e.get_body(), 404

@app.route('/ff/<re(".{21,}[^/]$"):path>',methods=('GET','POST'))
def receive(path:str):
    full = path.rsplit('@',1)
    full_path = full[0]; file_args = next(iter(full[1:]),'')
    #file_path,file_name = full_path[:9], full_path[:13]
    record = Image.get(full_path)
    dst = lambda p:str(Path(app.instance_path,app.config['IMAGE_DIR'],Path(p)))
    if request.method == 'GET':
        if record:
            record.count += 1
            Session.add(record)
            Session.commit()
            return send_file(dst(full_path))
        else:
            abort(404,'key error')
    elif request.method == 'POST':
        if record is None:
            img:FileStorage = request.files['image']
            img.save(dst(full_path))
            Session.add(Image(full_path,img.filename))
            Session.commit()
            NextKey.update()
            return jsonify(status='success')
        else:
            return jsonify(status='failed',detail='file exist')

@app.route('/next')
def next_path():
    path = Image.get_next_path()
    return jsonify(path=path)

@app.route('/pong')
def get_test():
    c:FlaskClient = app.test_client()
    r:Response = c.get('/ping')
    data = r.get_json()
    return data

@app.route('/ping')
def ping():
    return {'content':'pong'}
