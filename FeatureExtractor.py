import math, urllib2
from BeautifulSoup import BeautifulSoup
import pickle

class Feature(object):
        def __init__(self,stock,date,title,sentiment,author):                
                self.stock = stock
                self.date = date                
                self.title = title        
                self.sentiment = sentiment
                self.author = author
                
        def __repr__(self):
            #customize to get more info while printing
            return str(self.sentiment)

            
class WebPageParser(object):

        def __init__(self):
                self.features = {}
                self.feature = None
                
        def deserialize(self):
                file_name = 'features.dat'
                fp = open(file_name,'rb')
                try:
                        print 'Started Deserializing Features'
                        self.features = pickle.load(fp)
                        print 'Finished Deserializing Features'
                finally:
                        fp.close()                        
        
        def parse_webpage(self,urls,sentiment,stock):

                print 'Parsing ' + sentiment + ' Sentiment'
                no_of_files = 0
                for url in urls[0:10]:                        
                        try:
                                no_of_files += 1
                                print '\nparsing:' + str(no_of_files)
                                print 'url:' + url
                                html_file = urllib2.urlopen(url)
                                file_contents = html_file.read()
                                html_file.close()
                                soup = BeautifulSoup(file_contents)

                                #user_name
                                userNameSoup = soup.findAll("a", {"class" : "syslink authorname_nickname_reg"})[0]
                                user_name = str(userNameSoup.findAll(text=True)[0])                                              
                                
                                #title                
                                titleSoup =  soup.findAll("span", {"class" : "user-data"})[0]                       
                                title = str(titleSoup.findAll(text=True)[0])

                                #date
                                dateSoup = soup.findAll("span", {"style" : "vertical-align:middle;"})[0]
                                date = str(dateSoup.findAll(text=True)[0])
                                
                                #message
                                message = ''
                                messageContentsSoup = soup.findAll("div", {"class" : "user-data"})[0]                        
                                msgList = messageContentsSoup.findAll(text=True)
                                for msg in msgList:
                                        message += str(msg)                        
                                
                                feature = Feature(stock,date,title,sentiment,user_name)
                                self.features[message] = feature                               
                                
                        except urllib2.URLError, e:
                                print 'URLError'
                                pass
                        except IndexError, e:
                                print 'IndexError'
                                
                        except Exception, e:
                                print 'Unknown Error'
                        

        def serialize(self):
                try:
                        print 'Started Serializing Features'
                        file_name = 'features.dat'
                        fp = open(file_name,'wb')                        
                        pickle.dump(self.features,fp)
                        print 'Finished Serializing Features'
                finally:
                        fp.close()
                
        def extract_features(self,should_parse):
                if should_parse == False:
                        self.deserialize()        
                        return self.features
                
                #stocks = ['YHOO','GOOG','MSFT','INTC','AAPL']
                stocks = ['YHOO']
                for stock in stocks:
                        
                        f = open("output-"+stock+"/Buy.txt","r")
                        urls = f.readlines()                
                        f.close()                
                        self.parse_webpage(urls,'buy',stock)

                        f = open("output-"+stock+"/Sell.txt","r")
                        urls = f.readlines()
                        f.close()                
                        self.parse_webpage(urls,'sell',stock)

                        f = open("output-"+stock+"/StrongBuy.txt","r")
                        urls = f.readlines()
                        f.close()                            
                        self.parse_webpage(urls,'strong_buy',stock)

                        f = open("output-"+stock+"/StrongSell.txt","r")
                        urls = f.readlines()
                        f.close()
                        self.parse_webpage(urls,'strong_sell',stock)

                        f = open("output-"+stock+"/Hold.txt","r")
                        urls = f.readlines()
                        f.close()                            
                        self.parse_webpage(urls,'hold',stock)
                
                self.serialize()
                
                return self.features


