# Python 2.7.3
# -*- coding: latin-1 -*-
import re
import os
import collections
import time

# This is the map where dictionary terms will be stored as keys and value will be posting list with position in the file
dictionary = {}
# This is the map of docId to input file name
docIdMap = {}

def getGamma(b):
        a=bin(b)[3:]
        c='0'
        for x in a:
            c= '1'+c
        ans=c+a
        return ans
    
def getNum(b):
    n=len(b)/2
    n=int(n)
    b=b[n+1:]
    b='1'+b
    b=int(b,2)
    return b

class index:
    def __init__(self, path):
        self.path = path
        pass

    def buildIndex(self):

        docId = 1
        fileList = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for eachFile in fileList:
            position = 1
            # docName = "Doc_Id_" + str(docId)
            # docName =  str(docId)
            docIdMap[docId] = eachFile
            lines = [line.rstrip('\n') for line in open(self.path + "/" + eachFile)]

            for eachLine in lines:
                wordList = re.split('\W+', eachLine)

                while '' in wordList:
                    wordList.remove('')

                for word in wordList:
                    if (word.lower() in dictionary):
                        postingList = dictionary[word.lower()]
                        if (docId in postingList):
                            postingList[docId].append(position)
                            position = position + 1
                        else:
                            postingList[docId] = [position]
                            position = position + 1
                    else:
                        dictionary[word.lower()] = {docId: [position]}
                        position = position + 1
            docId = docId + 1

    def and_query(self, query_terms):
        if len(query_terms) == 1:
            resultList = self.getPostingList(query_terms[0])
            if not resultList:
                print ""
                printString = "Result for the Query : " + query_terms[0]
                print printString
                print "0 documents returned as there is no match"
                return

            else:
                print ""
                printString = "Result for the Query : " + query_terms[0]
                print printString
                print "Total documents retrieved : " + str(len(resultList))
                for items in resultList:
                    print docIdMap[items]

        else:
            resultList = []
            for i in range(1, len(query_terms)):
                if (len(resultList) == 0):
                    resultList = self.mergePostingList(self.getPostingList(query_terms[0]),
                                                       self.getPostingList(query_terms[i]))
                else:
                    resultList = self.mergePostingList(resultList, self.getPostingList(query_terms[i]))
            print ""
            printString = "Result for the Query(AND query) :"
            i = 1
            for keys in query_terms:
                if (i == len(query_terms)):
                    printString += " " + str(keys)
                else:
                    printString += " " + str(keys) + " AND"
                    i = i + 1

            print printString
            print "Total documents retrieved : " + str(len(resultList))
            for items in resultList:
                print docIdMap[items]

    def getPostingList(self, term):
        if (term in dictionary):
            postingList = dictionary[term]
            keysList = []
            for keys in postingList:
                keysList.append(keys)
            keysList.sort()
            # print keysList
            return keysList
        else:
            return None

    def mergePostingList(self, list1, list2):

        mergeResult = list(set(list1) & set(list2))
        mergeResult.sort()
        return mergeResult

    def print_dict(self):
        # function to print the terms and posting list in the index
        fileobj = open("invertedIndex.txt", 'w')
        for key in dictionary:
            print key + " --> " + str(dictionary[key])
            fileobj.write(key + " --> " + str(dictionary[key]))
            fileobj.write("\n")
        fileobj.close()

    def print_doc_list(self):
        for key in docIdMap:
            print "Doc ID: " + str(key) + " ==> " + str(docIdMap[key])

    

    def convert_docID(self):
        fileobj = open('diffIndex.txt', 'a')
        fileobjre = open('reconstruct.txt', 'a')
        for w in dictionary:
            plist = dictionary[w]
            od = collections.OrderedDict(sorted(plist.items()))
            diff = []
            diff2 = []
            const = []
            gammaDiff = ""
            gammaDiffnew = []
            f=0
            for key in od.keys():
                diff.append(key)
            gammaDiffnew.append(getGamma(diff[0]))
            diff2.append(getGamma(diff[0]))
            
            if len(diff) >1:
            	for i in range(1, len(diff)):
                	diff2.append(getGamma(diff[i] - diff[i-1]))
                	print "appended i= "+str(i)+" and len= "+ str(len(diff2))
                	diff[i] = abs(diff[i] - diff[i-1])
                	if gammaDiff==None or gammaDiff=="":
                		gammaDiffnew.append(getGamma(diff[i]))
                		f=1
                	else:
                		gammaDiffnew = gammaDiff.split();
                		gammaDiffnew.append(getGamma(diff[i]))
                		f=1
                if f==0:
                	gammaDiffnew.append(getGamma(diff[0]))
            if gammaDiff==None:
            	gammaDiffnew.append(getGamma(diff[0]))
            print gammaDiff
            fileobj.write(str(w) +" -> "+str(gammaDiffnew))
            fileobj.write("\n")

            #for reconstruction........
            const.append(getNum(diff2[0]))
            #print getNum(diff2[0])
            #print "len(diff2)  " +str(len(diff2))
            if len(diff2) >1:
            	for i in range(0,len(diff2)-1):
                	const.append((getNum(diff2[i]) + getNum(diff2[i+1])))
                	#diff[i] = abs(diff[i] - diff[i-1])
                	#print "getNum: i="+ str(i)+"--"+str(getNum(str(diff[i] + diff[i+1])))
            print "diff2- "+str(w) +" -> "+str(const)
            fileobjre.write(str(w) +" -> "+str(const))
            fileobjre.write("\n")
        fileobjre.close()
        fileobj.close()

def main():
    docCollectionPath = raw_input("Enter path of text file collection : ")
    queryFile = raw_input("Enter path of query file : ")
    indexObject = index(docCollectionPath)
    indexObject.buildIndex()

    print ""
    print "Inverted Index :"
    indexObject.print_dict()

    print ""
    print "Document List :"
    indexObject.print_doc_list()
    print ""


    QueryLines = [line.rstrip('\n') for line in open(queryFile)]
    for eachLine in QueryLines:
        wordList = re.split('\W+', eachLine)

        while '' in wordList:
            wordList.remove('')

        wordsInLowerCase = []
        for word in wordList:
            wordsInLowerCase.append(word.lower())
        indexObject.and_query(wordsInLowerCase)
    #print "sorting*"
    indexObject.convert_docID()

    qterm = wordList[0]
    file1 = open("invertedIndex.txt", 'r')
    for line in file1:
        if qterm in line:
            print "Intverted Index : " + line

    file1.close()
    file2 = open("diffIndex.txt", 'r')
    for line in file2:
        if qterm in line:
            print "Compressed Index : " + line
    file2.close()


if __name__ == '__main__':
    main()
