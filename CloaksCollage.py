#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 06:56:41 2024

@author: jordan
"""

import os
from typing import List, Tuple

from PIL import Image
from io import BytesIO

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


def find_multiples(number : int):
    multiples = set()
    for i in range(number - 1, 1, -1):
        mod = number % i
        if mod == 0:
            tup = (i, int(number / i))
            if tup not in multiples and (tup[1], tup[0]) not in multiples:
                multiples.add(tup)
                
    if len(multiples) == 0:
        mod == number % 2
        div = number // 2
        multiples.add((2, div + mod))
        
    return list(multiples)

def get_smallest_multiples(number : int, smallest_first = True) -> Tuple[int, int]:
    multiples = find_multiples(number)
    smallest_sum = number
    index = 0
    for i, m in enumerate(multiples):
        sum = m[0] + m[1]
        if sum < smallest_sum:
            smallest_sum = sum
            index = i
            
    result = list(multiples[i])
    if smallest_first:
        result.sort()
        
    return result[0], result[1]
    

def create_collage(listofimages : List[str],listofIpfs : List[str], listof4everland : List[str],
                   address: str = '', n_cols : int = 0, n_rows: int = 0, 
                   thumbnail_scale : float = 1.0, thumbnail_width : int = 1000, thumbnail_height : int = 1000):
 
    if(n_cols == 0):
        n_cols = int(math.sqrt(len(listofimages)))
            
        if(len(listofimages) % (n_cols**2) == 0):
            n_rows = n_cols
        elif(len(listofimages) % (n_cols**2) >= n_cols):
            n_rows = n_cols+1
        else:
            n_rows = n_cols
    
    #thumbnail_width = 0 if thumbnail_width == 0 or n_cols == 0 else round(thumbnail_width / n_cols)
    #thumbnail_height = 0 if thumbnail_height == 0 or n_rows == 0 else round(thumbnail_height/n_rows)
    timeout = 5
    
    user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]
    
    all_thumbnails : List[Image.Image] = []
    for i in range(len(listofimages)):
        try:
            response = requests.get(listofimages[i], timeout=timeout, headers={'User-Agent': random.choice(user_agents_list)})
        except:
            try:
                response = requests.get( listofIpfs[i], timeout=timeout, headers={'User-Agent': random.choice(user_agents_list)})
            except:
                try:
                    response = requests.get( listof4everland[i], timeout=timeout, headers={'User-Agent': random.choice(user_agents_list)})
                except: continue
        
        try:
            print(response.status_code)        
            img = Image.open(BytesIO(response.content))
            thumbnail = img
                
            ''' 
            if thumbnail_width * thumbnail_scale < thumbnail.width:
                thumbnail_width = round(thumbnail.width * thumbnail_scale)
            if thumbnail_height * thumbnail_scale < thumbnail.height:
                thumbnail_height = round(thumbnail.height * thumbnail_scale)
            '''
            #print(thumbnail_width, thumbnail_height)
            thumbnail.thumbnail((thumbnail_width, thumbnail_height))
            all_thumbnails.append(thumbnail)
            
        except:continue
        
    new_im = Image.new('RGB', (thumbnail_width * n_cols, thumbnail_height * n_rows), 'white')
    
    i, x, y = 0, 0, 0
    for row in range(n_rows):
        for col in range(n_cols):
            if i > len(all_thumbnails) - 1:
                continue
            
            print(i, x, y)
            new_im.paste(all_thumbnails[i], (x, y))
            i += 1
            x += thumbnail_width
            #y += thumbnail_height
        #x += thumbnail_width
        y += thumbnail_height
        x = 0

    extension = os.path.splitext(listofimages[0])[1]
    if extension == "":
        extension = ".png"
    #destination_file = os.path.join(os.path.dirname(listofimages[0]), f"Collage{extension}")
    save_path = '/Users/jordan/solidity/Cloaks Bot/Images/test_collage.png'
    save_path = f'collage_{address}'.join(re.split(r"collage", save_path))
    new_im.save(save_path)
    return save_path
   
def getCloaksImage(cloaks_list):
    chosen_token = random.choice(cloaks_list)
    
    timeout = 10
    #get image from reservoir api
    API_KEY = 'b7908546-3720-5bf5-ab46-4688bffb078b'
    url = f'https://api.reservoir.tools/tokens/v7?tokens=0x0c56f29b8d90eea71d57cadeb3216b4ef7494abc%3A{chosen_token}'

    headers = {
        "accept": "*/*",
        "x-api-key": API_KEY
    }

    response = requests.get(url, headers=headers, timeout=timeout)
    
    df_temp = pd.read_json(response.text)
    
    url = df_temp.iloc[0]['tokens']['token']['image']
    img = re.split(r'[?]', url)[0]
    img = 'https://'.join(re.split(r"\bhttps:/\b", img))
    #print(img)
    
    return img

def getCloaksByAddressNoMeta(address='0x50109fFA4e759038121A751C3d7c25020bd1Af19'):
    #address = '0x50109fFA4e759038121A751C3d7c25020bd1Af19'
    user_addr = address
    cursor = ''
    nextPage = ''
    cloaks_list = []
    for i in range(50):
        try:
            if(i == 0):
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts'
            else:
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts?&next={nextPage}'
            headers = {"accept": "application/json", 'X-API-KEY': '5afe6fdc2875416bbc7f419a7faec02c', 'next': '{0}'.format(cursor)}
            response = requests.get(url, headers=headers)
            df = pd.read_json(response.text)
            
            for i in range(len(df)):
                if(df.iloc[i][0]['collection'] == 'nakamigos-cloaks'):
                    #print(int(df.iloc[i][0]['identifier']))
                    cloaks_list.append(int(df.iloc[i][0]['identifier']))
    
        
            nextPage = df.next[0]
          
        except: break
    return cloaks_list
    
def getCloaksByAddress(address='0x50109fFA4e759038121A751C3d7c25020bd1Af19'):
    #address = '0x50109fFA4e759038121A751C3d7c25020bd1Af19'
    user_addr = address
    cursor = ''
    nextPage = ''
    cloaks_list = []
    for i in range(50):
        try:
            if(i == 0):
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts'
            else:
                url = f'https://api.opensea.io/api/v2/chain/ethereum/account/{user_addr}/nfts?&next={nextPage}'
            headers = {"accept": "application/json", 'X-API-KEY': '5afe6fdc2875416bbc7f419a7faec02c', 'next': '{0}'.format(cursor)}
            response = requests.get(url, headers=headers)
            df = pd.read_json(response.text)
            
            for i in range(len(df)):
                if(df.iloc[i][0]['collection'] == 'nakamigos-cloaks'):
                    #print(int(df.iloc[i][0]['identifier']))
                    cloaks_list.append(int(df.iloc[i][0]['identifier']))
    
        
            nextPage = df.next[0]
          
        except: break
    
    
    #pull up the meatadata file 
    df = pd.read_csv('/Users/jordan/solidity/Cloaks Bot/CloaksTraitTableWithImages.csv', keep_default_na=False)
    
    
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
    ipfs_list = []
    everland_list = []
    
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
        
        img = getCloaksImage([token])
        ipfs = df.Image.iloc[token]
        ipfs_img = 'https://ipfs.io/ipfs/' + re.split(r'[/]',ipfs)[2]
        everland_img = 'https://4everland.io/ipfs/' + re.split(r'[/]',ipfs)[2]
        
        img_list.append(img) 
        ipfs_list.append(ipfs_img)
        everland_list.append(everland_img)
    
    df2 = pd.DataFrame({'Token': cloaks_list, 'Clan': clan_list, 'Type': type_list,\
                        'Form': form_list, 'Accessory': accessory_list, 'Symbol': symbol_list,\
                        'Amulet': amulet_list, 'Power': power_list, 'Magic': magic_list, 'Agility': agility_list,\
                        'Image':img_list, 'IpfsImage': ipfs_list, 'EverlandImage': everland_list})
        
    df2 = df2.sort_values(by='Clan', ascending=False)
    df2 = df2.reset_index(drop=True)
    return df2
'''        
def getCloaksCollage(df):
    df = df.sort_values(by='Clan', ascending=False)
    
'''    
    
    