from flask import current_app, render_template, render_template_string
from jinja2.exceptions import TemplateNotFound
from marrow.mailer import Mailer as BaseMailer, Message as BaseMessage

class Message(BaseMessage):
    def render_template(self, plain, rich = None, **context):
        self.plain = render_template([plain, plain + '.txt'], **context)
        if rich is not None:
            self.rich = render_tempalte(rich, **context)
        else:
            try:
                self.rich = render_template(plain + '.html', **context)
            except TemplateNotFound:
                pass

    def render_template_string(self, plain, rich = None, **context):
        self.plain = render_template_string(plain, **context)
        if rich is not None:
            self.rich = render_template_string(rich, **context)

class Mailer:
    default_config = {
        'manager.use': 'futures',
        'transport.use': 'smtp',
        'transport.host': 'localhost'
    }

    def __init__(self, app = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        mailer = BaseMailer(app.config.get('MARROWMAILER_CONFIG') or self.default_config)
        app.extensions['marrowmailer'] = mailer

    def new(self, **kwargs):
        return Message(**kwargs)

    def send(self, msg):
        app = self.app or current_app
        mailer = app.extensions['marrowmailer']
        mailer.start()
        if not hasattr(msg, '__iter__'):
            result = mailer.send(msg)
        else:
            result = map(lambda message: mailer.send(message), msg)
        mailer.stop()
        return result

