"""
Flask-MarrowMailer
------------------

Marrow Mailer integration for Flask.
"""
from setuptools import setup


setup(
    name='Flask-MarrowMailer',
    version='0.2.0',
    url='http://github.com/miguelgrinberg/Flask-MarrowMailer/',
    license='MIT',
    author='Miguel Grinberg',
    author_email='miguel.grinberg@gmail.com',
    description='Marrow Mailer integration for Flask.',
    long_description=__doc__,
    py_modules=['flask_marrowmailer'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'marrow.mailer',
        'futures'
    ],
    test_suite = "test_marrowmailer",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

