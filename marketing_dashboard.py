# Importing Libraries
import os
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config("Marketing Dashboard", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Bank Marketing Dashboard")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
# setting up the file uploader
fl = st.file_uploader(":file_folder: Upload your file", ["csv", "xlsx", "xls"])
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
    df = pd.read_csv("marketing.csv")
month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
               'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
# Creating a filter for the dashboard
st.sidebar.title("Filter")
st.sidebar.header("Choose your filter")
job = st.sidebar.multiselect("Select a Job role", df["job"].unique())
if not job:
    df1 = df.copy()
else:
    df1 = df[df["job"].isin(job)]
col1, col2 = st.columns(2)
# Creating charts for the dashboard
with col1:
    st.metric("Total Number of Customers", df1["y"].count())
with col2:
    subscription_rate = (df1["y"].value_counts()["yes"]/df1["y"].count())*100
    st.metric("Subscription Rate", f"{subscription_rate:.2f}%")

ta = df1.groupby("month", as_index=False)["campaign"].sum()
st.subheader("Trend of No of Contacts")
fig = px.line(ta, x="month", y="campaign")
st.plotly_chart(fig, use_container_width=True)
y = df1["y"]
com = pd.DataFrame(df1["contact"], columns=["contact"])
com = com.groupby("contact", as_index=False).sum()
com["count"] = df1["contact"].value_counts().values.tolist()
with col1:
    st.subheader("Count of Subscribed and Unsubscribed Customers")
    fig = px.histogram(y, x="y", histfunc="count")
    fig.update_layout(xaxis_title="Subscribed")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Mode of Contact")
    fig = px.pie(com, values="count", names="contact", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)
cl1, cl2 = st.columns(2)
with cl1:
    st.subheader("Level of Education of Customers")
    fig = px.histogram(df1, x="education", color="y", barmode="stack",
                       histfunc="count")
    st.plotly_chart(fig, use_container_width=True)
married = df1[df1["marital"]=="married"]
single = df1[df1["marital"]=="single"]
divorced = df1[df1["marital"]=="divorced"]


mari = {"marital":["married", "married", "single", "single", "divorced", "divorced"],
        "sub":[married["y"].value_counts().index.tolist()[0],
               married["y"].value_counts().index.tolist()[1],
               single["y"].value_counts().index.tolist()[0],
               single["y"].value_counts().index.tolist()[1],
               divorced["y"].value_counts().index.tolist()[0],
               divorced["y"].value_counts().index.tolist()[1]],
        "values":[married["y"].value_counts().values.tolist()[0],
                  married["y"].value_counts().values.tolist()[1],
                  single["y"].value_counts().values.tolist()[0],
                  single["y"].value_counts().values.tolist()[1],
                  divorced["y"].value_counts().values.tolist()[0],
                  divorced["y"].value_counts().values.tolist()[1]]}
mari = pd.DataFrame(mari, columns=["marital", "sub", "values"])
with cl2:
    st.subheader("Relationship Status of Customers")
    fig = px.treemap(mari, path=["marital","sub"], values="values",
                     template="plotly_white",
                     color_discrete_map={"married": "blue",
                                         "single": "white",
                                         "divorced":"orange"})
    st.plotly_chart(fig, use_container_width=True)
st.subheader("Age Distribution of the Customers.")
fig = px.histogram(df1, x="age", color="y", barmode="stack",
                   hover_data={"age":True, "y":True })
st.plotly_chart(fig, use_container_width=True)








