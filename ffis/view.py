from flask import abort,render_template,make_response
from flask import current_app as app
from werkzeug.exceptions import NotFound
from werkzeug.datastructures import FileStorage
from werkzeug.http import parse_date
#from werkzeug.utils import secure_filename
from flask import request, jsonify, send_file,send_from_directory
from .model import Image,NextKey


@app.errorhandler(404)
def hello_world(e: NotFound):
    if request.path.startswith('/ff'):
        response = make_response(render_template('404.xml'))
        response.headers['Content-Type'] = 'text/xml; charset=utf-8'
        return response,404
    return e.get_body(), 404

#todo: access_key_required
@app.route('/ff/<re(".{21,}[^/]$"):path>',methods=('GET','POST'))
def receive(path:str):
    full = path.rsplit('@',1)
    full_path = full[0]; file_args = next(iter(full[1:]),'')
    file_path,file_name = full_path[:9], full_path[:13]
    #todo: 处理file_args
    if request.method == 'GET':
        #todo: 达到redis的404计数上限（3次）后限制访问30分钟
        if record := Image.get(full_path):
            record.count += 1
            record.update_record()

            return send_file(Image.file_path(full_path),conditional=True) #conditional参数用来控制http403
        else:
            abort(404,'key error')

    elif request.method == 'POST':

        if Image.get(full_path) is None:
            img_file:FileStorage = request.files['image']
            force_flag = request.form.get('force')
            dir_exist = None
            save = lambda :_save(img_file,full_path,file_args)

            if not force_flag:
                dir_exist = Image.check_dir(file_path)
            else:
                return save()

            if dir_exist is False:
                return jsonify(status='failed',detail='dir invalid')
            elif dir_exist is True:
                return save()
        else:
            return jsonify(status='failed',detail='file exist')

def _save(img_file,full_path,file_args):
    img  = Image.process(img_file)
    img.save(Image.file_path(full_path))
    img_mobi = Image.compress(img,mode='mobi')
    #img_mobi.save()
    Image(full_path, img_file.filename).update_record()
    if not file_args:
        NextKey.update()
    return jsonify(status='success')

def cache_response(response):
    # 这个缓存方法不一定对
    # response = make_response(send_file(Image.file_path(full_path)))
    # return cache_response(response)
    last_modified = parse_date(response.headers['Last-Modified'])
    if request.if_none_match:
        return response
    else:
        if request.if_modified_since:
            if request.if_modified_since > last_modified:
                return response
        else:
            return response
        return response, 304

@app.route('/next')
def next_path():
    path = Image.get_next_path()
    return jsonify(path=path)

@app.route('/ping')
def ping():
    return {'content':'pong'}
