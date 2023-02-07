# PySFTP

Supports Python 3.11+[^3]
[^3]: To use an older version of Python, you must install the [tomlib](https://docs.python.org/3.11/library/tomllib.html) module to parse the config.toml file.

## Description

This automation script uploads a file from a remote server to an SFTP server. In addition, the script emails its run results upon completion.

## Installation

From a Windows machine, open Command Prompt, navigate to a local directory where you wish to save this project and run: 

`git clone https://github.com/awilmes/awilmes-pysftp.git`

Next, ensure you have Python and Pip installed, then run:

`pip install -r requirements.txt`

This command will install the necessary dependencies for SFTP functions[^1].
[^1]: This project uses the [Paramiko](https://www.paramiko.org/) Python module for SFTP functions.

## Setup

### Task Scheduler

On Windows, use Task Scheduler to create a trigger for the script. The trigger action should call "pysftp", the main Python file in this project.

### Email

The config.toml file is pre-configured to use a Gmail account. In order for this feature to work properly, the Gmail account must have an associated App password. App password's can only be created for Gmail account's that have 2FA enabled.

[Help with App Passwords](https://support.google.com/accounts/answer/185833?hl=en/)

### Config.toml

Fill the *client*, *server*, and *smtp* fields in the config.toml file, remembering to use double-backslashes (`\\`) for Windows file paths.

The config.toml[^2] file is the *only* file that requires manipulation by the user. The following is an overview of the config parameters:
[^2]: The *.toml* extension indicates a TOML file. TOML files are parsed using the [tomlib](https://docs.python.org/3.11/library/tomllib.html) module, which is included in the standard Python library beginning with Python version 3.11.

#### [client]

- **log**: The desired path of the log file.
    - *Example (Windows):* `"C:\\path\\to\\log\\dir\\log"`
        - *NOTE:* The program will automatically append the current date and the .log extension.

- **source**: Path of directory containing the file to upload.
    - *Example:* `"C:\\path\\to\\source\\dir\\"`

- **archive**: Path of archive directory.
    - *Example:* `"C:\\path\\to\\archive\\dir\\"`

- **key**: Path to private key file.
    - *Example:* `"C:\\keys\\key.pem"`
        - *NOTE:* This project utilizes Paramiko to create an RSA key object from a private key file (.pem). See [Paramiko documention on key handling](https://docs.paramiko.org/en/stable/api/keys.html) for more information.

- **pattern**: Indicates the name of the file to target.
    - *Example:* `"FileName"`

- **extension**: Defines the type of the source file.
    - *Example:* `".csv"`

#### [server]

- **host**: Defines the hostname of the SFTP server.
    - *Example:* `""`

- **user**: Defines the username to log in to the SFTP server with.
    - *Example:* `""`

- **port**: The port number used by the transfer protocol.
    - *Example:* `22`
        - *NOTE:* The config.toml file does not require integers be wrapped in double quotations.

- **upload_dir**: The remote directory to upload to.
    - *Example:* `"/home/upload/dir/"`

#### [smtp]