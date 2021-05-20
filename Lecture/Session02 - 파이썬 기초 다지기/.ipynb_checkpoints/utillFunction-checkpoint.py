#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# 함수역할 : ~~~~
# 입력파라미터 : inValue : 숫자형 데이터
# 출력값 : 입력받은 숫자를 반올림 처리한 결과 반환
# 비고 : ~~~~


def roundFunction(inValue):
    # 함수를 개발하기위한 디버깅코드
    # Step1: 입력받은 데이터를 반올림 자리수만큼 곱해준다.
    # inValue = 1.893430903490
    step1 = inValue * 100


    # Step2: 곱해준결과에 0.5를 더한 후 소수점이하 버림!
    step2 = int(step1 + 0.5)

    # Step3: 100으로 나누어준다.
    step3 = step2 / 100
    outValue = step3
    
    return outValue

