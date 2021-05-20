#!/usr/bin/env python
# coding: utf-8

# ### 1. 라이브러리 선언하기

# In[1]:


# 데이터 조작 라이브러리
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

indata = pd.read_csv("../dataset/kopo_decision_tree_all_new.csv")
indata.columns.str.lower()

targetDbIp = "192.168.110.111"
targetDbPort = "5432"
targetDbId = "kopo"
targetDbPw = "kopo"
targetDbName = "kopodb"
targetDbPrefix = "postgresql://"

targetUrl = "{}{}:{}@{}:{}/{}".format(targetDbPrefix,
                                      targetDbId,
                                      targetDbPw,
                                      targetDbIp,
                                      targetDbPort,
                                      targetDbName)

pg_kopo_engine = create_engine(targetUrl)

tableName = "pg_result_yh"

try:
    indata.to_sql(name=tableName,
                  con = pg_kopo_engine,
                  if_exists="replace", index=False)
    print("{} unload 성공!".format(tableName))
except Exception as e:
    print(e)


# In[ ]:




