#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 15:01:38 2024

@author: jordan
"""

import requests
import pandas as pd
import numpy as np

import json
import time
import math
from collections import Counter
import ast
import re
import random
import os

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

def getStrings(df, i, attribute):
    strings = [] 
    
    if(attribute == 'Form'):
        for form in Counter(ast.literal_eval(df.iloc[i].Forms)).keys(): strings.append(f'> {form}: {str(Counter(ast.literal_eval(df.iloc[i].Forms))[form])} \n')
    
    elif(attribute == 'Type'):
        for types in Counter(ast.literal_eval(df.iloc[i].Types)).keys(): strings.append(f'> {types}: {str(Counter(ast.literal_eval(df.iloc[i].Types))[types])} \n')
   
    elif(attribute == 'Accessories'):
        for accessories in Counter(ast.literal_eval(df.iloc[i].Accessories)).keys(): strings.append(f'> {accessories}: {str(Counter(ast.literal_eval(df.iloc[i].Accessories))[accessories])} \n')
        if(len(strings) == 0): strings = ['None']
    
    elif(attribute == 'Symbols'):
        for symbols in Counter(ast.literal_eval(df.iloc[i].Symbols)).keys(): strings.append(f'> {symbols}: {str(Counter(ast.literal_eval(df.iloc[i].Symbols))[symbols])} \n')
        if(len(strings) == 0): strings = ['None']
        
    strings = ''.join(strings)
    return strings


def getImageByClan(df, img_count, i):
    img = ast.literal_eval(df.iloc[i]['Image'])[img_count]
    img_count = (img_count + 1) % len(ast.literal_eval(df.iloc[i]['Image']))
    
    return img, img_count


def getCloaksImage(cloaks_list):
    chosen_token = random.choice(cloaks_list)
    
    #get image from reservoir api
    API_KEY = os.getenv('RES_API_KEY')
    url = f'https://api.reservoir.tools/tokens/v7?tokens=0x0c56f29b8d90eea71d57cadeb3216b4ef7494abc%3A{chosen_token}'

    headers = {
        "accept": "*/*",
        "x-api-key": API_KEY
    }

    response = requests.get(url, headers=headers)
    df_temp = pd.read_json(response.text)
    
    url = df_temp.iloc[0]['tokens']['token']['image']
    img = re.split(r'[?]', url)[0]
    #print(img)
    
    return img

'''*** pull all tokens for an address ***'''
def getCloaksByAddress(address='0x50109fFA4e759038121A751C3d7c25020bd1Af19'):

    user_addr = address
    cursor = ''
    nextPage = ''
    cloaks_list = []
    #get image from reservoir api
    API_KEY = os.getenv('OS_API_KEY')
    for i in range(50):
        try:
            if(i == 0):
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts'
            else:
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts?&next={nextPage}'
            headers = {"accept": "application/json", 'X-API-KEY': API_KEY , 'next': '{0}'.format(cursor)}
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
    accessory_list = []
    symbol_list = []
    amulet_list = []
    
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
        
        accessory = str(df.Accessory.iloc[token])
        if(accessory == 'None'): accessory = 'No Accessory'
        accessory_list.append(accessory)
        
        symbol = str(df.Symbol.iloc[token])
        if(symbol == 'None'): symbol = 'No Symbol'
        symbol_list.append(symbol)
        
        amulet = str(df.Amulet.iloc[token])
        if(amulet == 'None'): amulet = 'No Amulet'
        amulet_list.append(amulet)
        
        stats_avg = round(sum([power, magic, agility])/3, 2)
        stats_avg_list.append(stats_avg)
        
        img = "/Images/" + str(token) + ".png"
        #img = 'https://ipfs.io/ipfs/' + re.split(r'[/]',img)[2]
        img_list.append(img) 
        
        
        
    if(len(cloaks_list)>0):
        #find the amount of each clan, form, and type held in wallet
        clan_dict = dict(Counter(clan_list))
        type_dict = dict(Counter(type_list))
        form_dict = dict(Counter(form_list))
        accessory_dict = dict(Counter(accessory_list))
        symbol_dict = dict(Counter(symbol_list))
        amulet_dict = dict(Counter(amulet_list))
        
        #calculate the sum of stats for the wallet
        total_power = sum(power_list)
        total_magic = sum(magic_list)
        total_agility = sum(agility_list)
        
        
        power_avg = int(total_power/len(cloaks_list))
        magic_avg = int(total_magic/len(cloaks_list))
        agility_avg = int(total_agility/len(cloaks_list))
        total_stats_avg = int(sum(stats_avg_list)/len(cloaks_list))
        
        df2 = pd.DataFrame({'NFTs': len(cloaks_list), 'Tokens': str(cloaks_list), 'ClanDict': str(clan_dict), 'TypeDict': str(type_dict), 'FormDict': str(form_dict),\
                            'AccessoryDict': str(accessory_dict), 'SymbolDict': str(symbol_dict), 'AmuletDict': str(amulet_dict),\
                            'TotalPower': total_power, 'TotalMagic': total_magic, 'TotalAgility': total_agility,\
                            'AveragePower': power_avg, 'AverageMagic': magic_avg, 'AverageAgility': agility_avg,\
                            'AverageStats': total_stats_avg, 'Image':random.choice(img_list) }, index = [0])
            
        df3 = pd.DataFrame({'Token': cloaks_list, 'Clan': clan_list, 'Type': type_list,\
                            'Form': form_list, 'Accessory': accessory_list, 'Symbol': symbol_list,\
                            'Amulet': amulet_list, 'Power': power_list, 'Magic': magic_list, 'Agility': agility_list,\
                            'Image':img_list})
        #return df2, df3
    
    
    
        #df2, df3 = getCloaksByAddress()
        
        clan_dicts = []
        clan_names = dict(Counter(df3.Clan).most_common())
        clan_names = list(clan_names.keys())
        
        
        for clan in clan_names:
            members = 0
            
            types = []
            forms = []
            accessories = []
            symbols = []
            amulets = []
            
            power = []
            magic = []
            agility = []
            
            images = []
            for i in range(len(df3)):
                if (df3.Clan.iloc[i] == clan):
                    # increase clan member count
                    members += 1
                    
                    #record values for clan dict and ignore none vals
                    types.append(df3.Type.iloc[i])
                    power.append(df3.Power.iloc[i])
                    magic.append(df3.Magic.iloc[i])
                    agility.append(df3.Agility.iloc[i])
                    images.append(df3.Image.iloc[i])
                    
                    
                    if(df3.Form.iloc[i] != 'No Form'):
                        forms.append(df3.Form.iloc[i])
                    
                    if(df3.Accessory.iloc[i] != 'No Accessory'):
                        accessories.append(df3.Accessory.iloc[i])
                    
                    if(df3.Symbol.iloc[i] != 'No Symbol'):
                        symbols.append(df3.Symbol.iloc[i])
                    
                    if(df3.Amulet.iloc[i] != 'No Amulet'):
                        amulets.append(df3.Amulet.iloc[i])
            
            #convert list of numpy int64 to python ints for using ast.literal_eval
            power = [int(x) for x in power]         
            magic = [int(x) for x in magic]   
            agility = [int(x) for x in agility]   
            
            temp_dict = {'Name': f'{clan}',\
                         'Members': f'{members}',\
                         'Types': f'{types}',\
                         'Forms': f'{forms}',\
                         'Accessories': f'{accessories}',\
                         'Symbols': f'{symbols}',\
                         'Amulets': f'{amulets}',\
                         'Power': f'{power}',\
                         'Magic': f'{magic}',\
                         'Agility': f'{agility}',\
                         'Image': f'{images}' }
                
            clan_dicts.append(temp_dict)
        df4 = pd.DataFrame(clan_dicts)
    else: df4 = []
    return df4

