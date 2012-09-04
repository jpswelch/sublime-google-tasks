
Sublime Google Tasks
====================

## Description:

Sublime Text 2 Plugin to view and manage your Google Tasks.


## Prerequisites:

* [Sublime Text 2](http://sublimetext.com)
* [Google API Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)
* Registered Client ID within [Google API Console Access](https://code.google.com/apis/console#:access)

## Installation:

Install [Google API's Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)

Register a client id and client secret on [Google API Console](https://code.google.com/apis/console#:access). 

* Select "Installed Application" as your application type 
* Set your redirect URL to "http://localhost"

Install Sublime Google Tasks Package

Under User Preferences for Google Tasks enter your client\_id, client\_secret and user\_agent


```
{
	"client_id": "PUT YOUR REGISTERED CLIENT ID HERE",
	"client_secret":"PUT YOUR REGISTERED CLIENT SECRET HERE",
	"user_agent":"PUT YOUR APPLICATION NAME HERE"
}
```

## Usage:

```
Cmd + Shift + T
```



