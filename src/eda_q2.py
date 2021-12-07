import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import re
import os
import warnings
warnings.filterwarnings("ignore")

test_date = datetime.datetime(2021, 11, 12)
milo_deplatform_date = datetime.datetime(2016, 7, 19)
milo_top_words = ["#sjw", "#triggered", "#feminismiscancer",'#hitler', "#politicalcorrectnessgonemad", "#trump2016", "savior",'#regressiveleft']
test_top_words = ["bebjfhadkfkdkdkkdkd", "alkflsdkfksdjf", "ajflksjdlkfdjsfkjsdklfjs"]
outdir = ".//data/out/"

# main function
def research_q2(data, test=False): 
    
    tweet_data = data 
    tweet_data["text"] = tweet_data["text"].str.lower()
    tweet_data["created_at"] = pd.to_datetime(tweet_data["created_at"])

    # check if test or not
    if test:
        deplat_date =  test_date
        top_words = test_top_words
    else:
        deplat_date = milo_deplatform_date
        top_words = milo_top_words

    # change deplatforming date to datetime date
    deplat_date = deplat_date.date()

    # filter out only tweets that contain the top words
    s_pattern = '|'.join(top_words)
    initial_df = tweet_data.loc[tweet_data["text"].str.contains(s_pattern)]
    
    words_df = create_word_cols(initial_df,top_words)
    # splitting and removing unecessary cols
    ideas_time_df = words_df.iloc[:,np.r_[1,  4:len(words_df.columns)]]
    users_time_df = words_df.iloc[:,np.r_[0,1,  4:len(words_df.columns)]]

    # create final output
    create_table(ideas_time_df, users_time_df, deplat_date, outdir)
    plot_unique_users(users_time_df, deplat_date, outdir)
    plt.clf()
    plot_tweets_vol(ideas_time_df, deplat_date, outdir)
    plt.clf()
    plot_med_tweets(ideas_time_df, deplat_date, outdir)


def create_word_cols(df, milo_top_words):
    '''
    retrieves all relevant tweets to influential words
    '''
    for w in milo_top_words:
        df[w] = df["text"].apply(lambda x: split_check(x,w))
    return df

def split_check(x,w):
    '''
    helper function to split words and hastags in tweets
    '''
    df_words = set(re.split(" |\.|,|!|\?|&|:|;",x))
    if w in df_words:
        return 1 
    else:
        return 0

def create_table(ideas_time_df, users_time_df, deplat_date, outdir):
    '''
    creates before and after deplatforming table
    '''
    # group by and calculate change in tweet vol for specified words
    ideas_time_df["created_at"] = ideas_time_df["created_at"].dt.date
    ideas_time_gb_sum = ideas_time_df.groupby("created_at").sum()
    ideas_time_gb_sum.reset_index(inplace=True)

    # split tweets into before and after deplat date
    before_dep_tweets = ideas_time_gb_sum.loc[ideas_time_gb_sum["created_at"] <= deplat_date]
    after_dep_tweets = ideas_time_gb_sum.loc[ideas_time_gb_sum["created_at"] > deplat_date]

    before_dep_tw_sum = before_dep_tweets.sum(axis=0).rename("Tweets Vol. Pre Deplatforming").to_frame()
    after_dep_tw_sum = after_dep_tweets.sum(axis=0).rename("Tweets Vol. Post Deplatforming").to_frame() 
    tweets_vol_ct = before_dep_tw_sum.join(after_dep_tw_sum)
        
    tweets_vol_ct["Tweets Vol. % Change"] = percentage_change(tweets_vol_ct["Tweets Vol. Pre Deplatforming"],tweets_vol_ct["Tweets Vol. Post Deplatforming"]).fillna(0)

    # group by and calculate change in unique users for specified words
    users_time_df["created_at"] = users_time_df["created_at"].dt.date

    # split users and tweets into before and after deplat date
    before_dep_users = users_time_df.loc[users_time_df["created_at"] <= deplat_date]
    after_dep_users = users_time_df.loc[users_time_df["created_at"] > deplat_date]

    before_users_time_gb = before_dep_users.groupby("id").sum()
    before_users_time_gb[before_users_time_gb != 0] = 1 
    before_users_time_gb.reset_index(inplace=True)
    before_users_time_gb = before_users_time_gb.sort_values("id", ascending=False)
    before_users_time_gb = before_users_time_gb.sum(axis=0).rename("Unique Users Pre Deplatforming").to_frame().iloc[1:,]

    after_users_time_gb = after_dep_users.groupby("id").sum()
    after_users_time_gb[after_users_time_gb != 0] = 1 
    after_users_time_gb.reset_index(inplace=True)
    after_users_time_gb = after_users_time_gb.sort_values("id", ascending=False)
    after_users_time_gb = after_users_time_gb.sum(axis=0).rename("Unique Users Post Deplatforming").to_frame().iloc[1:,]

    unique_users_ct = before_users_time_gb.join(after_users_time_gb)
    unique_users_ct["Unique Users % Change"] = percentage_change(unique_users_ct["Unique Users Pre Deplatforming"],unique_users_ct["Unique Users Post Deplatforming"]).fillna(0)

    # joining tweets vol and unique users results, write table to data folder
    final_table = tweets_vol_ct.join(unique_users_ct)
    final_table.to_csv(os.path.join(outdir, "Milo_RQ2_Table.csv")) 


def percentage_change(col1,col2):
    '''
    helper function to calculate percent change
    '''
    return round(((col2 - col1) / col1) * 100,0)

def plot_unique_users(users_time_df, deplat_date, outdir):
    '''
    plot graph for change in unique users
    '''
    # create column for days before and after deplateforming
    users_time_df["Days Before & After Deplatforming"] = (users_time_df["created_at"] - deplat_date).dt.days
    # group by and select unique users for tweets cont. top words
    user_days_gb = users_time_df.groupby(["Days Before & After Deplatforming","id"]).sum()
    user_days_gb[user_days_gb != 0] = 1 
    user_days_gb = user_days_gb.droplevel("id").reset_index()
    user_days_gb = user_days_gb.groupby("Days Before & After Deplatforming").sum()

    plt.figure(figsize = (16,9))
    p = sns.lineplot(data=user_days_gb, dashes=False).set(title="Number of Users using Keyword", ylabel = "# of Users")
    plt.axvline(0, 0.04, 0.99,color="red")
    plt.savefig(os.path.join(outdir, "unique_users.jpg"),dpi=300, bbox_inches = "tight")
    plt.close()


def plot_tweets_vol(ideas_time_df, deplat_date, outdir):
    '''
    plot graph for change in tweet volume
    '''
    # create column for days before and after deplateforming
    ideas_time_df["Days Before & After Deplatforming"] = (ideas_time_df["created_at"] - deplat_date).dt.days
    # group by and select tweets that cont. top words
    tweets_days_gb_sum = ideas_time_df.groupby("Days Before & After Deplatforming").sum()
    
    plt.figure(figsize = (16,9))
    p = sns.lineplot(data=tweets_days_gb_sum, dashes=False).set(title="Volume of Tweets having Keyword", ylabel = "# of Tweets")
    plt.axvline(0, 0.04, 0.99,color="red")
    plt.savefig(os.path.join(outdir, "tweets_volume.jpg"),dpi=300, bbox_inches = "tight")
    plt.close()

def plot_med_tweets(ideas_time_df, deplat_date, outdir):
    '''
    plot graph for median tweets
    '''
    # create column for days before and after deplateforming
    ideas_time_df["Days Before & After Deplatforming"] = (ideas_time_df["created_at"] - deplat_date).dt.days
    # group by and select median number of tweets that cont. top words
    tweets_days_gb_med = ideas_time_df.groupby("Days Before & After Deplatforming").median()

    plt.figure(figsize = (16,9))
    p = sns.lineplot(data=tweets_days_gb_med, dashes=False).set(title="Median Number of Tweets", ylabel = "# of Tweets")
    plt.axvline(0, 0.04, 0.99,color="red")
    plt.savefig(os.path.join(outdir, "median_number_tweets.jpg"),dpi=300, bbox_inches = "tight")
    plt.close()