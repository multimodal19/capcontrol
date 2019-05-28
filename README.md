# capcontrol
A multimodal controller for the Logitech Capture software.

## Usage
This is a collection of independently running modules, each of which provides
some functionality.
It's possible to run the system with just a couple of them, albeit with reduced
functionality. The coordinator is an essential part of the system, so it should
definitely run alongside the other modules you choose.
Refer to the instructions in the directories for individual modules to find out
how to run them.
It's strongly advised to use virtualenv to keep everything clean. One per
module could be a good idea.

The system was built and tested with Python 3.7 (64-bit) on Windows, with
the Python distribution added to the PATH variable. These are the preparations
that may be necessary to be able to install dependencies for the different
modules that make up the application:

1. If the `virtualenv` command is not recognized, start an administrator
   PowerShell and run `pip install virtualenv` to install it globally.
2. Allow scripts for virtualenv activation. From administrator PowerShell run
   `Set-ExecutionPolicy -ExecutionPolicy Unrestricted`.

Now you're ready and can create and activate virtualenvs inside the directories
for the different modalities with
```
virtualenv env
.\env\Scripts\activate
```

## License
[MIT license](LICENSE)
