from setuptools import find_packages, setup

setup(
    name='ffis',
    description='Fanfou image server re-implement',
    url='https://github.com/fandao-project/ffis',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        #'waitress',
        'flask-sqlalchemy', 'werkzeug', 'sqlalchemy', 'Pillow'
        #'psycopg2'
    ],
    tests_require= [
        'pytest','coverage'
    ]
)