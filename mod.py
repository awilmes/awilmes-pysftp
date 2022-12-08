#!/usr/bin/env
import datetime
import os
import paramiko
import shutil
from conf import cfg


def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%S |")


def get_date():
    today = datetime.datetime.today()
    return today.strftime("_%Y%m%d")


def log(str_input):
    with open(file=cfg['client']['log'] + f'{get_date()}.txt', mode='a') as lf:
        lf.write(f'{get_timestamp()} {str_input}\n')


def get_file_name():
    filename = cfg['client']['pattern'] + get_date() + cfg['client']['extension']
    return filename


def verify_source_file():
    filename = get_file_name()
    path_to_verify = cfg['client']['source'] + filename
    if os.path.exists(path_to_verify):
        log('INFO | Found source file! Beginning upload process.')
        return True
    else:
        log('ERROR | Source file not found! Exiting program.')
        return False


def verify_file_upload(list_result):
    filename = get_file_name()
    if filename in list_result:
        log(f'INFO | {filename} was uploaded successfully.')
        return True
    else:
        log(f'ERROR | {filename} upload could not be verified.')
        return False


def archive():
    # archive the transferred file after transfer
    filename = get_file_name()
    source = cfg['client']['source'] + filename
    dest = cfg['client']['archive'] + filename

    # verify file exists before moving (redundant)
    if os.path.exists(source):
        try:
            shutil.move(source, dest)
            # verify file was archived
            if os.path.exists(dest):
                log(f'INFO | {filename} was archived.')
                return True
            else:
                log(f'ERROR | {filename} was not archived.')
                return False
        except Exception as err:
            log(f'ERROR | Archive error: {err}')
            return False
    else:
        log('ERROR | Archive error: Source does not exist (ignore if testing)')
        return False


def count_bytes(partial, total):
    # Callback function for upload method
    log(f'INFO | Total bytes transferred: {partial} / {total}')


def session_put_file():
    # Opens an ssh session for sftp operations
    config = SshConfig()  # get the config file for ssh params
    log('INFO | SSH configuration loaded.')
    log('INFO | Starting SSH session...')
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=config.hostname,
            username=config.username,
            pkey=config.pkey,
            port=config.port
        )
        log('INFO | SSH connected. Starting SFTP session...')
        with ssh.open_sftp() as sftp:
            sftp.chdir(cfg['server']['upload_dir'])
            cwd = sftp.getcwd()
            log(f'INFO | Attempting to upload to {cwd}...')
            sftp.put(
                localpath=cfg['client']['source'] + get_file_name(),
                remotepath=cfg['server']['upload_dir'] + get_file_name(),
                callback=count_bytes
            )
            return sftp.listdir()  # Return a list of files to verify upload


def ssh_self_test():
    # Self test used for testing only
    # Connects to servers and returns cwd
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


class SshConfig:
    # Creates a config context object for ssh
    def __init__(self):
        self.hostname = cfg['server']['host']
        self.username = cfg['server']['user']
        self.pkey = paramiko.RSAKey.from_private_key_file(filename=cfg['client']['key'])
        self.port = cfg['server']['port']

    def get_info(self):
        str_out = f'hostname={self.hostname}\nusername={self.username}\npkey={self.pkey}\nport={self.port}'
        return str_out
