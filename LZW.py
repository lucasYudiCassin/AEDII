
from datetime import datetime

class LZWZip:
    """
    LZW Class to zip a file.
    You are able to set the memory length and the lenght (bytes) to encode the words, 
    so the code won't pass the limit.
    The greater the amount of bytes to encode the word, the greater the memory consumption. 
    It is not linearly related
    """
    def __init__(self, filePath: str, memoryLen: int = -1, pathSave: str = None) -> None:
        self.buffer = None
        if pathSave == None:
            raise Exception("You should pass a path to save the files")
        self.pathSave = pathSave
        try:
            self.file = open(filePath, 'rb')
            if memoryLen <= 0:
                self.memoryLen = -1
            else:
                self.memoryLen = int(memoryLen * 0.98) // 2
                self.file.seek(0)
        except FileNotFoundError as e:
            raise e
 
    def zip(self, byteWordLen = 2) -> str:
        '''
        Method that zip the file.
        byteWordLen: numbers of bytes to be used to encode the sequence
        Return: complete path of the file
        '''
        start = datetime.now()

        self.numBytes = byteWordLen
        self.maxNumDict = pow(2, byteWordLen * 8) - 1

        fileWrite = open(self.pathSave + r"\ZipedFile.lzw", "wb") 
        fileWrite.close()
        self.buffer = self.file.read(self.memoryLen)
        lenText = len(self.buffer)
        
        self.encodeEOF = True
        self.encodeDict = {}
        self.encodePos = 256
        self.bH = b''

        while lenText > 0:
            fileWrite = open(self.pathSave + r"\ZipedFile.lzw", "ab")
            fileWrite.write(bytes(self.zipHelp()))
            fileWrite.close()

            self.buffer = self.buffer + self.file.read(self.memoryLen - len(self.buffer))
            lenText = len(self.buffer)

        fileWrite = open(self.pathSave + r"\ZipedFile.lzw", "ab")
        fileWrite.write(bytes(self.endBH()))
        fileWrite.close()
        end = datetime.now()
        print(f"Time to zip: {end - start}")
        self.file.seek(0)
        return self.pathSave + r"\ZipedFile.lzw"

    def zipHelp(self):
        '''
        Helper method to zip the file.
        This method use the same dictionary until there isn't 
        more bytes to use (limited by the determined length).
        When about to pass the number of bytes to encode the 
        sequence, an EOF symbol is added as the maximum index
        So the extra data is saved for the next round. When 
        the EOF symbol is added, the dictionary is reseted
        This method use bits shift, buffer and yield to save memory to write and encode
        '''
        
        if self.encodeEOF:
            self.encodeDict = {i.to_bytes(1, 'big'): i for i in range(256)}
            self.encodePos = 256
            self.bH = b''
        
        buffer = 0
        size = 0
        pos = -1
        for s in self.buffer:
            pos += 1
            c = s.to_bytes(1, 'big')
            if len(self.bH) == 0 or ((self.bH + c) in self.encodeDict):
                self.bH += c
            else:
                code = self.encodeDict[self.bH]
                self.encodeDict[(self.bH + c)] = self.encodePos
                self.encodePos += 1
                self.bH = c
                sC = self.numBytes * 8
                size += sC
                buffer = (buffer << sC) + code
                while size >= 8:
                    byte = buffer >> (size - 8)
                    yield byte
                    buffer = buffer - (byte << (size - 8))
                    size -= 8
                if self.encodePos >= self.maxNumDict:
                    sC = self.numBytes * 8
                    size += sC
                    buffer = (buffer << sC) + self.maxNumDict
                    while size >= 8:
                        byte = buffer >> (size - 8)
                        yield byte
                        buffer = buffer - (byte << (size - 8))
                        size -= 8
                    self.buffer = self.bH + self.buffer[pos + 1:]
                    self.encodeEOF = True
                    return
        
        self.encodeEOF = False
        self.buffer = b''

    def endBH(self):
        '''
        Helper function to transform to bytes thes extra words on buffer helper.
        '''
        buffer = 0
        size = 0
        if len(self.bH) > 0:
            code = self.encodeDict[self.bH]
            sC = self.numBytes * 8
            size += sC
            buffer = (buffer << sC) + code
            while size >= 8:
                byte = buffer >> (size - 8)
                yield byte
                buffer = buffer - (byte << (size - 8))
                size -= 8
class LZWUnzip:
    """
    LZW Class to unzip a file.
    You are able to set the memory length and the lenght of the 
    word (bytes) that was used to zip, 
    so the code won't pass the limit.
    The greater the amount of bytes that was used to encode the 
    word, the greater the memory consumption. 
    It is not linearly related
    """
    def __init__(self, pathZipedFile: str, memoryLen: int = -1, completePathToSave: str = None) -> None:        
        self.buffer = None        
        self.pathZipedFile = pathZipedFile
        if completePathToSave == None:
            raise Exception("You should pass a path to save the file")
        self.completePathToSave = completePathToSave
        if memoryLen <= 0:
                self.memoryLen = -1
        else:
            self.memoryLen = int(memoryLen * 0.98) // 2
 
    def unzip(self, byteWordLen = 2) -> None:        
        '''
        Method that unzip the file.
        byteWordLen: numbers of bytes to be used to encode the sequence
        '''
        start = datetime.now()

        self.numBytes = byteWordLen
        self.maxNumDict = pow(2, self.numBytes * 8) - 1

        fileWrite = open(self.completePathToSave, "wb") 
        fileWrite.close()

        zipedFile = open(self.pathZipedFile + r"\ZipedFile.lzw", "rb")        
        
        self.buffer = zipedFile.read(self.memoryLen)
        lenText = len(self.buffer)

        self.decodeEOF = True
        self.decodeDict = {}
        self.decodePos = 256
        self.lb = 0

        while lenText > 0:
            fileWrite = open(self.completePathToSave, "ab")
            fileWrite.write(bytes(self.unzipHelper()))
            fileWrite.close()
            self.buffer = self.buffer + zipedFile.read(self.memoryLen - len(self.buffer))
            lenText = len(self.buffer)
        
        end = datetime.now()
        print(f"Time to unzip: {end - start}")

    def unzipHelper(self):
        '''
        Helper method to unzip the file.
        This method use the same dictionary until find the EOF symbol, 
        determinate from the number of bytes used to encode the words.
        When is the EOF symbol the method stops and save the extra data to the next round.
        Every time the EOF symbol is found, the dictionary is reseted
        This method use bits shift, buffer and yield to save memory to write and decode
        '''
        start = 0
        if self.decodeEOF:
            self.decodeDict = {i : i.to_bytes(1, 'big') for i in range(256)}
            self.decodePos = 256
            self.lb = int.from_bytes(self.buffer[0:self.numBytes], byteorder="big")
            start = self.numBytes
            yield self.lb

        buffer = 0
        size = 0
        li = 0
        for i in  range(start, len(self.buffer), self.numBytes):
            sb = int.from_bytes(self.buffer[i:i+self.numBytes], byteorder="big")
            if sb == self.maxNumDict:
                self.buffer = self.buffer[i+self.numBytes:]
                self.decodeEOF = True
                return
            if sb in self.decodeDict:
                cb = self.decodeDict[sb]
                pb = self.decodeDict[self.lb]
                ta = cb[0].to_bytes(1, 'big')
                self.decodeDict[self.decodePos] = (pb + ta)
                self.decodePos += 1
                sCB = len(cb) * 8
                size += sCB
                buffer = (buffer << sCB) + int.from_bytes(cb, byteorder="big")
                while size >= 8:                             
                    byte = buffer >> (size - 8)  
                    yield byte
                    buffer = buffer - (byte << (size - 8))
                    size -= 8
            else:
                pb = self.decodeDict[self.lb]
                ta = pb[0].to_bytes(1, 'big')
                cb = pb + ta
                self.decodeDict[self.decodePos] = cb
                self.decodePos += 1
                sCB = len(cb) * 8
                size += sCB
                buffer = (buffer << sCB) + int.from_bytes(cb, byteorder="big")
                while size >= 8:
                    byte = buffer >> (size - 8) 
                    yield byte
                    buffer = buffer - (byte << (size - 8))
                    size -= 8
            self.lb = sb
            li = i
        self.decodeEOF = False
        self.buffer = self.buffer[li + self.numBytes:]