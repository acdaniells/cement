Mail Messaging
==============

Introduction to the Mail Interface
----------------------------------

Cement defines a :ref:`Mail Interface <cement.core.mail>`, as well as the
default :ref:`DummyMailHandler <cement.ext.ext_dummy>` that implements the
interface as a placeholder but does not actually send any mail.

.. warning::
   Cement often includes multiple handler implementations of an interface that
   may or may not have additional features or functionality than the interface
   requires. The documentation below only references usage based on the
   interface and default handler (not the full capabilities of an
   implementation).

**Cement Extensions that Provide Mail Handlers:**

 * :ref:`Dummy <cement.ext.ext_dummy>` *(default)*
 * :ref:`SMTP <cement.ext.ext_smtp>`

**API References:**

 * :ref:`Cement Core Mail Module <cement.core.mail>`

Configuration
-------------

Application Meta Options
~~~~~~~~~~~~~~~~~~~~~~~~

The following options under ``App.Meta`` modify configuration handling:

+------------------+-------------------------------------------------+
| Option           | Description                                     |
+==================+=================================================+
| **mail_handler** | The handler that implements the mail interface. |
+------------------+-------------------------------------------------+

Working with Mail Messages
--------------------------

.. code-block:: python
   :linenos:
   :caption: **Example:** Working with Mail Messages - myapp.py
   :name: example-working-with-mail-messages

   from cement import App

   with App("myapp") as app:
       app.run()

       # send a message using the defined mail handler
       app.mail.send(
           "Test mail message",
           subject="My Subject",
           to=["me@example.com"],
           from_addr="noreply@localhost",
       )

.. code-block:: text
   :caption: **Example:** Working with Mail Messages - console

   $ python3 myapp.py

   =============================================================================
   DUMMY MAIL MESSAGE
   -----------------------------------------------------------------------------

   To: me@example.com
   From: noreply@localhost
   CC:
   BCC:
   Subject: My Subject

   ---

   Test mail message

   -----------------------------------------------------------------------------

.. note::
   The default ``dummy`` mail handler simply prints the message to console, and
   does not send anything. You can override the mail handler via
   ``App.Meta.mail_handler``, for example using the :ref:`SMTP Extension
   <cement.ext.ext_smtp>`.

Creating a Mail Handler
-----------------------

All interfaces in Cement can be overridden with your own implementation. This
can be done either by sub-classing ``MailHandler`` itself, or by sub-classing an
existing extension's handlers in order to alter their functionality.

.. code-block:: python
   :linenos:
   :caption: **Example:** Creating a Mail Handler - myapp.py
   :name: example-creating-a-mail-handler

   from cement import App
   from cement.core.mail import MailHandler

   class MyMailHandler(MailHandler):
       class Meta:
           label = "my_mail_handler"

       # do something to implement the interface

   class MyApp(App):
       class Meta:
           label = "myapp"
           mail_handler = "my_mail_handler"
           handlers = [MyMailHandler]
