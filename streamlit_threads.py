import streamlit as st
import json
import os
import datetime as dt
import pandas as pd
import altair as alt
import plotly.express as px
from makedatabymin import makedata, popwords, popmedia
from updatethreads import updatethreadreplies

st.set_page_config(layout="wide")
st.title("/Fishtank.live/ Trends")

st.sidebar.header('Time Interval')
timeint = st.sidebar.selectbox(" ", ("1 min","5 min","10 min","30 min","1 hour","3 hour","6 hour","12 hour","24 hour"),index=8)

st.sidebar.header('Select your fish')
fish_names = st.sidebar.multiselect(" ",["Josie","Jon","Letty","Vance","Sylvia","Damiel","Mauro","Simmons","Jet","Ben","Jason","Lance","Frank","Simon","Chris","Betty","Ella"],["Josie","Jon","Letty","Vance","Sylvia","Damiel","Mauro","Simmons"])
st.sidebar.header("Custom Values")
custom_names = st.sidebar.text_input("Comma separated")

topword_count = st.sidebar.number_input("Top words",value=10, step=1)
topmedia_count = st.sidebar.number_input("Top media",value=10, step=1)

st.sidebar.button("Regenerate Data")

with st.sidebar.expander("About me"):
    st.write("If you would like to reach out for questions/suggestions, contact me at:")
    st.text("Twitter: @YoungMOOBY")
    st.text("Discord: YoungBreezy#2000")
    st.text("")
    st.write("If you appreciate my work and would like to donate:")
    st.text("Cashapp: $MMMOOOBBB")
    st.text("Venmo: @MMOOBB")
    st.text("Paypal: paypal.me/mmoobb1")
    st.text("Bitcoin: 1CuagmLJFNpvXQb4Ya1Ht8BbU8WeR9h7gz")

contplot = st.container()

today = dt.datetime.combine(dt.date.today(),dt.time(0,0,0))

daterange = st.slider("Select Date Range",dt.datetime(2023,4,18,0,0,0),dt.datetime(2023,5,30,0,0,0),(dt.datetime(2023,4,18,0,0,0),today))#dt.datetime(2023,5,21,0,0,0)))

timecol1, timecol2 = st.columns(2)
with timecol1:
    starttime = st.slider("Start time", dt.time(0,0),dt.time(23,45))
with timecol2:
    endtime = st.slider("End time", dt.time(0,0),dt.time(23,45))


def regdata(names, interval, start, end):
    if not names:
        return
    pdata_list = []
    dash=[]
    for name in names:
        if os.path.exists(f"data/{name}"):
            continue
        makedata(name)
    for name in names:
        pdata_pre = pd.read_csv(f"data/{name}",index_col="time")
        pdata_list.append(pdata_pre)
        if len(dash)%30 < 10:
            dash.append('solid')
        elif len(dash)%30 < 20:
            dash.append('dash')
        elif len(dash)%30 < 30:
            dash.append('dashdot')
    pdata = pd.concat(pdata_list, axis='columns')
    pdata.index = pd.to_datetime(pdata.index)
    pdata = pdata.loc[start:end]
    pdata = pdata.resample(f'{interval}T').sum()
    pdataj = pdata
    pdataj.index = pdataj.index.strftime('%Y-%m-%d %H:%M:%S')
    pdataj = pdata.to_dict("index")
    #print(pdata)
    #print(json.dumps(pdataj, indent = 4))
    with open("alldatalol", "w") as alldata:
        alldata.write(json.dumps(pdataj, indent=4))
    fig = px.line(pdata, x=pdata.index, y=names)
    return fig


custom_names_list = [n.strip() for n in custom_names.split(',')]

names = fish_names+custom_names_list
try:
    while True:
        names.remove("")
except:
    pass
val, unit = timeint.split(" ")
if unit == "min":
    interval = val
elif unit == "hour":
    interval = int(val)*60

if type(daterange) == tuple:
    start, end = daterange
    start = dt.datetime.combine(start, starttime)
    end = dt.datetime.combine(end, endtime)
else:
    start = end = daterange
    start = dt.datetime.combine(start, starttime)
    end = dt.datetime.combine(end, endtime)

fig = regdata(names,interval, start, end)
contplot.plotly_chart(fig, use_container_width=True)

topwordscol, topmediacol = st.columns(2)

ignore = ['the', 'to', 'a', 'and', 'is', 'i', 'of', 'you', 'in', 'it', 'this', 'that', 'for', 'he', 'her', 'on', 'she', 'was', 'with', 'they', 'just', 'be', 'are', 'like', 'so', 'not', 'have', 'but', 'what', 'all', 'his', 'him', 'about','if', 'out', 'do', "it's", 'at', 'has', 'get', 'no', 'as', 'or', 'how', 'will', 'now', 'them', 'my', 'would', 'when', 'can', 'me', 'because', 'from', "he's", 'even', 'who', 'an', 'did', 'think', 'why', 'your', 'going', 'more', "don't", 'by', 'being', "she's", 'only', "i'm", 'we', 'know', 'been', 'there', 'really', 'some', 'too', 'got', 'go', 'their', 'make', 'its', 'than', 'want', 'into', 'had', 'still', 'after', 'then', 'said', 'see', 'these', 'much', "can't", 'does', "you're", 'here', 'way', 'got', 'go', 'their', 'make', 'its', 'than', 'want', 'into', 'had', 'still', 'after', 'then', 'said', 'see', 'these', 'much', "can't", 'does', "you're", 'here', 'way', 'should', 'someone', "that's", 'any', "doesn't", 'were', 'getting', 'other', 'everyone', 'something', 'gonna', 'thing', 'doing', 'guy', "they're", 'again', 'where', "didn't"]




with topmediacol:
    st.header(f"Most common {topmedia_count} media")
    topmedia = popmedia(topmedia_count, start, end)
    imgcol1, imgcol2, imgcol3 = st.columns(3)
    icol = 1
    for i,v in topmedia:
        filename = v["filename"]
        link = v["link"]
        mcount = v["count"]
        if icol == 1:
            icol = 2
            with imgcol1:
                if "web" in link:
                    print("test")
                    st.video(link)
                    st.text(f"filename: {filename}\ncount:{mcount}")
                else:
                    st.image(link, width = 200, caption=f"filename: {filename}\ncount:{mcount}")
        elif icol == 2:
            icol = 3
            with imgcol2:
                if "web" in link:
                    st.video(link)
                    st.text(f"filename: {filename}\ncount:{mcount}")
                else:
                    st.image(link, width = 200, caption=f"filename: {filename}\ncount:{mcount}")

        elif icol == 3:
            icol = 1
            with imgcol3:
                if "web" in link:
                    st.video(link)
                    st.text(f"filename: {filename}\ncount:{mcount}")
                else:
                    st.image(link, width = 200, caption=f"filename: {filename}\ncount:{mcount}")

with topwordscol:
    st.header(f"Most common {topword_count} words")
    topwords = popwords(topword_count,start,end, ignore)
    words = []
    wcount = []
    for i,v in topwords:
        words.append(i)
        wcount.append(v)
    table = pd.DataFrame(wcount,words)
    st.table(table)


print("done making datya")

#pdata1 = pd.read_csv("data/Josie",index_col="time")
#pdata2 = pd.read_csv("data/Letty",index_col="time")

#print(pdata1)
#pdata1.set_index('time', inplace=True)
#pdata2.set_index('time', inplace=True)

#pdata = pd.concat([pdata1, pdata2], axis='columns')

#pdata.index = pd.to_datetime(pdata.index)
#pdata = pdata.resample('30T').sum()

#fig = px.line(pdata.reset_index(), x="time", y=["josie","Letty"])
#st.plotly_chart(fig)













#st.altair_chart(chart, use_container_width=True)
#st.line_chart(pdata)

#chart = alt.Chart(pdata).mark_line().encode(
#    x='time:T',
#    y='value:Q'
#)
