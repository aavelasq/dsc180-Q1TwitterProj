# imports
import apikeys
import pandas as pd
import requests
import os
import json
import re

bearer_token = apikeys.apikeys['bearer_token']

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '"nct" (#NCT OR #NCT127) -is:retweet', 'max_results': '10', 
'tweet.fields': 'created_at,public_metrics,author_id'}


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
    json_response = connect_to_endpoint(search_url, query_params)
    df = json_into_df(json_response)
    json_poutput = json.dumps(json_response, indent=4, sort_keys=True)
    print(json_poutput)

if __name__ == "__main__":
    main()