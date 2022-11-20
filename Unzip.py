from Huffman import HuffmanUnzip
from LZW import LZWUnzip
from SFPT import SFTP


class Unzip:
    """
    Class to unzip a file.
    Every file should instance a new class.
    """
    def __init__(self, pathToSave: str, nameToSave: str, pathToDownloadFiles: str, memoryLen: int = -1) -> None:
        self.completePathToSave = pathToSave + nameToSave
        self.pathToSave = pathToSave
        self.pathToDownloadFiles = pathToDownloadFiles
        self.huffman = HuffmanUnzip(pathToDownloadFiles, memoryLen,self.completePathToSave)
        self.lzw = LZWUnzip(pathToDownloadFiles, memoryLen,self.completePathToSave)
        self.sftp = SFTP()

    def unzipHuffman(self):
        '''
        Method to unzip using Huffman code
        '''
        self.sftp.downloadFile(r'ZipedFile.huff', self.pathToDownloadFiles + r'\ZipedFile.huff')
        self.sftp.downloadFile(r'HuffmanTree.huff', self.pathToDownloadFiles + r'\HuffmanTree.huff')
        self.huffman.unzip()

    def unzipLZW(self, byteWordLen = 2):
        '''
        Method to unzip using LZW code
        byteWordLen: numbers of bytes that was used to encode the word
        '''
        self.sftp.downloadFile(r'ZipedFile.lzw', self.pathToDownloadFiles + r'\ZipedFile.lzw')
        self.lzw.unzip(byteWordLen)