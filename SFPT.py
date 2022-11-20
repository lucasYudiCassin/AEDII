import pysftp

class SFTP:
    """
    Helper class to upload and download ziped files.
    Uses pysftp library to connect, upload and download.
    """
    def __init__(self, hostname = 'localhost', port = 22, username = 'client', password = 'password') -> None:
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.cnOpts = pysftp.CnOpts()
        self.cnOpts.hostkeys = None
        

    def uploadFile(self, pathFile: str):
        '''
        Method to upload files to remote path: './root/ZipedFiles'
        pathFile: complete path of the file to upload
        '''
        try:
            with pysftp.Connection(host=self.hostname, port = self.port, username=self.username, password=self.password, cnopts=self.cnOpts) as sftp:
                sftp.cwd('./root/ZipedFiles')
                sftp.put(pathFile, preserve_mtime=True)
                print("Uploaded with success")
                sftp.close()
        except Exception as e:
            raise e
       
            
    
    def downloadFile(self, fileName: str, pathToSave: str):
        '''
        Method to download file from path: './root/ZipedFiles'
        fileName: name of the file to download
        pathToSave: complete path to save the file
        '''
        try:
            with pysftp.Connection(host=self.hostname, port = self.port, username=self.username, password=self.password, cnopts=self.cnOpts) as sftp:
                sftp.cwd('./root/ZipedFiles')
                sftp.get(remotepath='./' + fileName, localpath=pathToSave, preserve_mtime=False)
                print("Downloaded with success")
                sftp.close()
        except Exception as e:
            raise e    