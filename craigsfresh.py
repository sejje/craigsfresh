#!/usr/bin/env python

from datetime import datetime
import requests
import subprocess
import time
import BeautifulSoup
import sys

url = "http://fortmyers.craigslist.org/zip/" 
filename = "craigspage.html" #save the (temporary) CL page as this
big_delay_time = 610 #seconds to wait after last page update before any refresh
small_delay_time = 45 #seconds to wait once it gets close to time

def soundoff(time):
	#print "Craigslist has been updated!"
	s = subprocess.Popen(['play', 'beep.wav'], \
	      stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]


########## DATA FUNCTIONS -- FETCH PARSE AND SAVE HTML #####################
def save_page(request):
	output = open(filename, "w")
	output.write(request.text)
	output.close()


def get_page(url):
	#print "HIT SERVER!"
	#download a copy of the page to local file
	return requests.get(url)

def extract_top_listing(html):
	#pull the topmost listing for comparison to find changes
	soup = BeautifulSoup.BeautifulSoup(html)
	link = soup.p.a['href']
	return link

def extract_top_title(html):
	#extract the topmost link title
	soup = BeautifulSoup.BeautifulSoup(html)
	return soup.p.a.text

############ TIME FUNCTIONS -- EXTRACT AND PROCESS DATE FROM PAGE ###########
def get_page_time(html):
	time_string = extract_time_string(html)
	page_time = time_string_to_date(time_string)
	return page_time
	
def extract_time_string(html):
	#extract the timestamp from downloaded CL page (in memory)
	soup = BeautifulSoup.BeautifulSoup(html)
	tag = soup.span
	tag['id'] = 'timestamp'
	return tag.text[:20]
	#return "Thu, 20 Sep 18:57:02"

def time_string_to_date(time_string):
	#craigslist doesn't put a year, so we have to replace the default of 1900
	saved = datetime.strptime(time_string, "%a, %d %b %H:%M:%S")
	return saved.replace(year=2012)

def compare_times(craigstime):
	if not craigstime:
		#did not find a time, maybe no file downloaded
		print "Warning: no original time found."
		return True
	time_elapsed = (craigstime - datetime.time(datetime.now())).total_seconds()
	if time_elapsed > big_delay_time:
		return True
	return False

def time_elapsed(old_time):
	#return seconds elapsed between now and the time given
	return (datetime.now() - old_time).total_seconds()


if __name__ == "__main__":
	if sys.argv[1]:
		url = sys.argv[1]
	if sys.argv[2]:
		big_delay_time = int(sys.argv[2])
	if sys.argv[3]:
		small_delay_time = int(sys.argv[3])
	last_update = time_string_to_date("Thu, 20 Sep 18:57:02") #initialize timer
	last_link = ""
	while True:
		passed = time_elapsed(last_update)
		if passed > big_delay_time:
			print "Large wait of %s seconds has passed" % big_delay_time
			while True:
				page = get_page(url)
				page_time = get_page_time(page.text)
				if not page_time == last_update:
					last_update = page_time
					latest_link = extract_top_listing(page.text)
					latest_title = extract_top_title(page.text)
					if not latest_link == last_link:
						print "CL updated with new listings at %s" % last_update
						last_link = latest_link
						soundoff(last_update)
					else:
						print "CL listings updated at %s, but nothing was new." % last_update
					print "Last listing titled \"%s\"" % (latest_title)
					print "Waiting until %s seconds from last CL update" % big_delay_time
					break
				else:
					print "Waiting %s seconds to refresh, last update was %s" % (small_delay_time, extract_time_string(page.text))
					time.sleep(small_delay_time)
		else:
			
			#print "Time passed is %s seconds, last update %s" % (passed, extract_time_string(page.text)[12:])
			time.sleep(1)
