__author__ = 'Diogo Alves'
import urlparse
import oauth2 as oauth
from credentials import CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN_SECRET

def autenticate():
    REQUEST_TOKEN_URL = 'https://cloudpt.pt/oauth/request_token'
    ACCESS_TOKEN_URL  = 'https://cloudpt.pt/oauth/access_token'
    AUTHORIZATION_URL = 'https://cloudpt.pt/oauth/authorize'
    API_URL 		  = 'https://publicapi.cloudpt.pt/1'
    API_CONTENTS_URL  = 'https://api-content.cloudpt.pt'

    CALLBACK_URL = 'oob'

    consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    client = oauth.Client(consumer)

    resp, content = client.request(REQUEST_TOKEN_URL + '?oauth_callback=' + CALLBACK_URL, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    print "Request Token:"
    print "OAUTH_TOKEN        = %s" % request_token['oauth_token']
    print "OAUTH_TOKEN_SECRET = %s" % request_token['oauth_token_secret']
    print

    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (AUTHORIZATION_URL, request_token['oauth_token'])
    print

    if "xxxx" in OAUTH_TOKEN_SECRET:
        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Have you authorized me? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')

        token = oauth.Token(request_token['oauth_token'],
            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        resp, content = client.request(ACCESS_TOKEN_URL, "POST")
        access_token = dict(urlparse.parse_qsl(content))

        print "Access Token:"
        print "OAUTH_TOKEN        = %s" % access_token['oauth_token']
        print "OAUTH_TOKEN_SECRET = %s" % access_token['oauth_token_secret']
        print
        print "Insert these values in credentials.py"
        print "You may now access protected resources using the access tokens above."
        print
    else:
        print "All set to go"