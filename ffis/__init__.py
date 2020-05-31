import os
from flask import Flask,g
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex = items[0]

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.converters['re'] = RegexConverter

    if test_config is None:
        if app.config['ENV']=='development':
            filename = 'development_config.py'
        else:
            filename = 'production_config.py'
        app.config.from_pyfile(filename, silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #todo: 生成redis post_key

    from . import db
    db.db.init_app(app)
    db.init_app(app)

    with app.app_context():
        from . import view
        g.img_dir_path = os.path.join(app.instance_path, app.config['IMAGE_DIR'])

    return app

