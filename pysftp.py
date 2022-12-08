#!/usr/bin/env
from mod import log, verify_source_file, session_put_file, verify_file_upload, archive


def main():
    log('INFO | Program starting...')
    # Verify new file is in source directory
    if verify_source_file():
        # Upload the file and return the directory contents as a list
        list_result = session_put_file()
        # Verify the returned list contains the new file
        if verify_file_upload(list_result):
            # Archive source file
            if archive():
                log('INFO | Program exiting...')


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        log(f'ERROR | MAIN | {err}')
