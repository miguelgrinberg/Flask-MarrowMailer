# -*- coding: utf-8 -*-
from flask import current_app, render_template, render_template_string
from jinja2.exceptions import TemplateNotFound
from marrow.mailer import Mailer as BaseMailer, Message as BaseMessage

class Message(BaseMessage):
    '''This class encapsulates an email message. It inherits from 
    ``marrow.mailer.Message``, so all the attributes and methods 
    described in the base class documentation are available.'''
    
    def render_template(self, plain, rich = None, **context):
        '''Render the body of the message from a template. The plain
        body will be rendered from a template named ``plain`` or 
        ``plain + '.txt'`` (in that order of preference). The rich 
        body will be rendered from ``rich`` if given, or else from 
        ``plain + '.html'``. If neither exists, then the message will
        have no rich body.'''
        self.plain = render_template([plain, plain + '.txt'], **context)
        if rich is not None:
            self.rich = render_template(rich, **context)
        else:
            try:
                self.rich = render_template(plain + '.html', **context)
            except TemplateNotFound:
                pass

    def render_template_string(self, plain, rich = None, **context):
        '''Render the body of the message from a string. If ``rich`` isn’t 
        provided then the message will not have a rich body.'''
        self.plain = render_template_string(plain, **context)
        if rich is not None:
            self.rich = render_template_string(rich, **context)

class Mailer:
    '''This class encapsulates the mailer functionality.'''
    
    default_config = {
        'manager.use': 'futures',
        'transport.use': 'smtp',
        'transport.host': 'localhost'
    }

    def __init__(self, app = None):
        '''Initialize the extension. Similar to ``init_app(app)``.'''
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''Initialize the extension. Configuration will be 
        obtained from ``app.config['MARROWMAILER_CONFIG']``. If no 
        configuration is found the mailer will be configured to 
        send emails asynchrously via SMTP on localhost without 
        authentication. The created ``Mailer`` instance is written
        to ``app.marrowmailer``.'''
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        mailer = BaseMailer(app.config.get('MARROWMAILER_CONFIG') or self.default_config)
        app.extensions['marrowmailer'] = mailer
        app.marrowmailer = self

    def new(self, **kwargs):
        '''Return a new ``Message`` instance. The arguments are 
        passed to the ``marrow.mailer.Message`` constructor.'''
        app = self.app or current_app
        mailer = app.extensions['marrowmailer']
        msg = mailer.new(**kwargs)
        msg.__class__ = Message
        return msg

    def send(self, msg):
        '''Send the message. If message is an iterable, then send 
        all the messages.'''
        app = self.app or current_app
        mailer = app.extensions['marrowmailer']
        mailer.start()
        if not hasattr(msg, '__iter__'):
            result = mailer.send(msg)
        else:
            result = map(lambda message: mailer.send(message), msg)
        mailer.stop()
        return result
