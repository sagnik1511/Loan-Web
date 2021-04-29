# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 19:47:54 2021

@author: sagnik1511
"""

# Libraries

import streamlit as st
import pandas as pd
import base64
from PIL import Image
from sklearn.ensemble import RandomForestClassifier as rfc
#-------------------------------------------------------


# Data elements for test value preparation
#-------------------------------------------------------
def value(lst,string):
    for i in range(len(lst)):
        if lst[i]==string:
            return i
jobs=['admin','blue-collar','entrepreneur','housemaid','managerial','retired','self-employed','services','student','technician','unemployed','others']
marital_status=['divorced','married','single']
education=['10th standard or lower','12th standard','graduate','postgraduate or higher']
yn=['NO','YES']
commn=['Cellular','Telephone','Others']
mon=['January','February','March','April','May','June','July','August','September','October','November','December']
outcome=['Failure','Other','Success','Unknown']
#---------------------------------------------------------

# Body Interface
#---------------------------------------------------------
main_bg = "assets/images/bg.jpg"
main_bg_ext = "jpg"

side_bg = "assets/images/bg.jpg"
side_bg_ext = "jpg"

image=Image.open('assets/images/head.jpg')
st.sidebar.image(image)
st.markdown("<h1 style='text-align: center; color:#7a000d;'>LOAN-WEB</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color:#7a000d;'>Customer Filtering Engine for Loan Marketing</h2>",unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color:#7a000d;'>Find out your perfect customer.</h3>",unsafe_allow_html=True)


st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)
#------------------------------------------------------------


# Sidebar Interface 
#------------------------------------------------------------
st.sidebar.markdown("""
                    
---                    
                    
Update your customer data here.

Submit to see results!!

""")
age= st.sidebar.slider("⦿ Age ( Customer's age in Years)",5,100)
job = st.sidebar.selectbox("⦿ Present Job : Customer's present Job",('admin','blue-collar','entrepreneur','housemaid','managerial','retired','self-employed','services','student','technician','unemployed','others'))
marriage = st.sidebar.selectbox("⦿ Marital Status of the user : ",('divorced','married','single'))
edu = st.sidebar.selectbox("⦿ Educational background : ",('10th standard or lower','12th standard','graduate','postgraduate or higher'))
defa = st.sidebar.selectbox('⦿ User possess Credit Card/Cards',('NO','YES'))
bal = st.sidebar.slider("⦿ Average yearly Balance (Lacks per annum) Negative values for debt ",-0.75,100.0)
housing=st.sidebar.selectbox('⦿ Has any housing Loan',('NO','YES'))
loan=st.sidebar.selectbox('⦿ Has any other Loan',('NO',"YES"))
comm=st.sidebar.selectbox('⦿ Contact Medium : ',('Cellular','Telephone','Others'))
day=st.sidebar.slider('⦿ Last Contact day of the month (If no contact till now leave this as it is)',1,30)
month=st.sidebar.selectbox('⦿ Last Contact month (If no contact till now leave this as it is)' ,('January','February','March','April','May','June','July','August','September','October','November','December'))
dur=st.sidebar.slider('⦿ Duration of last call (In minutes)IfNo contact then leave it as 0: ',0,120)
camp=st.sidebar.slider('⦿ Total Number of candidates will be called for this campaign',1,100)
pdays=st.sidebar.slider('⦿ Number of days that passed by after the client was last contacted from a previous campaign (set it -1 if it is the first approach)', int(-1),1095)
prev=st.sidebar.slider('⦿ Number of calls executed in this campaign',0,99)
out=st.sidebar.selectbox('⦿ Previous Campaign Outcome()If no previous campaign leave it as Unknown',('Failure','Success','Unknown','Other'))
#--------------------------------------------------------

# Main Function 
#--------------------------------------------------------

if st.sidebar.button('SUBMIT'):
    data ={
        'age':age,
        'job':value(jobs,job),
        'marital':value(marital_status,marriage),
        'education':value(education,edu),
        'default':value(yn,defa),
        'balance':(bal/90.17)*100000,
        'housing':value(yn,housing),
       'loan':value(yn,loan),
       'contact':value(commn,comm),
       'day':day,
       'month':value(mon,month),
       'duration':dur*60,
       'campaign':camp,
       'pdays':pdays,
       'previous':prev,
       'poutcome':value(outcome,out)
        }
    df=pd.DataFrame(data,index=[0])
    
    st.markdown("<h1 style='text-align: center; color:#7a000d;'>Engine Running.Processing Results........</h1>", unsafe_allow_html=True)
    data=pd.read_csv('assets/data/evaluation data/final_train.csv')
    clf=rfc(random_state=1,n_estimators=95)
    clf.fit(data.drop('y',1),data['y'])
    
    prediction=clf.predict(df)
    prob=clf.predict_proba(df)*100
    prob=pd.DataFrame(prob,columns=['Rejection Possibility(in %)','Accepting Possibily(in %)'])
    if int(prediction.reshape(1))==1:
        image = Image.open('assets/images/pos.png')
        st.image(image)
    else:
        image=Image.open('assets/images/neg.png')
        st.image(image)
    st.write(pd.DataFrame(prob),index=[0])
    
#--------------------------------------------------------------


# Footers 
#--------------------------------------------------------------
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color:red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
bottom: 0;
width:45%;

color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="http://happai.epizy.com" target="_blank">Sagnik Roy</a></p>
</div> 


"""
st.markdown(footer,unsafe_allow_html=True)
st.sidebar.markdown("""Follow me on [Kaggle](https://kaggle.com/sagnik1511) , [Instagram](https://www.instagram.com/tensored___/) , [Github](https://github.com/sagnik1511)""")
#-----------------------------------------------------------------