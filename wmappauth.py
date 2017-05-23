#!/usr/bin/python3

# Source: http://gitlab.wmapp.mccollum.enterprises/wmapp/python2-client

import json
import requests
import getpass
import socket

protocol = "https"
server = "wmapp.mccollum.enterprises/loginserver"

authBaseUrl = protocol+"://"+server+"/api"
tokenBaseUrl = authBaseUrl+"/token"
usersBaseUrl = authBaseUrl+"/users"

loginUrl = tokenBaseUrl+"/getToken"
logoutUrl = tokenBaseUrl+"/invalidateToken"
listUrl = tokenBaseUrl+"/listTokens"
renewUrl = tokenBaseUrl+"/renewToken"
invalidationSubscriptionUrl = tokenBaseUrl+"/subscribeToInvalidation"
tokenValidUrl = tokenBaseUrl+"/tokenValid"

tokenSignature=""
tokenString=""

TOKEN_HEADER='Token'
TOKEN_SIGNATURE_HEADER='TokenSignature'

def readTokens():
	try:
		with open('token.json', 'r') as tf:
			global tokenString
			tokenString = tf.read()
		with open('sigb64.txt', 'r') as sf:
			global tokenSignature
			tokenSignature = sf.read()
		return True
	except IOError as e:
		return False

def getToken(username, password, deviceName):
	hrs = {'Content-Type': 'application/json'}
	loginObject = {'username': username, 'password': password, 'devicename': deviceName}
	return requests.post(url=loginUrl, data=json.dumps(loginObject), headers=hrs)

def invalidateToken(delToken, token, sigb64):
	hrs = {'Content-Type': 'application/json'}
	hrs['Token'] = token
	hrs['TokenSignature'] = sigb64
	return requests.delete(url=logoutUrl+'/'+str(delToken['tokenId']), headers=hrs)

def listTokens(token, sigb64):
	hrs = {'Content-Type': 'application/json'}
	hrs['Token'] = token
	hrs['TokenSignature'] = sigb64
	return requests.get(url=listUrl, headers=hrs)

def renewToken(token, sigb64):
	global TOKEN_HEADER
	global TOKEN_SIGNATURE_HEADER
	hrs = {'Content-Type': 'application/json'}
	hrs[TOKEN_HEADER] = token
	hrs[TOKEN_SIGNATURE_HEADER] = sigb64
	newCreds = requests.get(url=renewUrl, headers=hrs)
	if not checkCode(newCreds, 200, "renew"):
		return False
	global tokenString
	tokenString = str(newCreds.content, 'utf-8')
	global tokenSignature
	tokenSignature = newCreds.headers[TOKEN_SIGNATURE_HEADER]
	persistTokens()
	return True

def subscribeToInvalidation(invalidationSubscription, token, sigb64):
	hrs = {'Content-Type': 'application/json'}
	hrs['Token'] = token
	hrs['TokenSignature'] = sigb64
	return requests.post(url=invalidationSubscriptionUrl, headers=hrs)

"""
" Check whether the token is valid against the token validation API endpoint
"""
def isValidToken(token, sigb64):
	hrs = {'Content-Type': 'application/json'}
	hrs['Token'] = token
	hrs['TokenSignature'] = sigb64
	return requests.get(url=tokenValidUrl, headers=hrs)

"""
" Check your response against an API endpoint (primarily for testing, but may be good for production)
" @param httpResponse: response object from python-requests library to check
" @param expectedResponse: numeric response code expected
" @failureMessage String description of what action failed
"
" @return boolean: whether the code was verified or not
"""
def checkCode(httpResponse, expectedResponse, failureMessage):
	if httpResponse.status_code != expectedResponse:
		print("\tFailed to "+failureMessage)
		print("\t"+str(httpResponse.status_code))
		print("\t"+str(httpResponse.content, 'utf-8'))
		return False
	return True

def getTokenString():
	global tokenString
	return tokenString

def getSignature():
	global tokenSignature
	return tokenSignature

def persistTokens():
	with open('token.json', 'w') as tf:
		tf.write(getTokenString())
	with open('sigb64.txt', 'w') as sf:
		sf.write(getSignature())

def wmLogin(username, password, deviceName=socket.gethostname()):
	validCreds = getToken(username, password, deviceName)
	if not checkCode(validCreds, 200, "login"):
		return False
	global tokenString
	tokenString = str(validCreds.content, 'utf-8')
	global tokenSignature
	tokenSignature = validCreds.headers['TokenSignature']
	persistTokens()
	return True

def promptLogin():
	username = input("Username: ")
	passwd = getpass.getpass()
	return wmLogin(username, passwd)

def loadCredentials(prompt=True):
	if readTokens():
		return True
	if prompt:
		return promptLogin()
	return False


"""
/*
 * If this is being executed as a program, run sample code
 */
"""
if __name__ == "__main__":
	if not loadCredentials(prompt=False):
		print("Credentials not found")
		wmLogin('erichtofen', 'oneStupidLongTestPassword23571113', 'validDevice')

"""
Sample code:

  Login:
	print "Performing login..."
	wmLogin('erichtofen', 'oneStupidLongTestPassword23571113', 'validDevice')
"""
