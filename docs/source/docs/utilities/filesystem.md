# Filesystem

## Introduction to the Filesystem Utilities <a id="introduction-to-the-output-interface"></a>

Cement includes a [Filesystem Utility Module](https://cement.readthedocs.io/en/3.0/api/utils/fs/) with helpers for common tasks related to filesystem management.

**API References:**

* [Cement Filesystem Utility Module](https://cement.readthedocs.io/en/3.0/api/utils/fs/)

## Temporary Directories and Files

Creating and cleaning up temporary directories and files can be tedious, so we created the [`fs.Tmp`](https://cement.readthedocs.io/en/3.0/api/utils/fs/#cement.utils.fs.Tmp) class to make management easy:

{% tabs %}
{% tab title="Example: Temporary Directories and Files" %}
{% code-tabs %}
{% code-tabs-item title="example.py" %}
```python
import os
from cement import fs

# create a tmp object (includes dir and file)
with fs.Tmp() as t:
    # do something with a temporary dir
    print('Temp Dir: %s' % t.dir)
    os.listdir(t.dir)

    # do something with a temporary file
    print('Temp File: %s' % t.file)
    with open(t.file, 'w') as f:
        f.write('some data')
```
{% endcode-tabs-item %}
{% endcode-tabs %}
{% endtab %}

{% tab title="cli" %}
```text
$ python example.py
Temp Dir: /var/folders/jm/cr24ncsn1lgdblxm2mvgtdt40000gn/T/tmpwzo8kh89
Temp File: /var/folders/jm/cr24ncsn1lgdblxm2mvgtdt40000gn/T/tmps4s7n8xg
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
When using the Python `with` operator, the temporary directory and file are automatically cleaned up when exiting the block.
{% endhint %}

## Backup Directories and Files

Creating a `.bak` of a directory or file before modifying it is one of the most common tasks when working with the filesystem, but often takes some tedious code to do so without overwriting existing backups.  The [`fs.backup()`](https://cement.readthedocs.io/en/3.0/api/utils/fs/#cement.utils.fs.backup) creates a `.bak` file, or if it exists `.bak.0`, `.bak.1`, `.bak.2`, etc.

{% tabs %}
{% tab title="Example: Backup Directories and Files" %}
```python
from cement import fs

# create a backup of a file or directory
fs.backup('/path/to/my/file')
```
{% endtab %}
{% endtabs %}

## Filesystem Paths

Best practice when working with paths is to use `os.path.join()` to ensure cross-platform compatibility and also expanding the absolute path to account for things like `~` \(user home dir\) on Linux. We've created a number of helpers to meld these together for common tasks:

{% tabs %}
{% tab title="Example: Filesystem Paths" %}
```python
from cement import fs

# expand the full absolute path
fs.abspath('./some/relative/path')
fs.abspath('~/some/user/path/')

# join a path while also expanding absolute path
fs.join('~', '.myapp')
fs.join('.', 'some', 'sub-dir')

# join a path and test that it exists
path,exists = fs.join_exists('~', '.myapp')
if exists is True:
    # do something with the full absolute path
    os.listdir(path)

# ensure a directory exists
fs.ensure_dir_exists('/path/to/some/dir')

# ensure a parent directory exists
fs.ensure_parent_dir_exists('/path/to/parent/child')
```
{% endtab %}
{% endtabs %}

