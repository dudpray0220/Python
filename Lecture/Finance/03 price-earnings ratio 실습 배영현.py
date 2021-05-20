#!/usr/bin/env python
# coding: utf-8

# In[1]:


import FinanceDataReader as web

from datetime import date, timedelta

import matplotlib.pyplot as plt

import datetime

import numpy as np


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
# 파이썬 코드가 아니고 주피터랩에서만 인식하는 특수문자 (%~) : 그래프를 안에서 띄워달라고 함

plt.figure(figsize=(15,9))

# today = date.today()

startday = date(2021,4,1)

endday = date(2021,5,14)

KAKAO = web.DataReader("035720", startday, endday)


# In[6]:


KAKAO = KAKAO[KAKAO['Volume'] != 0]

# SEC['Close'].head()


# In[7]:


# 1 씩 shift

KAKAO['Close'].shift(1).head()


# In[9]:


# 일반 수익률 계산 (일반 수익률 = (미래가격 – 이전가격) / 이전가격 )
# shift(-1)은 위로 감 / shift(1)은 아래로 이동

KAKAO['Rate'] = (KAKAO['Close'].astype(float)-KAKAO['Close'].shift(1).astype(float)) / KAKAO['Close'].shift(1).astype(float)


# In[15]:


KAKAO["Rate"].plot(figsize=(16,4), color='dodgerblue')

plt.show()

