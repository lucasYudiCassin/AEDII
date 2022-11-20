from Huffman import HuffmanZip
from LZW import LZWZip
from SFPT import SFTP


class Zip:
    """
    Class to zip a file.
    Every file should instance a new class.
    """
    def __init__ (self, pathOriginalFileComplete: str, pathSaveZipedFile: str, memoryLen: int = -1) -> None:
        self.huffman = HuffmanZip(pathOriginalFileComplete, memoryLen, pathSaveZipedFile)
        self.lzw = LZWZip(pathOriginalFileComplete, memoryLen, pathSaveZipedFile)
        self.sftp = SFTP()

    def zipHuffman(self):
        '''
        Method to zip using Huffman code
        '''
        (pathFile, pathTree) = self.huffman.zip()
        self.sftp.uploadFile(pathFile)
        self.sftp.uploadFile(pathTree)
    
    def zipLZW(self, byteWordLen = 2):
        '''
        Method to zip using LZW code
        byteWordLen: numbers of bytes to be used to encode the sequence
        '''
        pathFile = self.lzw.zip(byteWordLen)
        self.sftp.uploadFile(pathFile)