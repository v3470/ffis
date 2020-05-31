import os,shutil
import tempfile
import pytest

import ffis
from ffis import db,default_config

@pytest.fixture
def app():
    prefix = 'f2is_'
    db_key = 'SQLALCHEMY_DATABASE_URI'
    config = {'TESTING':True}
    default = {k:getattr(default_config,k) for k in dir(default_config) if not k.startswith('__')}
    config.update(default)
    db_fd, db_path = tempfile.mkstemp(prefix=prefix)
    config[db_key] = 'sqlite:///'+db_path

    instance_path = tempfile.mkdtemp(prefix=prefix)
    app = ffis.create_app(config)
    app.instance_path = instance_path

    with app.app_context():
        db.init_db(app)
    yield app
    #print(instance_path)
    shutil.rmtree(instance_path)
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()