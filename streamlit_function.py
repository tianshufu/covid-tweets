import streamlit as st
import aws_opensearch
import util
import pandas as pd
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px


def set_home():
    md_parasite = 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UY720_.jpg'
    md_boyhood = 'https://m.media-amazon.com/images/M/MV5BMTYzNDc2MDc0N15BMl5BanBnXkFtZTgwOTcwMDQ5MTE@._V1_FMjpg_UX1000_.jpg'
    md_endgame = 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UY720_.jpg'
    md_interstellar = 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UY720_.jpg'
    md_showman = 'https://m.media-amazon.com/images/M/MV5BYjQ0ZWJkYjMtYjJmYS00MjJiLTg3NTYtMmIzN2E2Y2YwZmUyXkEyXkFqcGdeQXVyNjk5NDA3OTk@._V1_FMjpg_UY720_.jpg'
    md_split = 'https://m.media-amazon.com/images/M/MV5BZTJiNGM2NjItNDRiYy00ZjY0LTgwNTItZDBmZGRlODQ4YThkL2ltYWdlXkEyXkFqcGdeQXVyMjY5ODI4NDk@._V1_FMjpg_UY720_.jpg'
    md_sw_despertar = 'https://m.media-amazon.com/images/M/MV5BOTAzODEzNDAzMl5BMl5BanBnXkFtZTgwMDU1MTgzNzE@._V1_FMjpg_UY720_.jpg'
    md_lalaland = 'https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_FMjpg_UY720_.jpg'
    #st.header('Relaciones entre valoraciones de público y crítica, y la recaudación\n Películas en IMDb 2014 - 1019')
    #st.subheader('Relaciones entre valoraciones de público y crítica, y la recaudación')

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    with col1:
        st.image(md_parasite, use_column_width='always')
    with col2:
        st.image(md_endgame, use_column_width='always')
    with col3:
        st.image(md_showman, use_column_width='always')
    with col4:
        st.image(md_interstellar, use_column_width='always')
    with col5:
        st.image(md_boyhood, use_column_width='always')
    with col6:
        st.image(md_split, use_column_width='always')
    with col7:
        st.image(md_sw_despertar, use_column_width='always')
    with col8:
        st.image(md_lalaland, use_column_width='always')

    #st.write(intro, unsafe_allow_html=True)
    #st.write(intro_herramientas_fuentes, unsafe_allow_html=True)




def load_css(file_name):
    """
    Helper function for loading css
    Ref: https://discuss.streamlit.io/t/colored-boxes-around-sections-of-a-sentence/3201
    :param file_name:
    :return:
    """
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



def set_search():
    load_css("style.css")
    st.markdown(
        '<h1 style="background-color: #F0F2F6; padding-left: 10px; padding-bottom: 20px;">Tweets covid Search Engine</h1>',
        unsafe_allow_html=True)
    query = st.text_input('', help='Enter the search string and hit Enter/Return')
    # query = query.replace(" ", "+")  # replacing the spaces in query result with +

    # t = "<div>Hello there my <span class='highlight blue'>name</span> is <span class='highlight red'>Fanilo <span class='bold'>Name</span></span></div>"

    # st.markdown(t, unsafe_allow_html=True)

    # debug code

    # set the session state for the page
    if "curpage" not in st.session_state:
        # set the initial default value of the slider widget
        st.session_state.curpage = 0
    # initial the session state with query input
    if "searchtext" not in st.session_state:
        st.session_state.searchtext = query

    # This will get the value of the slider widget
    #st.write(st.session_state.curpage)

    def on_page_changed(page_num):
        #print(f"Test function:{page_num}")
        # st.write(f"Test function:{page_num}")
        st.session_state.curpage = page_num

    #
    if query:  # Activates the code below on hitting Enter/Return in the search textbox
        try:  # Exception handling
            # if query !
            print(f"new request with session {st.session_state.curpage}")
            result_str = '<html><table style="border: none;">'  # Initializing the HTML code for displaying search results
            res_dic = aws_opensearch.search_words_from_es(query.strip(), st.session_state.curpage * 10, 10)
            search_result = res_dic["results"]
            # total num of results
            total_num = res_dic["total_num"]
            time_took = int(res_dic["time_took"]) / 1000
            # print(search_result)
            for i, res in enumerate(search_result):  # iterating through the search results
                # print(res)
                # print(type(res))

                id = res["_id"]
                date_str = res["_source"]["date"]
                likes = res["_source"]["likes"]
                text = res["_source"]["text"]
                text_highlight = util.highlight_target_ch(text, query)
                text_lists = text.split(' ')
                text_head = " ".join(text_lists[0:3])
                # print(id,date_str,likes,text)
                url = "https://twitter.com/Hadly_/status/" + str(id)
                count_str = f'<b style="font-size:20px;">ES Search returned {total_num} results, took {time_took}s</b>'
                ########################################################
                ######### HTML code to display search results ##########
                ########################################################
                result_str += f'<tr style="border: none;">' + \
                              f'<td  style="border: none;" ><h3><a href="{url}" target="_blank">{st.session_state.curpage*10+i+1}.{text_head}</a></h3></td>' + \
                              f'<td  style="border: none;" ><img src="https://img.icons8.com/color/24/000000/filled-like.png"/></td>' + \
                              f'<td  style="border: none;" >{int(likes)}</td>' + \
                              f'</tr>' + \
                              f'<tr style="border: none;"><td  style="border: none;" ><strong style="color:green;">{date_str}</strong></td></tr>' + \
                              f'<tr style="border: none;"><td  style="border: none;" ><div>{text_highlight}</div></td></tr>' + \
                              f'<tr style="border: none;"><td style="border: none;"></td></tr>'
                result_str += '</table></html>'
        except:
            result_str = '<html></html>'
            count_str = '<b style="font-size:20px;">Looks like an error!!</b>'

        st.markdown(f'{count_str}', unsafe_allow_html=True)
        st.markdown(f'{result_str}', unsafe_allow_html=True)
        # get the total num of pages
        if total_num <= 10:
            page_num = 1
        else:
            page_num = total_num // 10 + 1
        # Ref: https://gist.github.com/treuille/2ce0acb6697f205e44e3e0f576e810b7
        col1,_ = st.columns([1,3])
        with col1:
            page_format_func = lambda i: "Page %s" % i
            option = st.selectbox("", range(page_num), format_func=page_format_func)
            # st.session_state.curpage = option
            page_change_button = st.button('Go to Page', on_click=on_page_changed, args=(option,))
        #st.write("Cur page session", st.session_state.curpage)

        #st.write('You selected:', option)

def set_tweets_stat():
    # get all the info from the database
    stat_df = util.search_covid_tweets_stat_table()
    # get the sub column of total_num
    stat_df_total_amount = stat_df[['date','total_num']]
    # since streamlit will choose the 'index' to be the x-axis, have to rename and set_index
    stat_df_total_amount = stat_df_total_amount.rename(columns={'date': 'index'}).set_index('index')
    # get the day of week
    stat_df_total_amount['day_of_week'] = stat_df_total_amount.index.dayofweek
    # get the weekend or not weekend
    stat_df_total_amount['is_weekend'] = stat_df_total_amount['day_of_week'].apply(lambda x: "weekend" if (x >= 5 ) else "weekday")

    # get other stat
    stat_df_other_stats = stat_df[['date','avg_likes','avg_quotes','avg_replys','avg_retweets']]
    stat_df_other_stats = stat_df_other_stats.rename(columns={'date': 'index'}).set_index('index')
    stat_df_other_stats['day_of_week'] = stat_df_other_stats.index.dayofweek
    stat_df_other_stats['is_weekend'] = stat_df_other_stats['day_of_week'].apply(lambda x: "weekend" if (x >= 5 ) else "weekday")

    st.title("Tweets Stat Visualisation")
    st.markdown("""
                This dashboard contains the basic analysis of all the tweets since `2021-12-20` related to Covid-19. The dash board contains
                 mainly three part: 1.General social stats of all the tweets 2.Key word analysis 3.Tweet sentiment analysis 
                """)
    st.subheader("Tweets general social stats")
    menu_relations = st.radio(
        "",
        ("Total Num", "Avg likes", "Avg quotes", "Avg replys","Avg retweets"),
    )

    with st.expander("Tweet data description"):
        st.code(stat_df.describe())

    if menu_relations == "Total Num":
        col1, col2 = st.columns([3,1])
        with col1:
    #df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
            fig = px.bar(stat_df_total_amount, x=stat_df_total_amount.index, y="total_num",color="is_weekend")
            fig.update_xaxes(rangeslider_visible=True)
            fig.update_layout(paper_bgcolor="#F0F2F6")
            col1.plotly_chart(fig, use_container_width=True)
        with col2:
            fig_box  = px.box(stat_df_total_amount, y="total_num")
            fig_box.update_layout(paper_bgcolor="#F0F2F6")
            col2.plotly_chart(fig_box, use_container_width=True)


    elif menu_relations == "Avg likes":
        col1, col2 = st.columns([3, 1])
        with col1:
            fig2 = px.bar(stat_df_other_stats,x= stat_df_other_stats.index,y="avg_likes",color="is_weekend")
            fig2.update_xaxes(rangeslider_visible=True)
            fig2.update_layout(paper_bgcolor="#F0F2F6")
            col1.plotly_chart(fig2, use_container_width=True)
        with col2:
            fig_box = px.box(stat_df_other_stats, y="avg_likes")
            fig_box.update_layout(paper_bgcolor="#F0F2F6")
            col2.plotly_chart(fig_box, use_container_width=True)


    elif menu_relations == "Avg_quotes":
        col1, col2 = st.columns([3, 1])
        with col1:
            fig2 = px.bar(stat_df_other_stats, x=stat_df_other_stats.index, y="avg_quotes", color="is_weekend")
            fig2.update_xaxes(rangeslider_visible=True)
            fig2.update_layout(paper_bgcolor="#F0F2F6")
            col1.plotly_chart(fig2, use_container_width=True)
        with col2:
            fig_box = px.box(stat_df_other_stats, y="avg_quotes")
            fig_box.update_layout(paper_bgcolor="#F0F2F6")
            col2.plotly_chart(fig_box, use_container_width=True)

    elif menu_relations == "Avg replys":
        col1, col2 = st.columns([3, 1])
        with col1:
            fig2 = px.bar(stat_df_other_stats, x=stat_df_other_stats.index, y="avg_replys", color="is_weekend")
            fig2.update_xaxes(rangeslider_visible=True)
            fig2.update_layout(paper_bgcolor="#F0F2F6")
            col1.plotly_chart(fig2, use_container_width=True)
        with col2:
            fig_box = px.box(stat_df_other_stats, y="avg_replys")
            fig_box.update_layout(paper_bgcolor="#F0F2F6")
            col2.plotly_chart(fig_box, use_container_width=True)

    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            fig2 = px.bar(stat_df_other_stats, x=stat_df_other_stats.index, y="avg_retweets", color="is_weekend")
            fig2.update_xaxes(rangeslider_visible=True)
            fig2.update_layout(paper_bgcolor="#F0F2F6")
            col1.plotly_chart(fig2, use_container_width=True)
        with col2:
            fig_box = px.box(stat_df_other_stats, y="avg_retweets")
            fig_box.update_layout(paper_bgcolor="#F0F2F6")
            col2.plotly_chart(fig_box, use_container_width=True)

    st.subheader('Key Word Analysis: Omicron vs Delta')
    # load the data for key word analysis
    key_word_df = util.search_covid_tweets_key_words_table()

    with st.expander("Tweet key word data description"):
        st.code(key_word_df.describe())
    # sort by date
    key_word_df = key_word_df.sort_values(by='date')
    # pivot longer the data frame for visualisation
    # Ref : https://medium.com/predmatic/reshaping-data-frames-using-pandas-melt-and-pivot-8fe65a30a252
    key_word_df_melt =  key_word_df .melt(id_vars='date')
    col3,col4 = st.columns([3,1])
    with col3:
        # plot the line plot of delta and omicron line
        fig = px.line(key_word_df_melt, x="date", y="value",color='variable',title="Trend of Omicron and Delta")
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(paper_bgcolor="#F0F2F6")
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        # plot the pie chart of the latest day
        # get the total sum of each genirics
        #key_word_sum = key_word_df_melt.groupby('variable').sum()
        delta_sum = key_word_df['delta_cnt'].sum()
        omicron_sum = key_word_df['omicron_cnt'].sum()
        fig2 = px.pie(values=[omicron_sum,delta_sum], names=['Omicron','Delta'],color_discrete_map={"Omicron":'red',"Delta":'blue'},title="Omicron vs Delta")
        fig2.update_layout(paper_bgcolor="#F0F2F6")
        st.plotly_chart(fig2,use_container_width=True)

    st.subheader("Tweets sentiment score")
    tweet_emotion_df = util.search_covid_tweets_emotion_table().sort_values(by='date')
    with st.expander("Tweet Emotion data description"):
        st.code(tweet_emotion_df.describe())
    col5,col6 =st.columns([1,1])
    with col5:
        # load the tweets emotion analysis df and sort by date
        #tweet_emotion_df = util.search_covid_tweets_emotion_table().sort_values(by='date')
        # get the sub score df
        tweet_emotion_score_df = tweet_emotion_df[['date','avg_compound_score','avg_neg_score','avg_neu_score','avg_pos_score']]
        # pivot longer the df for visualisation
        tweet_emotion_score_df_melt = tweet_emotion_score_df.melt(id_vars='date')
        fig = px.line(tweet_emotion_score_df_melt, x="date", y="value", color='variable', title='Tweets Emotion Score',
                      color_discrete_map= {"avg_compound_score":'black',"avg_neg_score":'red',"avg_neu_score":'gray',"avg_pos_score":'blue'}
                      )
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(paper_bgcolor="#F0F2F6")
        st.plotly_chart(fig, use_container_width=True)
    with col6:
        # get the sub rate df
        tweet_emotion_rate_df = tweet_emotion_df[['date','neg_rate','neu_rate','pos_rate']]
        fig = px.bar(tweet_emotion_rate_df, x="date", y=["pos_rate", "neu_rate", "neg_rate"], title="Tweets Emotion Rate",
                     color_discrete_map = {"pos_rate": 'blue',"neu_rate":'gray',"neg_rate":'red'})
        fig.update_layout(paper_bgcolor="#F0F2F6")
        st.plotly_chart(fig, use_container_width=True)












def test_stat_df_other_stats():
    stat_df = util.search_covid_tweets_stat_table()
    stat_df_total_amount = stat_df[['date', 'total_num']]
    stat_df_total_amount = stat_df_total_amount.rename(columns={'date': 'index'}).set_index('index')
    stat_df_total_amount['day_of_week'] = stat_df_total_amount['index'].dt.dayofweek




if __name__ == '__main__':
    test_stat_df_other_stats()


