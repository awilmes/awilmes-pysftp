# PySFTP

## Description

The motivation for this project was to eliminate the manual labor associated with uploading a daily report to an SFTP server. Before, the user was required to save a .csv attachment from their Outlook inbox to their local machine, upload the file to an SFTP server using a program like WinSCP, and then archive the file. By configuring this program to run using a service account, reliable daily automation can be acheived independent of external factors such as staff turnover.

## Features

### Basic Overview

This project takes a modular approach to solving the aforementioned issue. The present code is independent of any hard-coded values: Log path, source file path, archive path, **RSA** key path, file name, and file extension, are input by the user into the config.toml file during the initial setup. In addition, the config.toml file also contains server parameters such as the host, user, port, and upload directory, as well as SMTP parameters for transmitting log files upon completed execution.

The program determines the correct file to upload by searching the source directory for a file name matching the following syntax:

`<FileName>_<Date>.<Extension>`

*Example:* `FileName_20221013.csv`

If the target file is not to be found, the program will log the error and exit. Upon a successful execution, the program will move the file to the archive directory found in the config file.

### Logging

This program logs information during each run including the amount of bytes that were transferred to the SFTP server, and any errors should they occur. To prevent the user from having to manually navigate to log files to see run results, the program will automatically send the log contents via **email** upon completion.

Example log:

![Example Log Output](https://awilmes-github-artifacts.s3.amazonaws.com/awilmes-pysftp/log.PNG "Example Log Output")

### Config.toml

The **config.toml** file is the only file that requires manipulation by the user. The following is an overview of the config parameters:

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