import requests
import json
import datetime
import os
from settings import credentials
'''
https://www.space-track.org/documentation#howto-api_python
https://www.space-track.org/documentation#/api
response from the gp end point when using the json method is a list filled with dictionaries.
let's see if we can dump it into a text file and retrieve it so we only call the end point if we're missing recent data
'''


# orbital period of 90 minutes corresponds to an orbit height just over 282 km
# unboosted orbital lifetime measured in months
query_suffix = 'basicspacedata/query/class/gp/PERIOD/%3E90/OBJECT_TYPE/PAYLOAD/DECAY_DATE/null-val/orderby/PERIOD%20asc/limit/200/emptyresult/show'
base_url = 'https://www.space-track.org/'
login_suffix = 'ajaxauth/login'

def todays_prefix():
    today = datetime.date.today()
    return today.strftime('%Y_%m_%d')

def check_for_today():
    date_name = todays_prefix()+'.json'
    local_files = os.listdir('./api_archive')
    print(local_files)
    exists = (date_name in local_files)
    print(exists)
    if not exists:
        download_todays_ephemeris()
    return


def download_todays_ephemeris():
    date_name = todays_prefix()+'.json'
    target = open('./api_archive/'+date_name, 'w')
    with requests.Session() as session:
        log_in_attempt = session.post(base_url+login_suffix, credentials)
        print(log_in_attempt)
        result = session.get(base_url+query_suffix)
        print(result.status_code)
        if result.status_code == 200:
            # print(result.json())
            target.write(json.dumps(
                result.json(), indent=2
                ))


def main():
    check_for_today()
    date_name = todays_prefix()+'.json'
    file = open('./api_archive/'+date_name, 'r')
    todays_data = json.load( file)
    # print(todays_data)
    starlinks = 0
    for entry in todays_data:
        # print(entry['OBJECT_NAME'])
        if 'STARLINK' in entry['OBJECT_NAME']:
            starlinks+=1
        # print(entry['PERIOD'])
    print(starlinks)

if __name__ == '__main__':
    main()