# imports
import twitterkeys
import pandas as pd
import requests
import os
import json
import re
import datetime
from datetime import timedelta

bearer_token = twitterkeys.apikeys['bearer_token']

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '#freemilo', 'max_results': '10', 
                'start_time': '2016-01-19T00:00:00Z', 'end_time': '2017-01-19T00:00:00Z', 
                'tweet.fields': 'created_at,author_id'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def clean_string(text):
    t = text.lower() # lowercase string
    empty_str=""
    new_t=re.sub(r"[^\w\s]",empty_str,t)
    t = ''.join(new_t) # convert back to string

    return t 

def json_into_df(json_obj):
    df = pd.DataFrame(json_obj['data'])
    df['text'] = df['text'].apply(clean_string)
    
    return df['text']

def main():
    df = pd.DataFrame()

    date = datetime.datetime(2016, 6, 19)
    final_date = date + datetime.timedelta(days=61)

    while date != final_date:
        start_time = datetime.datetime.strftime(date, r"%Y-%m-%dT%H:%M:%SZ")
        end_date = date + datetime.timedelta(days=1)
        end_time = datetime.datetime.strftime(end_date, r"%Y-%m-%dT%H:%M:%SZ")

        query_params = {'query': '"milo yiannopoulos" (#freemilo OR #miloyiannopoulos OR #freenero OR #milo OR #jesuismilo OR #yiannopoulos OR #milosd OR #nero OR #talktomilo OR #freemilonow) -is:retweet', 
                        'max_results': '10', 
                        'start_time': start_time, 
                        'end_time': end_time, 
                        'tweet.fields': 'created_at,author_id'}

        json_response = connect_to_endpoint(search_url, query_params)
        df.append(json_into_df(json_response))
        json_poutput = json.dumps(json_response, indent=4, sort_keys=True)
        print(json_poutput)

        date += timedelta(days=1)


    print(len(df))
    
    with open('/Users/nikithagopal/Documents/dsc30-pa1/dsc180-Q1TwitterProj/data/raw/rawData_milo.json', 'w') as f:
        json.dump(df, f)

if __name__ == "__main__":
    main()