#!/usr/bin/env
from mod import Helpers, Log, Server


def main():
    Log.log('INFO | Program starting...')
    # Verify new file is in source directory
    if Helpers.file_exists():
        # Upload the file and return the directory contents as a list
        list_result = Server.session_put_file()
        # Verify the returned list contains the new file
        if Server.upload_exists(list_result):
            # Archive source file
            if Helpers.archive():
                Log.log('INFO | Program exiting...')


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        Log.log(f'ERROR | MAIN | {err}')
