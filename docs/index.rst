.. Flask-MarrowMailer documentation master file, created by
   sphinx-quickstart on Thu Aug  8 23:39:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask-MarrowMailer's documentation!
==============================================

Flask-MarrowMailer is a Flask extension that simplifies the use of `marrow.mailer <https://github.com/marrow/marrow.mailer>`_ to send emails in Flask applications.

Installation
------------

You can install Flask-MarrowMailer with pip::

$ pip install Flask-MarrowMailer

Examples
--------

The following is a basic example that sends a test email when the route ``/send`` is accessed::

    from flask import Flask
    from flask_marrowmailer import Mailer

    app = Flask(__name__)
    mailer = Mailer(app)

    @app.route('/send')
    def send_email():
        msg = mailer.new()
        msg.author = 'Sender <sender@localhost>'
        msg.to = ['user@example.com']
        msg.subject = 'test email'
        msg.plain = 'this is the text version'
        msg.rich = '<p>this is the <b>html</b> version</p>'
        mailer.send(msg)
        return "email sent!"

    app.run(debug = True)

The message can also render the body from templates::

    @app.route('/send')
    def send_email():
        msg = mailer.new()
        msg.author = 'Sender <sender@localhost>'
        msg.to = ['user@example.com']
        msg.subject = 'test email'
        msg.render_template('body.email', user = 'david')
        mailer.send(msg)
        return "email sent!"

In the above example the message class will first look for a file named ``'body.email'`` or ``'body.email.txt'`` in the templates folder and will render that template found to ``msg.plain``. Then it will look for ``'body.email.html'`` and if found will render the template to ``msg.rich``.

Configuration
-------------

Flask-MarrowMailer uses a single configuration key called ``MARROWMAILER_CONFIG``. The value of this key is passed intact to marrow.mailer as configuration.

The following example configures Flask-MarrowMailer to send email asynchronously through a gmail account sending a maximum of five messages per connection::

    app.config['MARROWMAILER_CONFIG'] = {
        'manager.use': 'futures',
        'transport.use': 'smtp',
        'transport.host': 'smtp.gmail.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': 'gmail username',
        'transport.password': 'gmail password',
        'transport.max_messages_per_connection': 5
    }

If the ``MARROWMAILER_CONFIG`` key is missing the following default configuration is used::

    app.config['MARROWMAILER_CONFIG'] = {
        'manager.use': 'futures',
        'transport.use': 'smtp',
        'transport.host': 'localhost'
    }

Consult the `marrow.mailer documentation <https://github.com/marrow/marrow.mailer>`_ for a complete list of configuration options.

API
---

.. automodule:: flask_marrowmailer
   :members:
   
