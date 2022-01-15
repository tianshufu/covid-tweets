import streamlit as st
import pandas as pd
import  streamlit_function
st.set_page_config(page_title='Twitter - Covid',
                   page_icon='https://tianshufu.site/104501_twitter_bird_icon.png',
                   layout="wide")

#st.sidebar.image('https://ane4bf-datap1.s3-eu-west-1.amazonaws.com/wmocms/s3fs-public/styles/featured_media_detail/public/advanced_page/featured_media/coronavirus-banner.jpg?Q5nNiocqqI30_Jy2.RwhGYpwU7fNVCAp&itok=REf-9mAr', width=300)
st.sidebar.image('https://southkingstownri.com/ImageRepository/Document?documentID=3809',width = 300)
st.sidebar.header('Twitter covid analysis')
st.sidebar.markdown('Real time daily analysis of covid-19 Twitter data')


menu = st.sidebar.radio(
    "",
    ("Project Introduction", "Word Search Engine", "Tweets Stat Visualisation"),
)



# lay the button horizontally
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write('Tianshu Fu | https://tianshufu.net/')


if menu == 'Project Introduction':
    streamlit_function.set_home()

if menu == 'Word Search Engine':
    streamlit_function.set_search()
if menu == 'Tweets Stat Visualisation':
    streamlit_function.set_tweets_stat()


