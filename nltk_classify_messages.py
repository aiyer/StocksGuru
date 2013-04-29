import operator
import sys
import nltk.classify.naivebayes
from FeatureExtractor import WebPageParser
import glob
import os
import re
import pickle
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer

class Classify(object):

    def __init__(self, name='', pool=None):
        self.classifier = None 
        self.parser = None        
        self.stops = [x for x in stopwords.words('english')]
        
    def tokenize(self,text):
        tokens = []
        words = re.split('[^a-zA-Z0-9]',text)
        for word in words:            
            if word.isalnum():
                #stemming
                PorterStemmer().stem_word(word)
                tokens.append(word.lower())
                
        return tokens

    def message_features(self,message,title,stock):
        words = self.tokenize(message)
        features = {}        

        #stop words
        good_words = list(set(words)-set(self.stops))
        for w in good_words:
            features["tf(%s)" % w] = words.count(w)
            features["title(%s)" % w] = title
            features["contains(%s)" % w] = True
            features["stock(%s)" % w] = stock
            
        return features
    
    def read_lexicon(self):
        #TODO
        #add positive words for strong buy sentiment        
        #add negative words for strong sell sentiment
        #add neutral words
        fs = []        
        fp = open('lexicon_buy.txt','r')
        lines = fp.readlines()       
        
        for line in lines:            
            fs.append( ({"contains(%s)" % line.rstrip():True},'buy') )
        fp.close()

        fp = open('lexicon_sell.txt','r')
        lines = fp.readlines()
        for line in lines:            
            fs.append( ({"contains(%s)" % line.rstrip():True},'sell') )

        fp.close()
        
        return fs              
    
    def Train(self,should_train):
        
        if should_train == False:
            self.Deserialize()
            return
        
        self.parser = WebPageParser()
        featuresets = []
        print 'Started training'
        parsed_fields = self.parser.extract_features(should_train)        
        for message in parsed_fields.keys():
            title = parsed_fields[message].title
            stock = parsed_fields[message].stock
            sentiment = parsed_fields[message].sentiment
            featuresets.append( (self.message_features(message,title,stock), sentiment) )

        featuresets.extend(self.read_lexicon())        
        self.classifier = nltk.NaiveBayesClassifier.train(featuresets)
        print 'Finished training'
        
        print 'Started Serializing'
        self.Serialize()
        print 'Finished Serializing'
        
    def Serialize(self):        
        try:
                print 'Started Serializing Classifier'
                file_name = 'classifier.dat'
                fp = open(file_name,'wb')                        
                pickle.dump(self.classifier,fp)
                print 'Finished Serializing Classifier'
        finally:
                fp.close()

    def Deserialize(self):        
        file_name = 'classifier.dat'
        fp = open(file_name,'rb')
        try:
                print 'Started Deserializing Classifier'
                self.classifier = pickle.load(fp)
                print 'Finished Deserializing Classifier'
        finally:
                fp.close() 

    #guess the sentiment of the given stock
    def Guess(self,message,title,stock):
        #TODO        
        #take avg of all sentiments across all messages posted in the past 2 days -
        #for the given stock.               
        sentiment = self.classifier.classify(self.message_features(message,title,stock))       
        return sentiment
        
def main(args):    
    c = Classify()
    c.Train(False)
    title = 'Google to buy yahoo'
    stock = 'Goog'    
    print c.Guess('awesome',title,stock)
    print c.Guess('this stock is a decent buy.',title,stock)
    print c.Guess('fair not',title,stock)
    print c.Guess('worst bad',title,stock)
    print c.Guess('bad',title,stock)    
    print c.Guess('wonderful company',title,stock)
    print c.Guess('extraordinary value for money',title,stock)    
    print c.Guess('suck on it',title,stock)
    print c.Guess('get rid of it sux',title,stock)    
    print c.Guess('shit stock',title,stock)
    print c.Guess('Google is crashing sell it fast',title,stock)
 
if __name__ == "__main__":
    import sys   
    main(sys.argv)

        
        
    


    
