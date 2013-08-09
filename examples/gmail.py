from flask import Flask
from flask_marrowmailer import Mailer, Message

app = Flask(__name__)
app.config['MARROWMAILER_CONFIG'] = {
    'manager.use': 'futures',
    'transport.use': 'smtp',
    'transport.host': 'smtp.gmail.com',
    'transport.port': 465,
    'transport.tls': 'ssl',
    'transport.username': 'gmail-username',
    'transport.password': 'gmail-password',
    'transport.max_messages_per_connection': 5
}
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

