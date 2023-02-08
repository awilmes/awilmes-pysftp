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

Fill the *client*, *server*, and *smtp* fields in the config.toml file, remembering to use double-backslashes (`\\`) for Windows file paths if not using an alternative solution.

The config.toml[^2] file is the *only* file that requires manipulation by the user. The following is an overview of the config parameters:
[^2]: The *.toml* extension indicates a TOML file. TOML files are parsed using the [tomlib](https://docs.python.org/3.11/library/tomllib.html) module, which is included in the standard Python library beginning with Python version 3.11.

| Table | Key | Description | Data Type | Example |
| :-----: | :----- | :------------------------ | :------ | --------------------------: |
| Client | log | Path to log file. | String | `"C:\\path\\source\\logs\\log"`[^4] |
[^4]: Path cannot be a directory. The script will automatically append the current date and the .log extension to each log file.
| Client | source | Path to source directory. | String | `"C:\\path\\source\\"` |
| Client | archive | Path to archive directory. | String | `"C:\\path\\source\\archive\\"` |
| Client | key | Path to private key file. | String | `"C:\\keys\\privateKey.pem"`[^5] |
[^5]: This project utilizes Paramiko to create an RSA key object from a private key file (.pem). See [Paramiko documention on key handling](https://docs.paramiko.org/en/stable/api/keys.html) for more information.
| Client | pattern | Name of the target file. | String | `"Filename"` |
| Client | extension | Extension of the target file. | String | `".csv"` |
| Server | host | Hostname of the server. | String | `"ftp.test.net"` |
| Server | user | Username of the server. | String | `"user"` |
| Server | port | Port number. | Integer | `20`[^6] |
| Server | upload_dir | Server directory to upload to. | String | `"/usr/home/"` |
| smtp | host | Hostname of smtp server. | String | `"smtp.gmail.com"` |
| smtp | port | Port number to use. | Integer | `465`[^6] |
[^6]: See [toml documentation](https://toml.io/en/v1.0.0#integer) for more information on data types.
| smtp | user | Sender address. | String | `"user@gmail.com"` |
| smtp | password | Sender app password. | String | `"app-p@ssw0rd"` |
| smtp | recipient | Recipient address. | String | `"recipient@email.net"` |
