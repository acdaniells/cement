# Part 2: Adding Features

Now that we have a working development environment and have become familiar with running our `todo` app, we can build in our initial feature set to manage task items.

## Persistent Storage

Before we can create anything, we need some way to store it.  For this project, we've chosen [TinyDB](http://tinydb.readthedocs.io/en/latest/), a light-weight key-value database that stores data on disk in a single JSON file.

Let's begin by adding the dependency to our `requirements.txt` file, and installing it to our virtualenv:

{% tabs %}
{% tab title="Add TinyDB Dependency" %}
Add the following to the bottom of the pip `requirements.txt` file:

```text
tinydb
```

Install the new requirements with `pip`:

```text
$ pip install -r requirements.txt
...
Successfully installed tinydb-3.10.0
```
{% endtab %}
{% endtabs %}

With our dependency installed, we need to add it to our application.  The primary things we will cover here are:

* Configuration settings for where we will store the `db.json` file on disk
* Using framework hooks to run code at a specific point in our runtime
* Extending our `app` with a `db` object we will use to integrate and access the TinyDB functionality in our application

{% tabs %}
{% tab title="Add Configuration Defaults" %}
Find and modify the following section of `todo/main.py` in order to define a default configuration for our database file called `db_file`:

```python
# configuration defaults
CONFIG = init_defaults('todo')
CONFIG['todo']['db_file'] = '~/.todo/db.json'
```

To be kind to our users, we will also want to add this default setting to our example configuration file `config/todo.yml.example`.  Modify the file to include the following:

```yaml
---
todo:

### Database file path
# db_file: ~/.todo/db.json
```
{% endtab %}
{% endtabs %}

We want to extend our application with a re-usable `db` object that can be used throughout our code.  There are many ways we could do this, however here we are going to use a [framework hook](../../core-foundation/hooks.md).

{% tabs %}
{% tab title="Add DB Object Code" %}
Add the following to the top of the `todo/main.py` file:

```python
import os
from tinydb import TinyDB
from cement.utils import fs

def extend_tinydb(app):
    app.log.info('extending todo application with tinydb')
    db_file = app.config.get('todo', 'db_file')
    
    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.info('tinydb database file is: %s' % db_file)
    
    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))
```

We've created a function to extend our application to include an `app.db` object, however in order for it to take affect we need to register the function as a hook with the framework.  Add the following `hooks` meta option to our Todo app in `todo/main.py`:

```python
class Todo(App):
    class Meta:
        hooks = [
            ('post_setup', extend_tinydb),
        ]
```

Now, when we run `todo` again you will see that our hook is executed \(via the `info` logs\):

```text
$ todo --help
INFO: extending todo application with tinydb
INFO: tinydb database file is: /Users/derks/.todo/db.json
...
```

And we can see that the database was created:

```text
$ cat ~/.todo/db.json
{"_default": {}}
```
{% endtab %}
{% endtabs %}

## Controllers and Sub-Commands

In order to work with todo items we need to map out commands with our app.  We could do this with the existing `Base` controller, however to keep code clean and organized we want to create an new controller called `Items`.  

At this point, we have a decision to make regarding [controller stacking](../../terminology.md#controller-stacking).  Do we want our controllers commands to appear **embedded** under the primary applications namespace \(ex: `todo my-command`\) or do we want a separate **nested** namespace \(ex: `todo items my-command`\).  As our application is still small, we will opt to embed our controllers commands under the primary namespace \(to keep our commands and examples shorter\).

{% tabs %}
{% tab title="Add Items Controller Code" %}
Add the following stubs to `todo/controllers/items.py` as a placeholder for our sub-commands:

```python
from cement import Controller, ex


class Items(Controller):
    class Meta:
        label = 'items'
        stacked_type = 'embedded'
        stacked_on = 'base'
    
    @ex(help='list items')
    def list(self):
        pass
        
    @ex(help='create new item')
    def create(self):
        pass
        
    @ex(help='update an existing item')
    def update(self):
        pass
    
    @ex(help='delete an item')
    def delete(self):
        pass
    
    @ex(help='complete an item')
    def complete(self):
        pass
        
```
{% endtab %}
{% endtabs %}

We've created the controller code, however for it to take affect we need to register it with our application.

{% tabs %}
{% tab title="Register Controller with App" %}
Add/modify the following in `todo/main.py`:

```python
from .controllers.items import Items

class Todo(App):
    class Meta:
        # ...
        handlers = [
            Base,
            Items,
        ]
```

With our new controller registered, lets see it in action:

```text
$ todo --help
INFO: extending todo application with tinydb
INFO: tinydb database file is: /Users/derks/.todo/db.json
usage: todo [-h] [-d] [-q] [-v]
            {complete,create,delete,update} ...

A Simple TODO Application

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           full application debug mode
  -q, --quiet           suppress all console output
  -v, --version         show program's version number and exit

sub-commands:
  {complete,create,delete,update}
    complete            complete an item
    create              create new item
    delete              delete an item
    update              update an existing item

Usage: todo command1 --foo bar
```
{% endtab %}
{% endtabs %}

## Feature Functionality

We've stubbed out our `Items` controller and sub-commands, so lets add the actual code that will support each of these features:

### Create Items

{% tabs %}
{% tab title="Add Create Items Code" %}
Add/modify the following in `todo/controllers/items.py`:

{% code-tabs %}
{% code-tabs-item title="todo/controllers/items.py" %}
```python
from time import strftime

class Items(Controller):
    # ...
    
    @ex(
        help='create an item',
        arguments=[
            ( ['item_text'],
              {'help': 'todo item text',
               'action': 'store' } )
        ],
    )
    def create(self):
        text = self.app.pargs.item_text
        now = strftime("%Y-%m-%d %H:%M:%S")
        self.app.log.info('creating todo item: %s' % text)

        item = {
            'timestamp': now,
            'state': 'pending',
            'text': text,
        }

        self.app.db.insert(item)
```
{% endcode-tabs-item %}
{% endcode-tabs %}

We've now built out the functionality to create items in our database, that will include the `text`, a `state` \(pending/complete\), and also the `timestamp` of when it was created/updated. Notice that we've added arguments to the sub-command function, and not the controller because the `item_text` argument is only relevant to the `create` action, and not the application or controller namespace as a whole.

 Let's try it out:

```text
$ todo create "Call Saul"
INFO: creating todo item: Call Saul

$ todo create "Go to Car Wash"
INFO: creating todo item: Go to Car Wash

$ todo create "Meet with Jessie About a Thing"
INFO: creating todo item: Meet with Jessie About a Thing
```
{% endtab %}
{% endtabs %}

### List Items

We've created an item, so now we need to be able to list them.  First, let's take a look at our database:

```text
$ cat ~/.todo/db.json | python -m json.tool
{
    "_default": {
        "1": {
            "timestamp": "2018-07-30 15:11:53",
            "state": "pending",
            "text": "Call Saul"
        },
        "2": {
            "timestamp": "2018-07-30 15:12:07",
            "state": "pending",
            "text": "Go to Car Wash"
        },
        "3": {
            "timestamp": "2018-07-30 15:12:54",
            "state": "pending",
            "text": "Meet with Jessie About a Thing"
        }
    }
}
```

We can see that TinyDB automatically generates database IDs, so we will want to display that when listing our items so that we can easily update/delete/complete by ID later.

{% tabs %}
{% tab title="Add List Items Code" %}
Add/modify the following in `todo/controllers/items.py`:

{% code-tabs %}
{% code-tabs-item title="todo/controllers/items.py" %}
```python
class Items(Controller):
    # ...
    
    @ex(help='list items')
    def list(self):
        data = {}
        data['items'] = self.app.db.all()
        self.app.render(data, 'items/list.jinja2')
```
{% endcode-tabs-item %}
{% endcode-tabs %}

Here we are pulling all of the items from the database, putting it into a data dictionary, then rendering with the [Jinja2OutputHandler](../../extensions/jinja2.md).  Put the following in the template file `todo/templates/items/list.jinja2`:

{% code-tabs %}
{% code-tabs-item title="todo/templates/items/list.jinja2" %}
```text
{% for item in items %}
{{ item.doc_id }} [{% if item.state == 'complete' %}X{% else %} {% endif %}] {{ item.text }}
{% endfor %}
```
{% endcode-tabs-item %}
{% endcode-tabs %}

It's a little messy, but that's why we put this in a separate template and not in our code.  We are including the ID so that we can use that for updating/deleting/etc, and also a `[ ]` \(checkbox\) that will be "checked" when the item's state is `complete`.

Let's have a go:

```text
$ todo list
1 [ ] Call Saul
2 [ ] Go to Car Wash
3 [ ] Meet with Jessie About a Thing
```
{% endtab %}
{% endtabs %}

### Update Items

If we've made a typo, or want to change an existing item we need a way to update it.  

{% tabs %}
{% tab title="Add Update Items Code" %}
Add/modify the following in `todo/controllers/items.py`:

{% code-tabs %}
{% code-tabs-item title="todo/controllers/items.py" %}
```python
class Items(Controller):
    # ...

    @ex(
        help='update an existing item',
        arguments=[
            ( ['item_id'],
              {'help': 'todo item database id',
               'action': 'store' } ),
            ( ['--text'],
              {'help': 'todo item text',
               'action': 'store' ,
               'dest': 'item_text' } ),
        ],
    )
    def update(self):
        id = int(self.app.pargs.item_id)
        text = self.app.pargs.item_text
        now = strftime("%Y-%m-%d %H:%M:%S")
        self.app.log.info('updating todo item: %s - %s' % (id, text))

        item = {
            'timestamp': now,
            'text': text,
        }

        self.app.db.update(item, doc_ids=[id])
```
{% endcode-tabs-item %}
{% endcode-tabs %}

Given a TinyDB ID, we can update our item including touching the `timestamp` and modifying the text.  Let's update our todo item:

```text
$ todo update 2 --text "Send Skyler to Car Wash"
INFO: updating todo item: 2 - Send Skyler to Car Wash

$ todo list
1 [ ] Call Saul
2 [ ] Send Skyler to Car Wash
3 [ ] Meet with Jessie About a Thing
```
{% endtab %}
{% endtabs %}

### Complete Items

A TODO list is not complete \(ah! pun intended\) without the ability to check off items that are done. This operation gets a little more interesting as we want to also send an email message when items are completed.

{% tabs %}
{% tab title="Add Complete Items Code" %}
Add/modify the following in `todo/controllers/items.py`:

{% code-tabs %}
{% code-tabs-item title="todo/controllers/items.py" %}
```python
class Items(Controller):
    # ...
    
    @ex(
        help='complete an item',
        arguments=[
            ( ['item_id'],
              {'help': 'todo item database id',
              'action': 'store' } ),
        ],
    )
    def complete(self):
        id = int(self.app.pargs.item_id)
        now = strftime("%Y-%m-%d %H:%M:%S")
        item = self.app.db.get(doc_id=id)
        item['timestamp'] = now
        item['state'] = 'complete'

        self.app.log.info('completing todo item: %s - %s' % (id, item['text']))
        self.app.db.update(item, doc_ids=[id])

        ### send an email message
        
        msg = """
        Congratulations! The following item has been completed:

        %s - %s
        """ % (id, item['text'])
        
        self.app.mail.send(msg,
                      subject='TODO Item Complete',
                      to=[self.app.config.get('todo', 'email')],
                      from_addr='noreply@localhost',
                      )
```
{% endcode-tabs-item %}
{% endcode-tabs %}

Add/modify the following in `todo/main.py`:

```python
# configuration defaults
CONFIG = init_defaults('todo')
CONFIG['todo']['email'] = 'you@yourdomain.com'
```

Now let's complete one of our items:

```text
$ todo complete 2
INFO: completing todo item id: 2

=============================================================================
DUMMY MAIL MESSAGE
-----------------------------------------------------------------------------

To: you@yourdomain.com
From: noreply@localhost
CC:
BCC:
Subject: TODO Item Complete

---


        Congratulations! The following item has been completed:

        2 - Send Skyler to Car Wash


-----------------------------------------------------------------------------

$ todo list
1 [ ] Call Saul
2 [X] Send Skyler to Car Wash
3 [ ] Meet with Jessie About a Thing
```



{% hint style="info" %}
Notice that the email message was not sent, but rather printed to console.  This is because the default `mail_handler` is set to `dummy`.  You can override this to use the `smtp` mail handler via the applications configuration files \(ex:`~/.todo.yml)`
{% endhint %}
{% endtab %}
{% endtabs %}

### Delete Items

Finally, if we just want to get rid of something, we need the ability to delete it:

{% tabs %}
{% tab title="Add Delete Code" %}
Add/modify the following in `todo/controllers/items.py`:

{% code-tabs %}
{% code-tabs-item title="todo/controllers/items.py" %}
```python
class Items(Controller):
    # ...
    
    @ex(
        help='delete an item',
        arguments=[
            ( ['item_id'],
              {'help': 'todo item database id',
              'action': 'store' } ),
        ],
    )
    def delete(self):
        id = int(self.app.pargs.item_id)
        self.app.log.info('deleting todo item id: %s' % id)
        self.app.db.remove(doc_ids=[id])
```
{% endcode-tabs-item %}
{% endcode-tabs %}

And lets delete our completed item:

```text
$ todo delete 2
INFO: deleting todo item id: 2

$ todo list
1 [ ] Call Saul
3 [ ] Meet with Jessie About a Thing
```
{% endtab %}
{% endtabs %}

## Conclusion

That concludes Part 2!  We now have a fully functional TODO application.  In the next parts we will discuss more indepth about extending the project with plugins, and digging deeper on things like documentation and testing.

