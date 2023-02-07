# PySFTP

## Description



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