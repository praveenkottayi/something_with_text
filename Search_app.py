import sys
import os

from whoosh.fields import Schema, TEXT, STORED
from whoosh.index import create_in, open_dir
from whoosh.query import *

#creating the schema
schema = Schema(name=TEXT(stored=True))

#creating the index
if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index",schema)
ix = open_dir("index")
writer = ix.writer()
writer.add_document(name=u"Absolutely nobody disputes the potential value of big data. It provides an economic way to ask new analytics questions that we were never able to ask before.")
writer.add_document(name=u"Methylophilus methylotrophus Jenkins et al. 1987")
writer.add_document(name=u"Chondromyces lichenicolus") 
writer.commit()

from whoosh.qparser import QueryParser
ix=open_dir("index")
with ix.searcher() as searcher:
    query = QueryParser("name", ix.schema).parse(u'data')
    results = searcher.search(query)
    for result in results:
        print(result)
		
		
mytext = 'Chondromyces'
with ix.searcher() as s:
    keywords = [keyword for keyword, score in s.key_terms_from_text("name", mytext)]
    print(str(keywords))
		


