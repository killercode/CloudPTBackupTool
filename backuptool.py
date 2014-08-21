__author__ = 'Diogo Alves'

import sys, getopt
import get_auth
import oauth2
import time
from credentials import CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN_SECRET, OAUTH_TOKEN
from requests_oauthlib import OAuth1Session
from os import listdir
from os.path import isfile, join
import os



def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hcf:",["credentials=","folder="])
   except getopt.GetoptError:
      print 'test.py -c <credentials> -f <backup folder>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -c <credentials> -f <backup folder>'
         sys.exit()
      elif opt in ("-c", "--credentials"):
         get_auth.autenticate()
      elif opt in ("-f", "--folder"):
         process(arg)

def process(folder):
    onlyfiles = [ f for f in listdir(folder) if isfile(join(folder,f)) ]

    for file in onlyfiles:
        f = open(os.path.join(folder, file), "rb")
        chunk = f.read()
        f.close()

        request = OAuth1Session(CONSUMER_KEY,
                                client_secret=CONSUMER_SECRET,
                                resource_owner_key=OAUTH_TOKEN,
                                resource_owner_secret=OAUTH_TOKEN_SECRET)


        consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        access_token = oauth2.Token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        client = oauth2.Client(consumer, access_token)
        my_scope = 'sandbox'
        my_operation = '/Files'
        my_method = 'POST'
        my_path = '/' + file

        uri = "https://api-content.meocloud.pt/1" + my_operation + '/' + my_scope + my_path
        #response, content = client.request(uri, my_method, chunk)
        response = None
        try:
            request.params["overwrite"] = false;
            response = request.post(uri,chunk)
            print "HTTP Reply: %s" % response.status_code
            if response.status_code == 200:
                print "work done!"
                os.remove(folder + "/" + file)
            else:
                print "FAILED"
        except:
            print "Something went wrong! Probably a file with that name already exists"
        request.close()

if __name__ == "__main__":
   main(sys.argv[1:])
