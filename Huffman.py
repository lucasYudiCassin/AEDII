
from collections import Counter
import heapq
import pickle
from datetime import datetime


class Node:
    """
    Node class used to create Huffman Tree to zip the files
    """
    def __init__(self, key, Weight, LeftNode = None, RightNode = None) -> None:
        self.Key = key
        self.Weight = Weight
        self.LeftNode = LeftNode
        self.RightNode = RightNode
        self.IsLeaf = LeftNode == None and RightNode == None
  
    def setLeftNode(self, LeftNode):
        '''
        Method to set Left Node of this Node
        '''
        self.LeftNode = LeftNode
        self.IsLeaf = LeftNode == None and self.IsLeaf

    def setRightNode(self, RightNode):
        '''
        Method to set Right Node of this Node
        '''
        self.RightNode = RightNode
        self.IsLeaf = RightNode == None and self.IsLeaf

    def __lt__(self, other):
        '''
        Method to verify if this node is lower than the passed Node.
        The weigth of the node is the key to compare
        '''
        return self.Weight < other.Weight

class HuffmanZip:
    """
    Huffman class to zip a file. 
    You are able to set the memory length so the code won't pass this limit
    """
    def __init__(self, filePath: str, memoryLen: int = -1, pathSave: str = None):
        self.eof = b'_EOF'
        if pathSave == None:
            raise Exception("You should pass a path to save the files")

        self.pathSave = pathSave
        if memoryLen <= 0:
                self.memoryLen = -1
        else:
            self.memoryLen = int(memoryLen * 0.98) // 2
        try:
            self.file = open(filePath, 'rb')            
        except FileNotFoundError as e:
            raise e
 
    def zip(self) -> str:
        '''
        Method that zip the file
        Return: tuple with complete path of the file ziped and the trees codes
        '''
        
        start = datetime.now()

        fileWrite = open(self.pathSave + r"\ZipedFile.huff", "wb") 
        fileWrite.close()

       
        text = self.file.read(self.memoryLen)
        

        lenText = len(text)
        trees = []
            
        while lenText > 0:
            heap = []
            charFreq = Counter(text).items()        
            for (l, q) in charFreq:
                heapq.heappush(heap, (Node(l, q)))
            treeRoot = self.createTree(heap)
            trees.append(treeRoot)
            c = self.defineCod(treeRoot)
            treeRoot = ''

            fileWrite = open(self.pathSave + r"\ZipedFile.huff", "ab")
            fileWrite.write(bytes(self.transform(text, c)))
            fileWrite.close()

            
            text = self.file.read(self.memoryLen)
            

            lenText = len(text)
        
        pickle.dump(trees,open(self.pathSave + r"\HuffmanTree.huff", "wb"))
        end = datetime.now()
        print(f"Time to zip: {end - start}")
        self.file.seek(0)
        return (self.pathSave + r"\ZipedFile.huff", self.pathSave + r"\HuffmanTree.huff")

    def transform(self, text, dic):
        '''
        Method that tansform the text to a binary sequence.
        This method use bits shift, buffer and yield to save memory to write and encode
        Also adds the EOF binary code by the end of the ziped piece of data, 
        so the unzip code changes the Huffman tree to decode
        '''
        buffer = 0
        size = 0
        eof = dic["'_EOF'"]
        for s in text:
            vA = dic[s]
            b = len(vA)
            v = int(vA, 2)
            buffer = (buffer << b) + v
            size += b
            while size >= 8:
                byte = buffer >> (size - 8)
                yield byte
                buffer = buffer - (byte << (size - 8))
                size -= 8
        
        for i in eof:
            if i == 48:
                buffer = (buffer << 1) + 0
            else:
                buffer = (buffer << 1) + 1
            size += 1
            while size >= 8:
                byte = buffer >> (size - 8)
                yield byte
                buffer = buffer - (byte << (size - 8))
                size -= 8
        if size > 0:
            byte = buffer << (8 - size)
            yield byte
       


    def createTree(self, heap):
        '''
        Method to create the Huffman Tree from a priority queue (created from character frequency)
        This method adds the EOF as the first element of the tree, so it's the biggest binary code
        '''
        eof = Node(repr('_EOF'),0)

        if (len(heap) == 1):
            right = heapq.heappop(heap)
            return Node(repr(''), right.Weight + eof.Weight, eof, right)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(repr(''), right.Weight + eof.Weight, eof, right))
        while len(heap) > 1:      
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            heapq.heappush(heap, Node(repr(''), left.Weight + right.Weight, left, right))
        return heapq.heappop(heap)

    def defineCod(self, treeRoot):
        '''
        Method to create a dictionary of codes from the Huffman Tree
        '''
        visitList = list()
        visitList.append((treeRoot, b''))
        finalList = {}
        while len(visitList) > 0:
            (no, cod) = visitList.pop(0)
            if no.IsLeaf:
                finalList[no.Key] = cod
            else:
                visitList.append((no.LeftNode, cod + b'1'))
                visitList.append((no.RightNode, cod + b'0'))
        return  finalList

class HuffmanUnzip:
    """
    Huffman class to unzip a file. 
    You are able to set the memory length so the code won't pass this limit
    """
    def __init__(self, pathZipedFile: str, memoryLen: int = -1, completePathToSave: str = None) -> None:
        self.eof = b'_EOF'
        self.extraDecode = b''
        self.pathZipedFile = pathZipedFile
        if completePathToSave == None:
            raise Exception("You should pass a path to save the files")

        self.completePathToSave = completePathToSave
        if memoryLen <= 0:
                self.memoryLen = -1
        else:
            self.memoryLen = int(memoryLen * 0.98) // 2

    def unzip(self) -> None:
        '''
        Method that unzip the file.
        '''
        start = datetime.now()
        fileWrite = open(self.completePathToSave, "wb") 
        fileWrite.close()

        
        zipedFile = open(self.pathZipedFile + r"\ZipedFile.huff", "rb")
        

        trees = pickle.load(open(self.pathZipedFile + r"\HuffmanTree.huff", "rb"))
        treeIndex = 0
        
        text = zipedFile.read(self.memoryLen)
        lenText = len(text)
        
        self.extraDecode = b''
        
        while lenText > 0 or len(self.extraDecode) > 0:
            c = trees[treeIndex]
            treeIndex+=1

            fileWrite = open(self.completePathToSave, "ab")
            fileWrite.write(bytes(self.unzipHelper(text, c)))
            fileWrite.close()
            
            text = zipedFile.read(self.memoryLen - len(self.extraDecode))

            lenText = len(text) 
        
        end = datetime.now()
        print(f"Time to unzip: {end - start}")

    def unzipHelper(self, dataBytes, treeRoot):
        '''
        Helper method to unzip.
        This method defined the data as the extra data that become after the EOF, 
        and the new data passed.
        This method use bits shift, buffer and yield to save memory to write and decode
        '''
        data = self.extraDecode + dataBytes
        buffer = 0
        size = 0
        node = treeRoot
        dataIndex = -1

        bufferWrite = 0
        sizeWrite = 0
        for byte in data:
            dataIndex += 1
            buffer = (buffer << 8) + byte
            size += 8
            while size >= 1:
                bit = buffer >> (size - 1)
                buffer = buffer - (bit << (size - 1))
                size -= 1     
                if bit == 1:
                    node = node.LeftNode
                elif bit == 0:
                    node = node.RightNode        
                if node.IsLeaf:
                    if node.Key == "'_EOF'":
                        self.extraDecode = data[dataIndex + 1:]
                        return
                    else:
                        sizeWrite += 8
                        bufferWrite = (bufferWrite << 8) + node.Key
                        while sizeWrite >= 8:
                            byte = bufferWrite >> (sizeWrite - 8) 
                            yield byte
                            bufferWrite = bufferWrite - (byte << (sizeWrite - 8))
                            sizeWrite -= 8                        
                        node = treeRoot