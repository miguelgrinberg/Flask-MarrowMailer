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

.. module:: flask_marrowmailer

.. class:: Mailer

  This class encapsulates the mailer functionality.
  
  .. method:: __init__(app)
  
    Initialize the extension. Similar to ``init_app(app)``.
  
  .. method:: init_app(app)
  
    Initialize the extension. Configuration will be obtained from ``app.config['MARROWMAILER_CONFIG']``. If no configuration is found the mailer will be configured to send emails asynchrously via SMTP on ``localhost`` without authentication.
  
  .. method:: new(**kwargs)
  
    Return a new ``Message`` instance. The arguments are passed to the constructor.
    
  .. method:: send(message)
  
    Send the message. If ``message`` is an iterable, then send all the messages.
    
.. class:: Message

  This class encapsulates an email message. It inherits from ``marrow.mailer.Message``, so all the attributes and methods described in the base class `documentation <https://github.com/marrow/marrow.mailer#4-the-message-class>`_ are also available.
  
  .. method:: render_template(plain, rich = None, **context)
  
    Render the body of the message from a template. The 'plain' body will be rendered from a template named ``plain`` or ``plain + '.txt'`` (in that order of preference). The 'rich' body will be rendered from ``rich`` if given, or else from ``plain + '.html'``.
    
  .. method:: render_template_string(plain, rich = None, **context)

    Render the body of the message from a string. If ``rich`` isn't provided then the message will only have the 'plain' body.
