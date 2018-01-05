'''
Fredrick Ryans
Last Date Modified: 12/28/2017

Americommerce URL Redirect Site Checker
This program checks if a url is an Americommerce site. If the
site is not Ammericommerce, then write it to a new file.
'''
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import csv
import sys
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.max_redirects = 20
output_file = "Not_On_Americommerce.csv"

def clean_url(url):

    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    return domain

def create_output_file():

    try:
        with open(output_file,"r") as file:
            print ("File exists")
            
    except IOError:
        with open(output_file,"w") as file:
            print ("File created")
            

def append_sitemonitor_page_to_url(url):
    
    if not url.endswith('/'):
        return url+'/store/sitemonitor.aspx'
    else:
        return url+'store/sitemonitor.aspx'
    
def check_if_url_is_Americommerce_site(url=""): 

    #Requests can also ignore verifying the SSL certficate if you set  verify to False.
    html_doc = requests.get(url,verify=False, timeout=20) #checks url
    text = html_doc.text #returns html/text of page

    if 'Success=True' in text and 400 >= html_doc.status_code < 500: 
        print ("Americommerce site: " + url)
        return "Americommerce"
    
    else: #returns redirects
        print("Not Americommerce site: " + url)
        return "Not Americommerce"
   
    return '-1'


def check_for_redirects(url):  

    try:
        return check_if_url_is_Americommerce_site(url)
    
    except requests.exceptions.Timeout:
        print (url + ' [timeout]')
    except requests.exceptions.ConnectionError:
        print (url + ' [connection error]')
    except requests.exceptions.TooManyRedirects:
        print (url + ' [too many redirects]')
    except:
        print (url + ' unexpected error')


def process_file():
    try:
        #my_csv = 'Marketing-Project.csv'
        #row_input = 'SourceURL'

        my_csv = input("Enter a csv file: ")
        row_input = input("Enter a row with URLs to check in CSV: ")
        
        if not my_csv.lower().endswith(".csv"):
            print ("Enter another file:\n")
            open_file()
            
        with open(my_csv, 'r') as input_csvfile, open(output_file, 'w',  newline='') as output_csvfile:
            reader = csv.DictReader(input_csvfile)

            writer = csv.writer(output_csvfile)
            writer.writerow([row_input])
            
            raw_urls = [row[row_input] for row in reader]
            cleaned_urls = [clean_url(url) for url in raw_urls]
            
            #returned the rows of data
            for url in cleaned_urls:
                #write to new file
                check = check_for_redirects(append_sitemonitor_page_to_url(url))
                if  check == "Not Americommerce":
                    writer.writerow([url])
                
              
    except Exception:
        print ("Unexpected error:", sys.exc_info()[0])
        sys.exit(0)
        
         
def main():
    create_output_file()
    process_file()
    print ("Done!")

if __name__ == "__main__":
    main()
