#!/usr/bin/env python3
"""
Programmer: Andrew Wilmes <awilmes@okstate.edu>
Date: 16 December 2022
"""
# Import custom helper functions from mod.py
from mod import Email, Helpers, Log, Server


def main():

    Log.sys('Starting program.')

    # Verify new file is in source directory
    if not Helpers.file_exists():
        return
    
    # Upload the file and return the directory contents as a list
    list_result = Server.session_put_file()

    # Verify the returned list contains the new file
    result = Server.upload_exists(list_result)

    if not result:
        return
    else:
        # Archive source file
        Helpers.archive()

    Log.info('Emailing log file.')
    Email.send(Email.create())
    Log.sys('Exiting program.')


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        Log.err(ex)
    finally:
        exit()
