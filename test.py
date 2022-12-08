#!/usr/bin/env
import unittest
import os

from .. import myConfig as CFG
from mod.mod import Helpers, ServerFuncs

class TestHelpers(unittest.TestCase):
    
    def test_log_path(self):
        """
        Tests log function by returning path from config file
        """
        data = CFG['client']['log'] + f'{Helpers.getDate()}.txt'
        result = CFG['client']['log'] + f'{Helpers.getDate()}.txt'
        print(f'Result = {result}')
        self.assertEqual(result, data)

    def test_archive(self):
        """
        Tests archive functionality (file must be in source dir)
        """
        result = Helpers.archive()
        self.assertEqual(result, True)

    def test_verifySourceFile(self):
        """
        Tests that source file exists before beginning operation
        """
        result = Helpers.verifySourceFile()
        self.assertEqual(result, True)
        
    def test_verifyFileUpload(self):
        """
        Tests upload verification
        """
        # Create a sample list to test function
        sampleList = []
        filename = Helpers.getFileName()        
        sampleList.append(filename)
        data = Helpers.verifyFileUpload(sampleList)
        self.assertEqual(data, True)

class TestServer(unittest.TestCase):

    def test_sshSelfTest(self):
        """
        Tests creating a new ssh session by returning cwd of server
        """
        result = ServerFuncs.sshSelfTest() + '/'
        data = CFG['server']['upload_dir']
        self.assertEqual(result, data)

    def test_confirmUpload(self):
        """
        Tests file upload by uploading file to sftp server,
        and returning a list of files on the server.
        Note: If file is already archived, test will fail.
        """
        result = ServerFuncs.sessionPutFile()
        data = Helpers.getFileName()
        self.assertIn(data, result)

    def test_sshClient(self):
        """
        Tests that sshClient object contains config params
        """
        ssh = ServerFuncs.sshConfig()
        hostname = CFG['server']['host']
        username = CFG['server']['user']
        port = CFG['server']['port']

        self.assertEqual(hostname, ssh.hostname)
        self.assertEqual(username, ssh.username)
        self.assertEqual(port, ssh.port)

    def test_sshClient_getInfo(self):
        """
        Tests getInfo method of sshClient
        """
        ssh = ServerFuncs.sshConfig()
        info = ssh.getInfo()
        print(info)

    def test_sshClient_callback(self):
        """
        Tests callback method 'countBytes'
        (logs output)
        """
        sample = ['0123456789', '9876543210']
        ServerFuncs.countBytes(sample[0], sample[1])      

class TestConfig(unittest.TestCase):

    def test_config_exists(self):
        """
        Tests that a config file exists and is accessible
        """
        data = os.path.exists('./config/config.toml')
        self.assertEqual(True, data)

if __name__ == '__main__':
    unittest.main()