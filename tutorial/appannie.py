# -*- coding: utf-8 -*-

from lib.appannie import *

appannie = AppAnnie('auth/appannie_headers.json')

#%% packageName2ID 테스트
package_names = [
    'com.webzen.muorigin.google', 
    'com.itsgames.aden',
    'com.longtukorea.snmg' ]
result = appannie.packageName2ID(package_names)

#%% weeklyTopGames 테스트
result = appannie.topGames(granularity='weekly', date='2017-04-01')

#%% 게임 history 테스트
result = appannie.gameHistory('20600005637922', granularity='monthly',
                              start_date='2017-01-01', end_date='2017-03-31')

#%% 게임 feature history 테스트
result = appannie.gameFeaturedHistory('20600005637922', start_date='2017-02-01', end_date='2017-02-28')
