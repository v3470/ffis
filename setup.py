from setuptools import find_packages, setup

setup(
    name='f2is',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalchemy', 'werkzeug', 'sqlalchemy'
        #'psycopg2'
    ],
)