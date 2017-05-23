#Python 3 Authentication and Authorization SDK/library

This python module enables authentication, authorization, etc. against Westmont's systems.

Requirements:

* json
* requests
* getpass
* socket

socket and json are probably already installed, but the remaining can be installed with pip.

```{.python}

"""
" Perform logout of the token given by delToken
"
" @param delToken(Dict): A dict generated from the json of the token you want to log out
" @param token(String): The token to use for authentication (can be gotten with wmappauth.getTokenString() )
" @param sigb64(String): Base64-encoded signature to use for authentication (can be gotten with wmappauth.getSignature() )
"""
def invalidateToken(delToken, token, sigb64)
"""
" Get a list of tokens from the server (returns the raw result of requests.get)
"""
def listTokens(token, sigb64)
"""
" Renew the token, persisting the result to the disk if successful
"
" @return: True or False, indicating whether the operation succeeded
"""
def renewToken(token, sigb64)
"""
" Pass a dict invalidationSubScription
"""
def subscribeToInvalidation(invalidationSubscription, token, sigb64)
"""
" Check if the given token and signature are valid (performs a network call)
"""
def isValidToken(token, sigb64)
"""
" Retrieve the token if credentials are present
"""
def getTokenString()
"""
" Retrieve the token signature if credentials are present
"""
def getSignature()
"""
" Save the token/signature to the disk (shouldn't ever need to call this)
"""
def persistTokens()
"""
" Login with the supplied credentials, saving them to the disk if successful
"
" @return True or False, indicating whether the operation succeeded
"""
def wmLogin(username, password, deviceName=socket.gethostname())
"""
/**
 * Prompt the user to login (handles obtaining the username and password on a CLI for you), saving the result to disk if successful
 * 
 * @return: True or False, indicating whether the operation succeeded
 */
"""
def promptLogin()

"""
/**
 * Load credentials from disk, prompting for a login in the terminal be default if the operation fails
 * 
 * @return: True or False, indicating whether they were loaded
 */
"""
def loadCredentials(prompt=True)
```

