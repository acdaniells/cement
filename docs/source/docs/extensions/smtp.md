# SMTP

## Introduction

The SMTP Extension includes the [`SMTPMailHandler`](https://cement.readthedocs.io/en/3.0/api/ext/ext_smtp/#cement.ext.ext_smtp.SMTPMailHandler), and provides the ability for applications to send email via standard SMTP.

**Documentation References:**

* [Mail Messaging](../core-foundation/mail-messaging.md)

**API References:**

* [Cement SMTP Extension](https://cement.readthedocs.io/en/3.0/api/ext/ext_smtp)
* [Python SMTP Library](https://docs.python.org/3/library/smtplib.html)

## Requirements

* No external depencies

## Configuration

### Application Configuration Settings

This extension supports the following configuration settings under a `[mail.dummy]` configuration section:

| **Setting** | **Description** |
| :--- | :--- |
| **to** | Default recipient address \(list, or comma separated depending on the config handler in use\). |
| **from\_addr** | Default sender address |
| **cc** | Default carbon-copy addresses \(list, or comma separated depending on the config handler in use\) |
| **bcc** | Default blind-carbon-copy addresses \(list, or comma separated depending on the config handler in use\) |
| **subject** | Default subject line |
| **subject\_prefix** | Additional string to prepend to the subject line of all messages |
| **host** | The SMTP host server address. Default: `localhost` |
| **port** | The SMTP host server port. Default: `25` |
| **timeout** | The timeout in seconds before terminating a connection. Default: 30 |
| **ssl** | Whether to initiate SSL or not. Default: `False` |
| **tls** | Whether to use TLS or not \(requires SSL\). Default: `False` |
| **auth** | Whether or not to initiate SMTP authentication. Default: `False` |
| **username** | SMTP authentication username. Default: `None` |
| **password** | SMTP authentication password. Default: `None` |

## Usage

{% tabs %}
{% tab title="Example: Using SMTP Mail Handler" %}
{% code-tabs %}
{% code-tabs-item title="myapp.py" %}
```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'
        mail_handler = 'smtp'

with MyApp() as app:
    app.run()
    app.mail.send('This is my fake message',
        subject='This is my subject',
        to=['john@example.com', 'rita@example.com'],
        from_addr='me@example.com',
        )
```
{% endcode-tabs-item %}

{% code-tabs-item title="~/.myapp.conf" %}
```text
[myapp]

# set the mail handler to use
mail_handler = smtp


[mail.smtp]

# default to addresses (comma separated list)
to = me@example.com

# default from address
from = someone_else@example.com

# default cc addresses (comma separated list)
cc = jane@example.com, rita@example.com

# default bcc addresses (comma separated list)
bcc = blackhole@example.com, someone_else@example.com

# default subject
subject = This is The Default Subject

# additional prefix to prepend to the subject
subject_prefix = MY PREFIX >

# smtp host server
host = localhost

# smtp host port
port = 465

# timeout in seconds
timeout = 30

# whether or not to establish an ssl connection
ssl = true

# whether or not to use start tls
tls = true

# whether or not to initiate smtp auth
auth = true

# smtp auth username
username = john.doe

# smtp auth password
password = oober_secure_password
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}
{% endtabs %}

