# Terminology

## Controller Stacking

In Cement, there are two ways that [application controllers](core-foundation/controllers.md) can be implemented:

* **embedded**: The controller's sub-commands, arguments, and options are embedded within its parent controller's namespace.  To the end-user, usage would appear to be part of the parent controller. Examples:
  * `myapp embedded-sub-command`
  * `myapp --embedded-option`
  * etc
* **nested**: The controller's sub-comands, arguments, and options are nested below its parent controller's namespace.  To the end-user, usage would require prefixing sub-commands with the controller's namespace.  Examples:
  * `myapp nested-controller nested-sub-command`
  * `myapp nested-controller --nested-option`

## Minimal, Complete, Verifiable Example \(MCVE\)

Cement has adopted this term from a post on [Stack Overflow](https://stackoverflow.com/help/mcve). "MCVE" is used to refer to something as a "complete working example". Generally this is used most often on Github when interacting with users, often times reporting bugs or other issues, where a working example is required to reproduce said issue.

## Runtime

Runtime encompasses the entire execution from the moment the application is called at the command line, all the way through to exit. In Cement, this generally involves the following primary steps:

* App Setup
* App Run
* App Close

## Runtime Dispatch

A sub-step within the application runtime that we use to refer to the process of parsing the command-line, processing arguments, mapping sub-commands to controllers, and executing the specified controller function.

