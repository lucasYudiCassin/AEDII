from Zip import Zip
from Unzip import Unzip


def runStats(filesList: list) -> None:
    '''
    Helper function to run the zip and unzip. 
    This function uses more memory than the memory limit and LZW word length,
    because this open all files to compare theis sizes and contents.
    filesList: list of tuples of files to zip. (file name, memory limit, LZW word length, 
    indicator to run Huffman algorithm, indicator to run LZW algorithm)
    All files should be at the path: '.\\files\\OriginalFiles'
    All files will be unziped at the path: '.\\files\\UnzipedFiles'
    '''
    for (file, ml, lzwLen, runHuffman, runLZW) in filesList:
        pathZipedFiles = r".\files\ZipedFiles"
        pathDownloadedZipedFiles = r".\files\DownloadedZipedFiles"
        pathUnzipedFiles = r".\files\UnzipedFiles"


        textOriginal = r".\files\OriginalFiles" + file


        memoryLen = ml
        lzwByteWordLen = lzwLen

        zipText = Zip(textOriginal, pathZipedFiles, memoryLen)
        unzipText100 = Unzip(pathUnzipedFiles, file, pathDownloadedZipedFiles, memoryLen)

        originalFile = open(textOriginal, 'rb').read()
        print("===================================================")
        print(f"File: {file}")
        print(f"Memory Len: {memoryLen}")
        if runHuffman:
            print("===================== Huffman =====================")
            zipText.zipHuffman()
            zipedFile = len(open(pathZipedFiles + r"\ZipedFile.huff", 'rb').read())
            treeFile = len(open(pathZipedFiles + r"\HuffmanTree.huff", 'rb').read())
            unzipText100.unzipHuffman()
            unzipedFile = open(pathUnzipedFiles + file, 'rb').read()
            print(f"*** Results:\n     Len Original file: {len(originalFile)}\n     Len Ziped File: {zipedFile}\n     RC: {zipedFile/len(originalFile)}\n     Len tree file: {treeFile}\n     RC2: {(zipedFile+treeFile)/len(originalFile)}\n     Len Unziped File: {len(unzipedFile)}\n     Are they equal: {unzipedFile == originalFile}")


        if runLZW:
            print("======================= LZW =======================")
            print(f"Word Len: {lzwByteWordLen}")
            zipText.zipLZW(lzwByteWordLen)
            zipedFile = len(open(pathZipedFiles + r"\ZipedFile.lzw", 'rb').read())
            unzipText100.unzipLZW(lzwByteWordLen)
            unzipedFile = open(pathUnzipedFiles + file, 'rb').read()
            print(f"*** Results:\n     Len Original file: {len(originalFile)}\n     Len Ziped File: {zipedFile}\n     RC: {zipedFile/len(originalFile)}\n     Len Unziped File: {len(unzipedFile)}\n     Are they equal: {unzipedFile == originalFile}")

def zip(fileName, memoryLen, lzwByteWordLen, runHuffman = True):
        '''
        helper function to zip the file at the path: '.\files\ZipedFiles'
        fileName: name of the file at the main path
        memoryLen: memory limit (bytes)
        lzwByteWordLen: length to use to enconde the words using LZW
        runHuffman: if True the Huffman code will be used, if Falsem the LZW code will be used
        '''
        pathZipedFiles = r".\files\ZipedFiles"       


        textOriginal = r".\files\OriginalFiles" + fileName


        zipText = Zip(textOriginal, pathZipedFiles, memoryLen)

        print("===================================================")
        print(f"File: {fileName}")
        print(f"Memory Len: {memoryLen}")
        if runHuffman:
            print("===================== Huffman =====================")
            zipText.zipHuffman()
        else:
            print("======================= LZW =======================")
            print(f"Word Len: {lzwByteWordLen}")
            zipText.zipLZW(lzwByteWordLen)

def unzip(fileName, memoryLen, lzwByteWordLen, runHuffman = True):
        '''
        helper function to unzip the file at the path: '.\\files\\UnzipedFiles'
        fileName: name of the file to save at the main path
        memoryLen: memory limit (bytes)
        lzwByteWordLen: length that was used to enconde the words using LZW
        runHuffman: if True the Huffman code will be used, if Falsem the LZW code will be used
        '''
        pathDownloadedZipedFiles = r".\files\DownloadedZipedFiles"
        pathUnzipedFiles = r".\files\UnzipedFiles"

        unzipText100 = Unzip(pathUnzipedFiles, fileName, pathDownloadedZipedFiles, memoryLen)

        
        print("===================================================")
        print(f"File: {fileName}")
        print(f"Memory Len: {memoryLen}")
        if runHuffman:
            print("===================== Huffman =====================")
            unzipText100.unzipHuffman()
        else:
            print("======================= LZW =======================")
            print(f"Word Len: {lzwByteWordLen}")
            unzipText100.unzipLZW(lzwByteWordLen)

'''
You can use runStats to print all statistics or
use zip and unzip to just upload or download the files

Atention:
You should change the SFTP.py to your own SFTP server. 
Also should create the path ./root/ZipedFiles on the remote path of your server

'''
texts = [
    (r"\txt100KB.txt", 20000, 2, True, True),
    (r"\txt1MB.txt", 210000, 2, True, True),

    (r"\pdf82KB.pdf", 16000, 2, True, True),
    (r"\pdf1MB.pdf", 210000, 2, True, True),
    (r"\pdf1MB.pdf", 210000, 3, False, True),

    (r"\png4MB.png", 1000000000, 2, True, True),
    (r"\png4MB.png", 1000000000, 3, False, True)

]

runStats(texts)


zip(r"\txt100KB.txt", 210000, 2, True)
unzip(r"\txt100KB.txt", 210000, 2, True)




