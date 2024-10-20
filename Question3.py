#-------------------------------------------------------------------------
# AUTHOR: Logan Gravitt
# FILENAME: db_connection_mongo_solution
# SPECIFICATION: Accesses and changes a mongoDB database
# FOR: CS 4250- Assignment #2
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient

def connectDataBase():

    client = MongoClient('localhost', 27017)
    db = client['documents']
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
   docText = docText.lower()
   docText = ''.join(char for char in docText if char.isalnum() or char.isspace())
   
   terms = docText.split(" ")
   termCount = {}

    # create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
   for term in terms:
      if term:
       termCount[term] = termCount.get(term, 0)+1
    
   termList = []
   termsSorted = sorted(termCount.items())
   for term, count in termsSorted:
      termList.append({'term' : term,'count' : count, 'num_chars' : len(term)})


    #Producing a final document as a dictionary including all the required fields
   finalDocument = {
       'docId' : docId,
       'text' : docText,
       'title' : docTitle,
       'date' : docDate,
       'category' : docCat,
       'terms' : termList,
    }

    # Insert the document
   col.insert_one(finalDocument)

def deleteDocument(col, docId):

    # Delete the document from the database
    col.delete_one({'docId' : docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    col.delete_one({'docId' : docId})

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
    # We are simulating an inverted index here in memory. 
    index = {}
    documents = col.find()

    for doc in documents:
       for termData in doc['terms']:
          term = termData['term']
          count = termData['count']
          title = doc['title']
          if term not in index:
             index[term] = []
          formatArg = f"{title}:{count}"
          index[term].append(formatArg)

    for term in index:
       index[term] = ','.join(index[term])

    indexSorted = dict(sorted(index.items()))

    return indexSorted
