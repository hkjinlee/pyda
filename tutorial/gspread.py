# -*- coding: utf-8 -*-

'''
Google spreadsheet에서 문서를 읽어들이는 예제

문서주소: 
https://docs.google.com/spreadsheets/d/1KNIWwcT54p7mi3S0yLcEA9EUlgJPnRUWecy4EcrUANc/

사전 준비사항:
!pip install oauth2client
'''

#%% 모듈 import
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#%% OAuth 인증
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(
  'auth/google_service_secrets.json', scope)
client = gspread.authorize(creds)

#%% Google spreadsheet 읽어들이기
DOCUMENT_KEY = '1KNIWwcT54p7mi3S0yLcEA9EUlgJPnRUWecy4EcrUANc'
sheet = client.open_by_key(DOCUMENT_KEY).sheet1
values = sheet.get_all_values()

#%% sheet 조회
import pandas as pd

employees = pd.DataFrame(values[1:], columns=values[0:1][0])
