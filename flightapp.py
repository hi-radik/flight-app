from pyflightdata import FlightData
import json
import pandas as pd
import numpy as np
import time
import os.path
import csv
import datetime
import timedelta
import os
#############################

#############################
print('It is working!')
#Создание объекта и авторизация
f=FlightData()
f.login('login,'password')


#Получение сегодняшней даты
yesterday = datetime.datetime.now() - timedelta.Timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

#Список авиабаз НАТО из википедии + Армения
airforce_bases = ['LTAG', 'KLTS','PGUA','OAIX','KXMR','KVBG','KDYS','KDMA','KXTA',
'DNA','UTSL','BIKF','KUV','EGUL','KLFI','FRU','EGUN','KLSV','KOFF','RMS','KROW','BGTL',
'KSZL','EGVA','OASD','EDW','PAED','KADW','KVOK','KVD','YLV','UBBI','LIPA','RIV','SUU','WHP','TAY','TLL','EPU','KDL','URE ','RIX',
'VNT','LPX','VNO','KUN','SQQ','PLQ','GDN','SZZ','BZG','POZ','WMI','WAW','LCJ','LUZ','WRO','KTW','KRK','RZE','IEV','RWN',
'GML','VIN','ADB','ADA','TBS','KBP','PED','KBL', 'BSL', 'WOE', 'DHF' ,'NHD', 'EDF' ,'DOV' ,'SKF', 'BST', 'CCN', 'FAH', 'HEA',
           'KBL', 'KDH', 'MZR', 'TII', 'ZAJ', 'BTS', 'KSC', 'PZY', 'TAT', 'SLD', 'ILZ', 'LJU', 'MBX', 'ARW', 'BCM', 'BAY',
           'BRV', 'OTP', 'BBU', 'CLJ', 'CND', 'CRA', 'IAS', 'OMR', 'SUJ', 'SBZ', 'SCV', 'TGM', 'TSR', 'DYU', 'LBD', 'TJU',
           'KQT', 'CWC', 'DNK', 'DOK', 'IFO', 'HRK', 'KHE', 'KWG', 'KBP', 'GML', 'IEV', 'LWO', 'NLV', 'ODS', 'PLV', 'RWN',
           'SIP', 'UDJ', 'VIN', 'OZH', 'ZTR', 'ADA', 'ADF', 'AJI', 'ESB', 'HTY', 'AYT', 'BAL', 'BGG', 'BJV', 'YEI', 'CKZ',
           'DNZ', 'DLM', 'DIY', 'EDO', 'EZS', 'ERC', 'ERZ', 'AOE', 'GZT', 'GZP', 'IGD', 'ISE', 'IST', 'SAW', 'ISL', 'ADB',
           'KCO', 'KCM', 'KSY', 'KFS', 'ASR', 'KYA', 'KZR', 'MLX', 'MQM', 'MZH', 'MSR', 'NAV', 'OGU', 'SZF', 'GNY', 'SXZ',
           'NOP', 'NKT', 'VAS', 'TEQ', 'TJK', 'TZX', 'ECN', 'USQ', 'VAN', 'YKO', 'ONQ', 'ASB', 'TAZ', 'KEA', 'MYP', 'CRZ',
           'KRW', 'AGH', 'AJR', 'BLE', 'EKT', 'GEV', 'GVX', 'GOT', 'GSE', 'HFS', 'HAD', 'HMV', 'HLF', 'JKG', 'KLR', 'KSK',
           'KSD', 'KRN', 'KRF', 'KID', 'LDK', 'LPI', 'QEL', 'LLA', 'LYC', 'MMX', 'MXX', 'NRK', 'QEM', 'ORB', 'OER', 'OSD',
           'PJA', 'RNB', 'SCR', 'SFT', 'KVB', 'NYO', 'BMA', 'VST', 'ARN', 'SDL', 'EVG', 'TYF', 'THN', 'UME', 'VVK', 'VXO',
           'VHM', 'VBY', 'BRN', 'BXO', 'QYE', 'GVA', 'QYG', 'QYC', 'QYL', 'QYZ', 'LUG', 'QYQ', 'SIR', 'ACH', 'SMV', 'ZRH',
           'KAC', 'ALP', 'DAM', 'LTK', 'BXP', 'BZG', 'CZW', 'GDN', 'KTW', 'OSZ', 'KRK', 'LCJ', 'LUZ', 'QEI', 'SZY', 'POZ',
           'RDO', 'RZE', 'SZZ', 'QEB', 'WAW', 'WMI', 'WRO', 'IEG', 'LPX', 'RIX', 'VNT', 'ROB', 'ZIS', 'LAQ', 'BEN', 'GHT',
           'MRA', 'SEB', 'TOB', 'MJI', 'TIP', 'WAX', 'KUN', 'PLQ', 'SQQ', 'VNO', 'KDL', 'URE', 'EPU', 'TLL', 'TAY', 'BUD',
           'DEB', 'QEG', 'QGY', 'QEY', 'PEV', 'SOB', 'QEU', 'KFZ', 'TIA', 'AZR', 'ALG', 'AAE', 'BLJ', 'BJA', 'BSK', 'CFK',
           'CZL', 'DJG', 'ELU', 'GHA', 'HME', 'VVZ', 'GJL', 'LOO', 'ORN', 'OGX', 'QSF', 'TMR', 'TIN', 'TLM', 'QAD', 'TNM',
           'QAN', 'QAO', 'QAP', 'QAS', 'QAT', 'GRZ', 'HOH', 'INN', 'KLU', 'LNZ', 'SZG', 'VIE', 'QEW', 'GYD', 'FZL', 'KVD',
           'LLK', 'NAJ', 'GBB', 'BQT', 'GME', 'GNA', 'MSQ', 'MVQ', 'VTB', 'ANR', 'BRU', 'CRL', 'KJK', 'LGG', 'OST', 'CCA',
           'CIJ', 'CBB', 'GYA', 'LPB', 'ORU', 'RIB', 'RBQ', 'SRZ', 'VVI', 'SRE', 'TJA', 'TDD', 'UYU', 'BOJ', 'PDV', 'SOF', 'VAR']


#Создание DataFrame
data = pd.DataFrame(columns = ['today','code','text','afb','is_arrived','from_where_a',"a_time",
'is_departured','where_d',"d_time"])
on_ground_data = pd.DataFrame(columns = ['afb_gr','code','text','callsign', 'owner_code', 'owner_text', 'time'])

#Для каждой базы из списка достаем словари прибытий и убытий:
#Убытия
for i in airforce_bases:
    print('ok first')
    time.sleep(3)
    airbase_departures = f.get_airport_departures(i,page=1,limit=100,earlier_data=True)
    time.sleep(3)

    #Afb
    afb = i
    time.sleep(3)
    print('second ok')
    airbase_arrivals = f.get_airport_arrivals(i,page=1,limit=100,earlier_data=True)
    time.sleep(3)

    if airbase_departures == []:

        #Прибытия
        for ar in range(0,len(airbase_arrivals)):

            is_arrived = 1
            is_departured = 0

            if airbase_arrivals[ar]['flight']['aircraft'] != 'None' :

                #Достаем имя судна и код
                try:
                    model_text = airbase_arrivals[ar]['flight']['aircraft']['model']['text']
                except:
                    model_text = ''
                try:
                    model_code = airbase_arrivals[ar]['flight']['aircraft']['registration']
                except:
                    model_code = ''

                #Достаем ожидаемый таймстемп убытия
                try:
                    a_timestamp = airbase_arrivals[ar]['flight']['time']['estimated']['arrival']
                except:
                    a_timestamp == 'None'
                if a_timestamp == 'None':
                    a_timestamp = airbase_arrivals[ar]['flight']['time']['scheduled']['arrival']
                    if yesterday_str != datetime.datetime.fromtimestamp(a_timestamp).strftime('%Y-%m-%d'):
                        continue
                    a_time = pd.to_datetime(a_timestamp, unit='s')
                a_time = pd.to_datetime(a_timestamp, unit='s')
                d_time = 0
                where_d = 0
                #Откуда прибыл?
                if airbase_arrivals[ar]['flight']['airport']['origin']['code']['iata'] != 'None':
                    try:
                        from_where_a = airbase_arrivals[ar]['flight']['airport']['origin']['code']['iata']
                    except:
                        from_where_a = 0

                else:
                    from_where_a = 0

            #Запись в таблице
            data.loc[len(data)] = [yesterday_str, model_code, model_text, afb, is_arrived, from_where_a, a_time, is_departured, where_d, d_time]
            print('table ok')
    else:

        #Прибытия
        for ar in range(0,len(airbase_arrivals)):

            is_arrived = 1
            is_departured = 0

            if airbase_arrivals[ar]['flight']['aircraft'] != 'None' :

                #Достаем имя судна и код
                try:
                    model_text = airbase_arrivals[ar]['flight']['aircraft']['model']['text']
                except:
                    model_text = ''
                try:
                    model_code = airbase_arrivals[ar]['flight']['aircraft']['registration']
                except:
                    model_code = ''

                #Достаем ожидаемый таймстемп прибытия
                try:
                    a_timestamp = airbase_arrivals[ar]['flight']['time']['estimated']['arrival']
                except:
                    a_timestamp == 'None'
                if a_timestamp == 'None':
                    a_timestamp = airbase_arrivals[ar]['flight']['time']['scheduled']['arrival']
                    if yesterday_str != datetime.datetime.fromtimestamp(a_timestamp).strftime('%Y-%m-%d'):
                        continue
                    a_time = pd.to_datetime(a_timestamp, unit='s')
                a_time = pd.to_datetime(a_timestamp, unit='s')
                d_time = 0
                where_d = 0

                '''
                if airbase_arrivals[ar]['flight']['time']['estimated']['arrival'] != 'None':
                    a_timestamp = airbase_arrivals[ar]['flight']['time']['estimated']['arrival']
                    a_time = pd.to_datetime(a_timestamp, unit='s')
                else:
                    a_timestamp = airbase_arrivals[ar]['flight']['time']['scheduled']['arrival']


                '''

                #Откуда прибыли?
                try:
                    if airbase_arrivals[ar]['flight']['airport']['origin']['code']['iata'] != 'None':
                        try:
                            from_where_a = airbase_arrivals[ar]['flight']['airport']['origin']['code']['iata']
                        except:
                            from_where_a = 0

                    else:
                        from_where_a = 0
                except:
                    from_where_a = 0

            #Запись в таблице
            data.loc[len(data)] = [yesterday_str, model_code, model_text, afb, is_arrived, from_where_a, a_time, is_departured, where_d, d_time]
            print(afb)

    #Для каждого блока в словаре:
    for n in range(0, len(airbase_departures)):
        is_arrived = 0
        from_where_a = 0
        is_departured = 1
        a_time = 0

        #Достаем имя судна и код
        if airbase_departures[n]['flight']['aircraft'] != 'None':
            try:
                model_text = airbase_departures[n]['flight']['aircraft']['model']['text']
            except:
                model_text = ''
            try:
                model_code = airbase_departures[n]['flight']['aircraft']['registration']
            except:
                model_code =''

        #Куда летим?
        try:
            if airbase_departures[n]['flight']['airport']['destination']['code']['iata'] != 'None':
                where_d = airbase_departures[n]['flight']['airport']['destination']['code']['iata']
            else:
                where_d = 0
        except:
            where_d = 0


        #Достаем ожидаемый таймстемп убытия
        try:
            d_timestamp = airbase_departures[n]['flight']['time']['estimated']['departure']
        except:
            d_timestamp =='None'
        if d_timestamp == 'None':
            d_timestamp = airbase_departures[n]['flight']['time']['scheduled']['departure']
            if yesterday_str != datetime.datetime.fromtimestamp(d_timestamp).strftime('%Y-%m-%d'):
                continue
            d_time = pd.to_datetime(d_timestamp, unit='s')
        d_time = pd.to_datetime(d_timestamp, unit='s')

        #Запись в таблице
        data.loc[len(data)] = [yesterday_str, model_code, model_text, afb, is_arrived, from_where_a, a_time, is_departured, where_d, d_time]
        print(afb)
        print('tut toje ok')
os.chdir('/home/hiradik/new_flight_data')
data.to_csv(f'{yesterday_str}.csv', index=False)
