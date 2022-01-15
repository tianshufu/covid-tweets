from cassandra.cluster import Cluster,ExecutionProfile,EXEC_PROFILE_DEFAULT,ConsistencyLevel
from ssl import SSLContext, PROTOCOL_TLSv1_2 , CERT_REQUIRED
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.auth import PlainTextAuthProvider
from sqlalchemy import create_engine
import pandas as pd


def highlight_target_ch(text,target):
    """
    Function to highlight the target words, which adds `` to the text
    exp：text: How are you  target: How , then return `How` are you
    :param text:
    :param target:
    :return:
    """
    # get the size of the target
    n_text,n_target = len(text),len(target)
    if n_text < n_target:
        return text
    # split the text
    text_list = text.split(" ")
    ans_list  = []
    for word in text_list:
        if target.lower() in word.lower():
            ans_list.append("<span class='highlight blue'>"+word+"</span>")
        else:
            ans_list.append(word)
    return  " ".join(ans_list)





def get_session():
    user_name = st.secrets["cassandra"]["db_username"]
    user_password =  st.secrets["cassandra"]["db_password"]
    ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    ssl_context.load_verify_locations('sf-class2-root.crt')
    ssl_context.verify_mode = CERT_REQUIRED
    profile = ExecutionProfile(consistency_level= ConsistencyLevel.LOCAL_QUORUM)
    auth_provider = PlainTextAuthProvider(username=user_name, password=user_password)
    cluster = Cluster(['cassandra.us-east-1.amazonaws.com'], ssl_context=ssl_context, auth_provider=auth_provider,
                      port=9142, execution_profiles={EXEC_PROFILE_DEFAULT: profile})
    session = cluster.connect()
    return session

def search_covid_tweets_stat_table():
    """
    General function to get the info from covid stat table, return data frame format
    :return:
    """
    cur_session = get_session()
    sql = """
        select cast(date as text) as date,avg_likes,avg_quotes,avg_replys,avg_retweets,total_num from covid.tweets_stat
    """
    r = cur_session.execute(sql)
    #print(r.current_rows)
    res_pd = pd.DataFrame(r.current_rows)
    res_pd['date'] = pd.to_datetime(res_pd['date'], format='%Y-%m-%d')
    return res_pd

def search_covid_tweets_key_words_table():
    """
    General function to get the info from covid key word table, return data frame format
    :return:
    """
    cur_session = get_session()
    sql = """
           SELECT cast(date as text) as date, delta_cnt,omicron_cnt FROM covid.tweets_key_cnt_table;
       """
    r = cur_session.execute(sql)
    res_pd = pd.DataFrame(r.current_rows)
    res_pd['date'] = pd.to_datetime(res_pd['date'], format='%Y-%m-%d')
    return res_pd

def search_covid_tweets_emotion_table():
    cur_session = get_session()
    sql = """
              select cast(date as text) as date,avg_compound_score,avg_neg_score
              ,avg_neu_score,avg_pos_score,neg_rate,neu_rate,pos_rate from covid.tweets_emotion
           """
    r = cur_session.execute(sql)
    res_pd = pd.DataFrame(r.current_rows)
    res_pd['date'] = pd.to_datetime(res_pd['date'], format='%Y-%m-%d')
    return res_pd



def test_highlight_target_ch():
    text = "Dr Alex Summers says Thursdays clinic mobile vaccine bus announced morning suddenly cancelled Just heard province says I dont explanation They wont able join us LdnOnt"
    target = "sum"
    print(highlight_target_ch(text,target))

def test_search_covid_table():
    res = search_covid_tweets_stat_table()
    print(res)
    #print(res)pd.to_datetime(res['date'], format='%Y-%m-%d')

def test_search_covid_text_table():
    res = search_covid_tweets_key_words_table()
    tmp_res = res.sort_values(by='date')
    print(tmp_res['delta_cnt'].sum())
    tmp_res_melt = tmp_res.melt(id_vars='date')
    #print(tmp_res.melt(id_vars='date'))
    print(tmp_res_melt.groupby('variable').sum())
    #print(tmp_res.groupby(['date']).sum())

def test_search_covid_tweets_emotion_table():
    res = search_covid_tweets_emotion_table()
    tweet_emotion_df = res[['date', 'avg_compound_score', 'avg_neg_score', 'avg_neu_score', 'avg_pos_score']]
    res = res.melt(id_vars='date')
    print(res)


def test_stat_df_other_stats():
    stat_df = search_covid_tweets_stat_table()
    stat_df_total_amount = stat_df[['date', 'total_num']]
    stat_df_total_amount = stat_df_total_amount.rename(columns={'date': 'index'}).set_index('index')
    stat_df_total_amount['day_of_week'] = stat_df_total_amount.index.dayofweek

    print(stat_df_total_amount)


if __name__ == '__main__':
    #test_highlight_target_ch()
    #test_search_covid_table()
    #test_stat_df_other_stats()
    #test_search_covid_text_table()
    test_search_covid_tweets_emotion_table()


