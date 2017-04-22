import requests
from threading import Thread
import sys
import getopt
import re
from termcolor import colored

def banner():
    print "\n*******************************************"
    print "* Brutee V0.3 *"
    print "*******************************************"

def usage():
    print "Usage:"
    print "     -w: url (http://somesite.com/Brutee)"
    print "     -t: threads"
    print "     -f: dictionary file\n"
    print "     -c: filter by status code"
    print " example Brutee.py -w http://www.targetsite.com/Brutee -t 5 -f common.txt -c 404"


class request_performer(Thread):
    def __init__(self, word, url,hidecode):
        Thread.__init__(self)
        try:
            self.word = word.split("\n")[0]
            self.urly = url.replace('Brutee',self.word)
            self.url = self.urly
            self.hidecode = hidecode
        except Exception, e:
            print e

    def run(self):
        try:
            r = requests.get(self.url)
            lines = str(r.content.count("\n"))
            chars = str(len(r._content))
            words = str(len(re.findall("\S+", r.content)))
            code = str(r.status_code)
            if self.hidecode != code:
                if '200' <= code < '300':
                    print colored(code,'green') + " \t\t" + code + " \t\t" + lines +  " \t\t" + words + " \t\t" + self.url + " \t\t" + chars + " \t\t"
                elif '400' <= code < '500':
                    print colored(code,'red') + "   \t\t" + code + " \t\t" + lines +  " \t\t" + words + " \t\t" + self.url + " \t\t" + chars + " \t\t"
                elif '300' <= code < '400':
                    print colored(code,'blue') + "  \t\t" + code + " \t\t" + lines +  " \t\t" + words + " \t\t" + self.url + " \t\t" + chars + " \t\t"
                else:
                    print colored(code,'yellow') + " \t\t" + code + " \t\t" + lines +  " \t\t" + words + " \t\t" + self.url + " \t\t" + chars + " \t\t"
            else:
                pass
            i[0] = i[0] - 1
        except Exception, e:
                print e

def start(argv):
    banner()
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try :
        opts, args = getopt.getopt(argv, "w:f:t:c:")
    except getopt.GetoptError:
        print "Error en arguments"
        sys.exit()
    hidecode = 000
    for opt, arg in opts:
            if opt == '-w':
                url = arg
            elif opt == '-f':
                dict = arg
            elif opt == '-t':
                    threads=arg
            elif opt == '-c':
                hidecode = arg
    try:
        f = open(dict, "r")
        words = f.readlines()
    except:
            print"Failed opening file: " + dict + "\n"
            sys.exit()
    launcher_thread(words, threads, url,hidecode)

def launcher_thread(names, th, url,hidecode):
    global i
    i=[]
    i.append(0)
    print "------------------------------------------------------------------------------------------------------------------------"
    print "Code" + "\t\t\t\t\t\t Lines \t\t\tURL\t\t\t\t\tWords"
    print "------------------------------------------------------------------------------------------------------------------------"
    while len(names):
        try:
            if i[0] < th:
                n = names.pop(0)
                i[0] = i[0] + 1
                thread = request_performer(n, url,hidecode)
                thread.start()

        except KeyboardInterrupt:
            print "Brutee interrupted by user. Finishing attack..."
            sys.exit()
        thread.join()
    return

if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
            print "Brutee interrupted by user, killing all threads!!!"
