#!/usr/bin/env
import datetime
import os
import paramiko
import shutil

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
        Log.log('INFO | SSH configuration loaded.')
        Log.log('INFO | Starting SSH session...')
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=config.hostname,
                username=config.username,
                pkey=config.pkey,
                port=config.port
            )
            Log.log('INFO | SSH connected. Starting SFTP session...')
            with ssh.open_sftp() as sftp:
                sftp.chdir(cfg['server']['upload_dir'])
                cwd = sftp.getcwd()
                Log.log(f'INFO | Attempting to upload to {cwd}...')
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
        Log.log(f'INFO | Total bytes transferred: {partial} / {total}')


    def upload_exists(list_result):
        """
        Takes a list of SFTP destination contents to verify file upload.
        """
        filename = Helpers.get_file_name()
        if filename in list_result:
            Log.log(f'INFO | {filename} was uploaded successfully.')
            return True
        else:
            Log.log(f'ERROR | {filename} upload could not be verified.')
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
            Log.log('INFO | Found source file! Beginning upload process.')
            return True
        else:
            Log.log('ERROR | Source file not found! Exiting program.')
            return False

    
    def get_file_name():
        """
        Gets the name of the current file based on config params
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
        Gets the current date as a formatted string
        """
        today = datetime.datetime.today()
        return today.strftime("_%Y%m%d")


    def archive():
        """
        Archives the current working file based on config params
        """
        # archive the transferred file after transfer
        filename = Helpers.get_file_name()
        source = cfg['client']['source'] + filename
        dest = cfg['client']['archive'] + filename

        try:
            shutil.move(source, dest)
            # verify file was archived
            if os.path.exists(dest):
                Log.log(f'INFO | {filename} was archived.')
                return True
            else:
                Log.log(f'ERROR | {filename} was not archived.')
                return False
        except Exception as err:
            Log.log(f'ERROR | Archive error: {err}')
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
