
Sublime Google Tasks
====================

## Description:

Sublime Text 2 Plugin to view and manage your Google Tasks.

![Sublime Google Tasks](http://jpwelch.me/wp/wp-content/uploads/2012/09/sublime-google-tasks.png)

## Prerequisites:

* Mac OS X
* [Sublime Text 2](http://sublimetext.com)
* [Google API Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)
* Registered Client ID within [Google API Console Access](https://code.google.com/apis/console#:access)

## Installation:

Follow Google's instructions on how to install [Google API's Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)

Register a client id and client secret on [Google API Console](https://code.google.com/apis/console#:access). 

* Select "Installed Application" as your application type 
* Set your redirect URL to "http://localhost"

### Install "Sublime Google Tasks" Package

<!-- 
**Sublime Package Control**

Sublime Google Tasks is discoverable and installable in [Sublime Package Control](http://wbond.net/sublime_packages/package_control).  
 -->

**Clone from GitHub**

```
cd ~/"Library/Application Support/Sublime Text 2/Packages/"
git clone git://github.com/jpswelch/sublime-google-tasks
```

## Configuration:

Under Preferences > Package Settings > Google Tasks > Settings Users you must enter your client\_id, client\_secret and user\_agent from you Google API setup.

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


## Support

This plugin is fairly new.  You might have [suggestions or issues](https://github.com/jpswelch/sublime-google-tasks/issues). 

[Donate](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=H8Y45D7BCR6JL&lc=US&item_name=Sublime%20Google%20Tasks%20Plugin&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)


## License

Copyright (c) 2012 Jean-Pierre Welch

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
