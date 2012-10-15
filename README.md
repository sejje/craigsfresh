Craigsfresh.py
=============

A simple way to monitor craigslist sections
-------------------------------------------

Craigsfresh is a basic script, and very unpolished. It takes three arguments on the command line: 
* a (craigslist) url -- this should be a section with ads
* long delay period (in seconds)
* short delay (in seconds)

The long delay is used to avoid hitting the CL server too often. A good value to use it 600, but CL updates different sections at different rates (usually 600 or 900 seconds).

The short delay is used in the event that you hit the server before it updates--if you cut it close, it's not likely you want to wait the entire long delay again before refreshing.

I usually use this to monitor the free section (quick response is mandatory), and run it as follows:
python craigsfresh.py http://yourcity.craigslist.org/zip/ 600 20
