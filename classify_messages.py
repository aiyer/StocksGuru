import operator
import sys
from NBClassifier import Bayes
from FeatureExtractor import WebPageParser
#from WebCrawler import Crawler

class Classify(object):

    def __init__(self, name='', pool=None):
       self.guesser = {}
       self.parser = WebPageParser()
       
    def Train(self,should_train):        
        if should_train == False:
            self.Deserialize()
            return

        #each stock will have its own guesser        
        print 'Started training'
        features = self.parser.extract_features(should_train)        
        for message in features.keys():
            text = message + features[message].title + features[message].sentiment + features[message].stock
            self.guesser.train(features[message].sentiment,text)
        print 'Finished training'
        print 'Started Serializing'
        self.Serialize()
        print 'Finished Serializing'
        
    def Serialize(self):        
        self.guesser.save()

    def Deserialize(self):        
        self.guesser.load()

    #guess the sentiment of the given stock
    def Guess(self,message,stock):
        #TODO
        #check for empty res
        #take avg of all sentiments across all messages posted in the past 2 days -
        #for the given stock.
        res = dict(self.guesser.guess(message))
        sentiment = max(res.iteritems(), key=operator.itemgetter(1))[0]
        return sentiment

def main(args):
    c = Classify()
    c.Train(True)    
    print c.Guess('Well then don\'t buy YHOO, long live, MSFT ... :) To be frankly with you, I hate to think that YHOO got merged with a company without any culture ...Doesn\'t matter whether merged with MSFT or not. YHOO could prosper without MSFT, too.I just want to enjoy a short-cut, though. ')    

if __name__ == "__main__":
    import sys   
    main(sys.argv)

        
        
    


    
