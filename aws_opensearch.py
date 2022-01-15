import requests
from requests.auth import HTTPBasicAuth
import json
from sqlalchemy import create_engine
import pandas as pd
import time
import streamlit as st

user_name = st.secrets["db_username"]
password = st.secrets["db_password"]
search_url = "https://search-twitter-covid-data-gmgce6zcfpiv44xe5e3b6cxzcu.us-east-1.es.amazonaws.com/movies/_search?q=mars&pretty=true"
# response = requests.get(
#   search_url,
#   auth=HTTPBasicAuth(user_name, password)
# )
#
# print(response.text)
domain_endpoint = "https://search-twitter-covid-data-gmgce6zcfpiv44xe5e3b6cxzcu.us-east-1.es.amazonaws.com"

upload_url = domain_endpoint+"/tweeter/_doc/1"
dic = {'id':"1472793906773327882" ,'text':"Wheres booster vaccine kids Coronavirus Omicron ITLivestream","likes":1,"date":"2021-12-21"}
headers = {'Content-type': 'application/json'}
#json_dic = json.dumps(dic)
#upload_response = requests.post(upload_url,json_dic,auth = HTTPBasicAuth(user_name,password),headers=headers)
#print(upload_response.json())

def upload_single(dic):
    """
    upload single row to the aws open search service, the id will
    we generated automatically
    :param dic: dic containing the info
    :return: success or not
    """
    #json.loads(dic)
    id_str = dic['id']
    upload_url = domain_endpoint + "/tweeter/_doc/"+id_str
    json_dic = json.dumps(dic)
    upload_response = requests.post(upload_url, json_dic, auth=HTTPBasicAuth(user_name, password), headers=headers)
    #print(upload_response.ok)
    return upload_response.ok
    #response_dic = json.load(upload_response.json())
    #print(response_dic)
    #print(response_dic["success"])
    #print(upload_response.json())

def search_by_sql(sql_str):
    """
    pass in the sql_str format, search in the aws open search service
    :param sql_str:
    :return: json format of ans
    """
    search_url = domain_endpoint+"/_plugins/_sql"
    search_headers = {'Content-Type': 'application/x-ndjson'}
    data = {"query":sql_str}
    search_data_dic = json.dumps(data)
    search_response = requests.post(search_url, search_data_dic, auth=HTTPBasicAuth(user_name, password),headers= search_headers)
    print(search_response.json())

def search_by_es(es_dic):
    """
    pass in the es language search format and perform the search
    :param es_dic:
    :return:
    """
    search_url = domain_endpoint +"/tweeter/_search"
    search_response = requests.get(
       url= search_url,
       data= json.dumps(es_dic),
       headers = headers,
       auth=HTTPBasicAuth(user_name, password)
    )
    #print(search_response.json())
    return  json.loads(search_response.text)


def get_date_data_from_mysql(date_str):
    """
    Given the date str format ,return the data frame consist of of (id,text)
    :param date_str: exp:"2021-12-22"
    :return: (id,text) data frame
    """
    db_connection_str = 'mysql+pymysql://admin:fts970914@database-1.cm4w5eqwv8zj.us-east-1.rds.amazonaws.com/covid'
    db_connection = create_engine(db_connection_str)
    search_sql = """
        select tc.id as id, date(tc.created_at) as date ,ct.cleaned_text as text,tc.likes as likes
        from  twitter_covid as tc
        left join covid_text as ct
        on tc.id = ct.id
        where date(tc.created_at)= %(date)s
        and tc.likes > 10 


    """
    df = pd.read_sql(search_sql,
                     con=db_connection,
                     params={"date": date_str},
                     )
    df["date"] = date_str
    return df


def df_to_jsons(df):
    """
    turn df to list of json files
    :param df:
    :return:
    """
    json_str = df.to_json(orient='records', lines=True)
    json_list = json_str.split('\n')
    return json_list

def insert_to_es_from_mysql_by_date(date_str):
    """
    Pass in the parameter of the date_str, get the data from mysql,
    insert the data to es
    :param date_str:
    :return:
    """
    # get the df
    date_df = get_date_data_from_mysql(date_str)
    # turn to list of json
    date_jsons_list = df_to_jsons(date_df)
    n = len(date_jsons_list)
    i = 0
    print("total num: "+str(n))
    # iterate the list to insert
    for dic_str in date_jsons_list:
        # turn dic_str to dic
        #time.sleep(2)
        dic = json.loads(dic_str)
        if(upload_single(dic)):
            i += 1
            print("Finnished element:"+str(i))


def get_values_by_response(res):
    """
    Take the dic format of the response and retrieve the corresponding values
    from the dic, return the dic format
    :param res:
    :return:
    """
    ans = {}
    # list of all the results, in json format
    ans["results"] = res['hits']['hits']
    # total ans
    ans["total_num"] = res['hits']['total']['value']
    # time took in ms
    ans["time_took"] = res['took']
    return ans


def search_words_from_es(text,start,size):
    """
    Search words from es
    :param text: str format of input
    :param start:
    :param size:
    :return: dic contains all tweets in list format: ans["results"]
             total num of ans: ans["total_num"]
             time took to search:  ans["time_took"]
    """
    cur_search_dic = {
        "from": start,
        "size": size,
        "query": {
            "wildcard": {
                "text": text+"*"
            }
        },
        "sort": [
            {"likes": {"order": "desc"}}
        ]
    }
    # get the result from the server and turn to dic format
    res = search_by_es(cur_search_dic)
    # get the wanted information and return as a dic 
    cleaned_res = get_values_by_response(res)
    return cleaned_res


def test_upload_single():
    dic2 = {'id':"1472793909990363138",'text':"Wational US Sen Elizabeth Warren said Sunday tested positive COVID19 country deals another surge cases emergence omicron variant","likes":2,"date":"2021-12-21"}
    upload_single(dic2)


def test_search_by_sql():
    sql_str = "select * from tweeter"
    search_by_sql(sql_str)

def test_search_by_es():
    search_dic = {
      "from": 0,
      "size": 10,
      "query": {
        "wildcard": {
          "text": "covid*"
        }
      },
      "sort": [
            {"likes": {"order": "desc"}}
        ]
    }
    res = search_by_es(search_dic)
    print(type(res))
    print(res)

def test_search_words_from_es():
    res = search_words_from_es("covid",0,10)
    print(res["results"])


def test_insert_to_es_from_mysql_by_date():
    date_str = "2021-12-31"
    insert_to_es_from_mysql_by_date(date_str)

if __name__ == '__main__':
    #test_search_by_sql()
    #test_search_by_es()
    #test_upload_single()
    test_insert_to_es_from_mysql_by_date()
    #test_search_words_from_es()

