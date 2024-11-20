from __future__ import print_function
import logging
import numpy as np
import sys
import matplotlib.pyplot as plt
import csv
import string
import re
import sys
import codecs
from tkinter import *
import random
#import spacy
from textblob import TextBlob
import sys
from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from tkinter import Tk, ttk, Frame, Button, Label, Entry, Text, Checkbutton, \
    Scale, Listbox, Menu, BOTH, RIGHT, RAISED, N, E, S, W, \
    HORIZONTAL, END, FALSE, IntVar, StringVar, messagebox as box

	
	
def load_news_from_csv():
    with open("IRC_News_data.csv",'r') as my_file:  # sub_News_data_test.csv ,,encoding="utf8"
        reader = csv.reader(my_file, delimiter=',')
        news_data_test = list(reader)
    random_news_generator = random.randint(1,len(news_data_test)-1)
    print(news_data_test[random_news_generator][2])
    return news_data_test[random_news_generator][2]
		
def news_classifier(x):    
    from sklearn.externals import joblib      
    vec_loaded = joblib.load('IRC_vectorizer.pkl')   
    clf_loaded = joblib.load('IRC_classifier.pkl')
    x = vec_loaded.transform(x).toarray()
    class_output_NB = clf_loaded.predict(x)
    class_description = " "
    if class_output_NB == '1':
        class_description = "ABIM"
    if class_output_NB == '2':
        class_description = "IOT"
    if class_output_NB == '3':
        class_description = "ETCU"
    if class_output_NB == '4':
        class_description = "Mobility"     
    return class_description

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="skyblue")
        self.parent = parent
        self.parent.title("NEWS ANALYZER")
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.centreWindow()
        self.pack(fill=BOTH, expand=1)

        textNameLabel = Label(self, text="Enter text (News) :",font=('Helvetica 16 bold'), bg= "sky blue")
        textNameLabel.grid(row=0, column=0, padx=(100,10), pady=(100,10))

        textNameText = Entry(self, width=80)
        textNameText.grid(row=0, column=1, pady=(100,20))
		
        #fromCsvText = Text(self, width=30 , height = 3)
        #fromCsvText.grid(row=1, column=1, pady=(100,20))
        
        classNameLabel = Label(self, text="Category :", font=('Helvetica 16 bold'), bg= "sky blue")
        classNameLabel.grid(row=2, column=2)

        entityNameLabel = Label(self, text="Entities :", font=('Helvetica 16 bold'), bg= "sky blue")
        entityNameLabel.grid(row=2, column=0)

        entityNameLabel = Label(self, text="Sentiment :", font=('Helvetica 16 bold'), bg= "sky blue")
        entityNameLabel.grid(row=2, column=1)        

        okBtn = Button(self, text="ANALYZE", width=15, bg= "green", font=('Helvetica 16 bold'), command= lambda: self.onConfirm(textNameText.get()))
        okBtn.grid(row=0, column=2,padx = 5, pady=(100,10))
		
        okBtn = Button(self, text="get NEWS >>", width=15, bg= "yellow", font=('Helvetica 16 bold'), command= lambda: self.getNews())
        okBtn.grid(row=1, column=0,padx = 5, pady=(100,10))		

    def centreWindow(self):
        w = 1200
        h = 500
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def onConfirm(self,s):
        #box.showinfo("Information", s)
        self.update_idletasks()       
        S= [s]        
        output_class = news_classifier(S)
        print(output_class)
        getNewsLabel = Label(self, text= "..............................."*32, font=('Helvetica 10'), bg= "sky blue", wraplength=500)
        getNewsLabel.grid(row=1, column=1)
        getNewsLabel = Label(self, text= s, font=('Helvetica 10'), bg= "sky blue", wraplength=500)
        getNewsLabel.grid(row=1, column=1)
        resultClassLabel = Label(self, text = "                   ", font=('Helvetica 16 bold'), bg= "sky blue")
        resultClassLabel.grid(row=3, column=2)
        resultClassLabel = Label(self, text = output_class, font=('Helvetica 16 bold'), bg= "sky blue")
        resultClassLabel.grid(row=3, column=2)   
        sentimentClassLabel = Label(self, text = "                  ", font=('Helvetica 16 bold'), bg= "sky blue")
        sentimentClassLabel.grid(row=3, column=1) 
        sentimentClassLabel = Label(self, text = self.getSentiment(s), font=('Helvetica 16 bold'), bg= "sky blue")
        sentimentClassLabel.grid(row=3, column=1) 		
        self.update_idletasks()		
        #load_news_from_csv()	


    def getEntity(self,s):
        #nlp = spacy.load('en_core_web_sm')
        print("1")
        nlp = joblib.load('spacy_nlp.pkl')
        print("2")
        parsed_review = nlp(s)
        print(".........................................")
        entity_list= ""
        for entity in parsed_review.ents:
            entity_list= entity_list + (str(entity) + " : " + str(entity.label_) + "\n")
            print(str(entity) + " : " + str(entity.label_)) 
        return entity_list 


    def getSentiment(self,s):    
        # create TextBlob object of passed tweet text
        analysis = TextBlob(s)
        # set sentiment
        if analysis.sentiment.polarity >= 0.3:
            return 'positive'
        elif (analysis.sentiment.polarity < 0):
            return 'negative'
        else:
            return 'neutral'			
		
    def getNews(self):
        #box.showinfo("Information", s)
        self.update_idletasks()
        
        text = load_news_from_csv()       	
        x = [text]
        output_class = news_classifier(x)
        print(output_class)
        #self.getEntity(text)
        senti= self.getSentiment(text)
        print(senti)
		
        getNewsLabel = Label(self, text= "..............................."*32, font=('Helvetica 10'), bg= "sky blue", wraplength=500)
        getNewsLabel.grid(row=1, column=1)
        getNewsLabel = Label(self, text= text[0:500]+ "***", font=('Helvetica 8'), bg= "sky blue", wraplength=500)
        getNewsLabel.grid(row=1, column=1)
		
        sentimentClassLabel = Label(self, text = "                  ", font=('Helvetica 16 bold'), bg= "sky blue")
        sentimentClassLabel.grid(row=3, column=1) 
        sentimentClassLabel = Label(self, text = senti, font=('Helvetica 16 bold'), bg= "sky blue")
        sentimentClassLabel.grid(row=3, column=1) 
		
        resultClassLabel = Label(self, text = "                   ", font=('Helvetica 16 bold'), bg= "sky blue")
        resultClassLabel.grid(row=3, column=2)
        resultClassLabel = Label(self, text = output_class, font=('Helvetica 16 bold'), bg= "sky blue")
        resultClassLabel.grid(row=3, column=2)
		
        resultClassLabel = Label(self, text = self.getEntity(text) , font=('Helvetica 10 bold'), bg= "sky blue" , anchor= W)
        resultClassLabel.grid(row=3, column=0)
		
	  
        		

def main():
    root = Tk()    
    #root.geometry("250x150+300+300")    # width x height + x + y
    # we will use centreWindow instead
    root.resizable(width=FALSE, height=FALSE)
    # .. not resizable
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
