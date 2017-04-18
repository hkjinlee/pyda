# -*- coding: utf-8 -*-

'''
GA(Google Analytics) 예제

- google2pandas(https://github.com/panalysis/Google2Pandas) 패키지 기반
- pandas도 자체적으로 GA API를 지원하나 python 3.6 기준으로 의존성 깨져 사용 불가

사전 준비사항:
!pip install --upgrade google-api-python-client
!pip install git+https://github.com/panalysis/Google2Pandas

'''

from google2pandas import *

#%% OAuth 인증
VIEW_ID = '112942966'
START_DATE = '2017-01-01'
END_DATE = '2017-01-31'

#%% GA Reporting API v3
'''
GA API v3는 OAuth 인증실패가 떨어져 현재로서는 사용할 수 없음.
(google2pandas 말고 다른 라이브러리를 사용해야 할 것으로 판단)
'''

conn = GoogleAnalyticsQuery(secrets='auth/google_service_secrets.json')

query = {
    'ids': VIEW_ID,
    'metrics': ['screenviews', 'uniqueScreenviews'],
    'dimensions': ['date', 'screenName'],
    'start_date': START_DATE,
    'end_date': END_DATE
}

df = conn.execute_query(query)

#%%
'''
GA API v4는 실행은 되나 결과값을 pandas DataFrame으로 만들 수 없음.
(현재 maintainer가 거기까지 신경 못쓴다고)
'''
conn = GoogleAnalyticsQueryV4(secrets='auth/google_service_secrets.json')

query = {
    'reportRequests': [{
        'viewId': VIEW_ID,
        'dateRanges': [{
            'startDate': START_DATE,
            'endDate': END_DATE,
        }],
        'dimensions': [
            { 'name': 'ga:date' },
            { 'name': 'ga:screenName' },
        ],
        'metrics': [
            { 'expression': 'ga:screenviews' },
            { 'expression': 'ga:uniqueScreenviews' },
        ]
    }]
}
result = conn.execute_query(query, as_dict=True) 
