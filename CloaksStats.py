#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:37:03 2024

@author: jordan
"""

import requests
import pandas as pd
import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider
#from web3.middleware import construct_sign_and_send_raw_middleware
import json
import time
import math
from collections import Counter
import ast
import re
import random

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

def getCloaksImage(cloaks_list):
    chosen_token = random.choice(cloaks_list)
    
    user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]
    #get image from reservoir api
    API_KEY = os.getenv('RES_API_KEY')
    url = f'https://api.reservoir.tools/tokens/v7?tokens=0x0c56f29b8d90eea71d57cadeb3216b4ef7494abc%3A{chosen_token}'

    headers = {
        "accept": "*/*",
        "x-api-key": API_KEY,
        'User-Agent': random.choice(user_agents_list)
    }

    response = requests.get(url, headers=headers)
    df_temp = pd.read_json(response.text)
    
    url = df_temp.iloc[0]['tokens']['token']['image']
    img = re.split(r'[?]', url)[0]
    #print(img)
    
    return img

'''*** pull all tokens for an address ***'''
def getCloaksByAddress(address='0xa06E907671Abfaceb4851BE64BBeb3644C8661C0'):
#address = '0x50109fFA4e759038121A751C3d7c25020bd1Af19'
    user_addr = address
    cursor = ''
    nextPage = ''
    cloaks_list = []
    API_KEY = os.getenv('OS_API_KEY')
    for i in range(50):
        try:
            if(i == 0):
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts'
            else:
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts?&next={nextPage}'
            headers = {"accept": "application/json", 'X-API-KEY': API_KEY, 'next': '{0}'.format(cursor)}
            response = requests.get(url, headers=headers)
            df = pd.read_json(response.text)
            
            for i in range(len(df)):
                if(df.iloc[i][0]['collection'] == 'nakamigos-cloaks'):
                    #print(int(df.iloc[i][0]['identifier']))
                    cloaks_list.append(int(df.iloc[i][0]['identifier']))
    
        
            nextPage = df.next[0]
          
        except: break
    
    
    #pull up the meatadata file 
    df = pd.read_csv('CloaksTraitTableWithImages.csv', keep_default_na=False)
    
    
    clan_list = []
    type_list = []
    form_list = []
    power_list = []
    magic_list = []
    agility_list = []
    stats_avg_list  = []
    
    img_list = []
    
    for token in cloaks_list:
        clan = str(df.Clan.iloc[token])
        if(clan == 'None'): clan = 'No Clan'
        clan_list.append(clan)
        
        cloak_type = str(df.Type.iloc[token])
        type_list.append(cloak_type)
        
        form = str(df.Form.iloc[token])
        if(form == 'None'): form = 'No Form'
        form_list.append(form)
        
        power = df['Power/Strength'].iloc[token]
        power_list.append(power)
        
        magic = df['Wisdom/Magic'].iloc[token]
        magic_list.append(magic)
        
        agility = df['Speed/Agility'].iloc[token]
        agility_list.append(agility)
        
        stats_avg = round(sum([power, magic, agility])/3, 2)
        stats_avg_list.append(stats_avg)
        
        
        img = './css/Images/' + str(token) + '.png'
        img_list.append(img) 
        
        
        
    if(len(cloaks_list) > 0):
        #find the amount of each clan, form, and type held in wallet
        clan_dict = dict(Counter(clan_list))
        type_dict = dict(Counter(type_list))
        form_dict = dict(Counter(form_list))
        
        #calculate the sum of stats for the wallet
        total_power = sum(power_list)
        total_magic = sum(magic_list)
        total_agility = sum(agility_list)
        
        
        power_avg = int(total_power/len(cloaks_list))
        magic_avg = int(total_magic/len(cloaks_list))
        agility_avg = int(total_agility/len(cloaks_list))
        total_stats_avg = int(sum(stats_avg_list)/len(cloaks_list))
        
        df2 = pd.DataFrame({'NFTs': len(cloaks_list), 'Tokens': str(cloaks_list), 'ClanDict': str(clan_dict), 'TypeDict': str(type_dict), 'FormDict': str(form_dict),\
                            'TotalPower': total_power, 'TotalMagic': total_magic, 'TotalAgility': total_agility,\
                            'AveragePower': power_avg, 'AverageMagic': magic_avg, 'AverageAgility': agility_avg,\
                            'AverageStats': total_stats_avg, 'Image':str(img_list) }, index = [0])
    else: df2 = []
    print(df2)
        
    return df2
    
