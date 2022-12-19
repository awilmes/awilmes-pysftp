#!/usr/bin/env python3
import datetime
import os
import paramiko
import shutil

from email.message import EmailMessage
from smtplib import SMTP_SSL

from conf import cfg


class Server:
    """
    Namespace for server functions
    """

    def session_put_file():
        """
        Opens an ssh session for sftp operations.
        """
         
        config = SshConfig()  # get the config file for ssh params
        Log.info('SSH configuration loaded.')
        Log.info('Starting SSH session.')
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=config.hostname,
                username=config.username,
                pkey=config.pkey,
                port=config.port
            )
            Log.info('SSH connected. Starting SFTP session.')
            with ssh.open_sftp() as sftp:
                sftp.chdir(cfg['server']['upload_dir'])
                cwd = sftp.getcwd()
                Log.info(f'Attempting to upload to {cwd}.')
                sftp.put(
                    localpath=cfg['client']['source'] + Helpers.get_file_name(),
                    remotepath=cfg['server']['upload_dir'] + Helpers.get_file_name(),
                    callback=Server.count_bytes
                )
                return sftp.listdir()  # Return a list of files to verify upload
    
    
    def count_bytes(partial, total):
        """
        Callback function for SFTP upload method.
        """
        Log.info(f'Total bytes transferred: {partial} / {total}')


    def upload_exists(list_result):
        """
        Takes a list of SFTP destination contents to verify file upload.
        """
        filename = Helpers.get_file_name()
        if filename in list_result:
            Log.info(f'{filename} was uploaded successfully.')
            return True
        else:
            Log.err(f'{filename} upload could not be verified.')
            return False


    def ssh_self_test():
        """
        Self test used for testing only!
        Connects to servers and returns cwd.
        """
        config = SshConfig()
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=config.hostname,
                username=config.username,
                pkey=config.pkey,
                port=config.port
            )
            with ssh.open_sftp() as sftp:
                sftp.chdir(cfg['server']['upload_dir'])
                cwd = sftp.getcwd()

        return cwd


class Log:
    """
    Namespace for log functions.
    """

    def info(input):
        """
        Logs info to a file based on config params
        """
        i = ''
        with open(file=cfg['client']['log'] + f'{Helpers.get_date()}.log', mode='a') as lf:
            lf.write(f'{Helpers.get_timestamp()} {i:-^16} {input:.<50}\n')

    
    def err(input):
        """
        Logs errors to a file based on config params
        """
        e = 'ERROR'
        with open(file=cfg['client']['log'] + f'{Helpers.get_date()}.log', mode='a') as lf:
            lf.write(f'{Helpers.get_timestamp()} {e:-^16} {input}\n')

    def sys(input):
        """
        Logs program benchmarks to a file based on config params
        """
        s = ''
        with open(file=cfg['client']['log'] + f'{Helpers.get_date()}.log', mode='a') as lf:
            lf.write(f'{Helpers.get_timestamp()} {s:-^16} {input:-^50}\n')


class Helpers:
    """
    Namespace for helper functions.
    """

    def file_exists():
        """
        Verifies whether the source file exists and returns a boolean value
        """
        filename = Helpers.get_file_name()
        path_to_verify = cfg['client']['source'] + filename
        if os.path.exists(path_to_verify):
            Log.info('Found source file! Beginning upload process.')
            return True
        else:
            Log.err('Source file not found! Exiting program.')
            return False

    
    def get_file_name():
        """
        Gets the name of the current file based on config params.
        """
        filename = cfg['client']['pattern'] + Helpers.get_date() + cfg['client']['extension']
        return filename


    def get_timestamp():
        """
        Gets the current date and time
        """
        now = datetime.datetime.now()
        return now.strftime("[%Y-%m-%d][%H:%M:%S]")


    def get_date():
        """
        Gets the current date as a formatted string with leading underscore.
        """
        today = datetime.datetime.today()
        return today.strftime("_%Y%m%d")


    def archive():
        """
        Archives the current working file based on config params.
        """
        # archive the transferred file after transfer
        filename = Helpers.get_file_name()
        source = cfg['client']['source'] + filename
        dest = cfg['client']['archive'] + filename

        try:
            shutil.move(source, dest)
            # verify file was archived
            if os.path.exists(dest):
                Log.info(f'{filename} was archived.')
                return True
            else:
                Log.err(f'{filename} was not archived.')
                return False
        except Exception as err:
            Log.err(f'Archive error: {err}')
            return False


class SshConfig:
    """
    Creates a config context object for ssh operations
    """

    def __init__(self):
        self.hostname = cfg['server']['host']
        self.username = cfg['server']['user']
        self.pkey = paramiko.RSAKey.from_private_key_file(filename=cfg['client']['key'])
        self.port = cfg['server']['port']

    def get_info(self):
        str_out = f'hostname={self.hostname}\nusername={self.username}\npkey={self.pkey}\nport={self.port}'
        return str_out


class Email:
    """
    Namespace for email functions
    """

    def create():
        """
        Reads the log file and returns an email message object with its contents
        """
        # Read the file and build the message object
        with open(f"{cfg['client']['log']}{Helpers.get_date()}.log") as lf:
            msg = EmailMessage()
            msg.set_content(lf.read()+'\n\nThis message was sent using Python.')

        msg['Subject'] = 'Log - pysftp'
        msg['From'] = cfg['smtp']['user']
        msg['To'] = cfg['smtp']['recipient']

        return msg


    def send(msg):
        """
        Sends the message object passed to this function
        """
        # Use SSL port
        port = cfg['smtp']['port']
        host = cfg['smtp']['host']
        user = cfg['smtp']['user']
        password = cfg['smtp']['password']

        # Create SSL connection object
        try:
            ssl = SMTP_SSL(host, port)
            ssl.login(user, password)
            ssl.send_message(msg)
        except Exception as ex:
            print(ex)
        finally:
            ssl.quit()