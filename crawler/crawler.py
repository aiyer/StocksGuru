'''def readfromfile(filename, files_indexed):
    tm = []
    for i in range(0, files_indexed):
        l = []
        tm.append(l)
        for j in range(0, files_indexed):
            tm[i].append(0)

    f = open(filename, "r")
    line = f.readline(files_indexed)
    i=0
    while(line):
        for j in range(0, files_indexed):
            tm[i][j] = int(line[j])
        line = f.readline(files_indexed)
        i += 1
    
    f.close()
    return tm'''
    
class Crawler(object):
    def __init__(self):
        self._files_indexed = 0
        self._messages = {}
        
    def traverse_web_dir(self, url):
        from urllib import *
        from BeautifulSoup import *
        import os
        count = 0
        link = ''
        doc = urlopen(url).read()
        soup = BeautifulSoup(doc)

        for a in soup('a'):
            
            if a.has_key('href'):
                link = str(a['href'])
            else:
                link = ''
            #print link
            if link.startswith('http'):
                if link.find('mid') != -1:
                    mid = int(link[link.find('mid')+4:])
                    if self._messages.has_key(mid) == False:
                        self._messages[mid] = link
                        self._files_indexed += 1
                        count += 1

        '''if link == '#':
            return 0

        if count == 0:
            return -1'''
        
        return count
        

    
    def index_url(self, url):
        self._files_indexed = 0
        count = int(url.split(' ')[1])
        url = url.split(' ')[0]
        print ''
        file_name = ''
        messages_crawled = 0
        while messages_crawled < count:
            c = self.traverse_web_dir(url)
            #print c
            if c == 0:
                continue
            messages_crawled += c
            new_url = int(url[url.find('off=')+4:])+20
            file_name = self.get_file_name(url)
            sentiment = file_name.split('/')[1]
            sentiment = sentiment[:sentiment.find('_')]
            print '%s : ' %sentiment + 'messages_crawled [%d]' %(messages_crawled)
            url = url[:url.find('off=')+4] + str(new_url)
            #print url
        
        self.writetofile(file_name)
        
        return

    def writetofile(self, filename):
        from time import localtime
        t = localtime()
        s = '-%s' %str(t[1]).rjust(2, '0')
        s += '%s' %str(t[2]).rjust(2, '0')
        s += '%s' %str(t[3]).rjust(2, '0')
        s += '%s' %str(t[4]).rjust(2, '0')
        s += '%s.txt' %str(t[5]).rjust(2, '0')
        filename += s
        f = open(filename,"w")
        for m in self._messages:
            f.write(self._messages[m]+'\n')
            
        f.close()
        return

    def get_file_name(self, url):
        file_name = ''

        if int(url.split('sentiment=')[1][0]) == 1:
            file_name='output-GOOG/Strong Sell_'+str(self._files_indexed)
        else:
            if int(url.split('sentiment=')[1][0]) == 2:
                file_name='output-GOOG/Sell_'+str(self._files_indexed)
            else:
                if int(url.split('sentiment=')[1][0]) == 3:
                    file_name='output-GOOG/Hold_'+str(self._files_indexed)
                else:
                    if int(url.split('sentiment=')[1][0]) == 4:
                        file_name='output-GOOG/Buy_'+str(self._files_indexed)
                    else:
                        if int(url.split('sentiment=')[1][0]) == 5:
                            file_name='output-GOOG/Strong Buy_'+str(self._files_indexed)

        return file_name
    
    def tokenize(self, text):
        import re
        tokens = []
        temp_str = text.lower()
        temp_str = re.sub(r'[^a-zA-Z0-9]',' ', temp_str)
        tokens = temp_str.split()
        return tokens

def main(args):
    #yahoo message board url for goog stock
    f = open("input-GOOG/input_url.txt", "r")
    url = f.readline()
    while(len(url)!=0):
        c = Crawler()
        if url.endswith('\n'):
            url = url[:-1]
        num_files = c.index_url(url)
        url = f.readline()
        
    f.close()
    
if __name__ == "__main__":
    import sys
    main(sys.argv)

