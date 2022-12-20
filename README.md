# PySFTP

## Description

The motivation for this project was to eliminate the manual labor associated with uploading a daily report to an SFTP server. Before, the user was required to save a .csv attachment from their Outlook inbox to their local machine, upload the file to an SFTP server using a program like WinSCP, and then archive the file. By configuring this program to run using a service account, reliable daily automation can be acheived independent of external factors such as staff turnover.

## Features

### Basic Overview

This project takes a modular approach to solving the aforementioned issue. The present code is independent of any hard-coded values: Log path, source file path, archive path, **RSA** key path, file name, and file extension, are input by the user into the config.toml file during the initial setup. In addition, the config.toml file also contains server parameters such as the host, user, port, and upload directory, as well as SMTP parameters for transmitting log files upon completed execution.

The program determines the correct file to upload by searching the source directory for a file name matching the following syntax:

`<Name>_<Current Date>.<Extension>`

*Ex: `AwardSpring_20221013.csv`*

If the target file is not to be found, the program will log the error and exit. Upon a successful execution, the program will move the file to the archive directory found in the config file.

### Logging

This program logs information during each run including the amount of bytes that were transferred to the SFTP server, and any errors should they occur. To prevent the user from having to manually navigate to log files to see run results, the program will automatically send the log contents via **email** upon completion.

Example log:

![Example Log Output](https://awilmes-github-artifacts.s3.amazonaws.com/awilmes-pysftp/log.PNG "Example Log Output")


