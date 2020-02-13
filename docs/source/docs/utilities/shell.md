# Shell

## Introduction to the Shell Utilities <a id="introduction-to-the-output-interface"></a>

Cement includes a [Shell Utility Module](https://cement.readthedocs.io/en/3.0/api/utils/shell/) with helpers for common tasks related to executing commands, spawning subprocesses/threads, and other tasks.

**API References:**

* [Cement Shell Utility Module](https://cement.readthedocs.io/en/3.0/api/utils/shell/)

## Prompting User Input

Requesting input from the user is straight forward, however we've included the [`shell.Prompt`](https://cement.readthedocs.io/en/3.0/api/utils/shell/#cement.utils.shell.Prompt) utility to expand beyond just a simple one-dimensional input response.

{% tabs %}
{% tab title="Example: User Input Prompts" %}
{% code-tabs %}
{% code-tabs-item title="example.py" %}
```python
from cement import shell

### simple user response prompt

p = shell.Prompt("Press Enter To Continue", default='ENTER')
res = p.prompt()

### provide a numbered list for longer selections

p = shell.Prompt("Where do you live?",
                 options=[
                     'San Antonio, TX',
                     'Austin, TX',
                     'Dallas, TX',
                     'Houston, TX',
                 ],
                 numbered = True)
res = p.prompt()

### Create a more complex prompt, and process the input

class MyPrompt(shell.Prompt):
    class Meta:
        text = "Do you agree to the terms?"
        options = ['Yes', 'no', 'maybe-so']
        options_separator = '|'
        default = 'no'
        clear = True
        max_attempts = 99

    def process_input(self):
        if self.input.lower() == 'yes':
            # do something crazy
            pass
        else:
            # don't do anything... maybe exit?
            print("User doesn't agree! I'm outa here")

p = MyPrompt()
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python example.py

### simple user response prompt

Press Enter To Continue

### provide a numbered list for longer selections

Where do you live?

1: San Antonio, TX
2: Austin, TX
3: Dallas, TX
4: Houston, TX

Enter the number for your selection: 1

### Create a more complex prompt, and process the input

Do you agree to the terms? [Yes|no|maybe-so] no
User doesn't agree! I'm outa here
```
{% endtab %}
{% endtabs %}

## Executing Commands

Shell commands can be executed via the `shell.cmd()` function in two ways; by capturing STDOUT/STDERR and exit code, or just the exit code and letting STDOUT/STDERR print to console normally.

{% tabs %}
{% tab title="Example: Executing Commands" %}
```python
from cement import shell

### execute command and capture output
out, err, code = shell.cmd('echo helloworld')

### execute command with output to console
code = shell.cmd('echo helloworld', capture=False)
```
{% endtab %}
{% endtabs %}

## Spawning Processes and Threads

Spawning processes and threads is easy via the `shell.spawn()` helper.

{% tabs %}
{% tab title="Example: Spawning Processes and Threads" %}
```python
from cement import shell

def add(a, b):
    print(a + b)

### spawn a process
p = shell.spawn(add, args=(12, 27))
p.join()

### spawn a thread
t = shell.spawn(add, args=(12, 27), thread=True)
t.join()
```
{% endtab %}
{% endtabs %}

See the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) and [threading](https://docs.python.org/3/library/threading.html) modules in the Python standard library for more information on working with processes and threads.

