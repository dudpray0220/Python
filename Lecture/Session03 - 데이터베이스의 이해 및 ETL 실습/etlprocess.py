#!/usr/bin/env python
# coding: utf-8

# ### 1. 라이브러리 선언하기

# In[1]:


# 데이터 조작 라이브러리
import pandas as pd


# In[1]:


import psycopg2
from sqlalchemy import create_engine


# In[1]:


### 2. 데이터 불러오기


# In[1]:


# pwd


# In[4]:


indata = pd.read_csv("../dataset/kopo_decision_tree_all_new.csv")
indata


# In[5]:


indata.shape


# ### 3. 데이터 처리 (컬럼 소문자로 변환)

# In[6]:


indata.columns.str.lower()


# ### 4. 데이터 저장하기

# In[7]:


targetDbIp = "192.168.110.111"
targetDbPort = "5432"
targetDbId = "kopo"
targetDbPw = "kopo"
targetDbName = "kopodb"


# In[8]:


targetDbPrefix = "postgresql://"


# In[9]:


targetUrl = "{}{}:{}@{}:{}/{}".format(targetDbPrefix,
                                      targetDbId,
                                      targetDbPw,
                                      targetDbIp,
                                      targetDbPort,
                                      targetDbName)
targetUrl


# In[10]:


pg_kopo_engine = create_engine(targetUrl)


# In[11]:


tableName = "pg_result_yh"


# In[12]:


try:
    indata.to_sql(name=tableName,
                  con = pg_kopo_engine,
                  if_exists="replace", index=False)
    print("{} unload 성공!".format(tableName))
except Exception as e:
    print(e)


# In[ ]:




