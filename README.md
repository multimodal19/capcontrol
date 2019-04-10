# capcontrol
A multimodal controller for the Logitech Capture software.

## Usage
This is currently in an experimental state, refer to the instructions in the
directories for individual modalities (e.g. `speech`) to find out how to run
them. It's strongly advised to use virtualenv to keep everything clean. One
per module could be a good idea.

It's based on a default installation of Python 3.7 (64-bit) on Windows, with
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
