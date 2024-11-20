#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:29:18 2024

@author: jordan
"""


import requests
import pandas as pd
import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider

import json
import time
import math
from collections import Counter
import ast
import re
import random


def sort_df(df, sort_by = str, max_price=None, accessory=None, clan=None, form=None, type_cloak=None, amulet=None):
    
    if(sort_by == 'priceEth'):
        df = df.sort_values(by='PriceEth')
        
    #elif(sort_by == 'priceUsd'):
    #    df = df.sort_values(by='PriceUsd') #highest to lowest 
        
    elif(sort_by== 'power'):
        df = df.sort_values(by='Power', ascending=False) #highest to lowest
        
    elif(sort_by == 'magic'):
        df = df.sort_values(by='Magic', ascending=False) #highest to lowest
        
    elif(sort_by == 'agility'):
        df = df.sort_values(by='Agility', ascending=False) #highest to lowest 
        
    elif(sort_by == 'averageStats'):
        df = df.sort_values(by='statsAvg', ascending=False) #highest to lowest
        
    else:
        df = df.sort_values(by='PriceEth')
        
    if(max_price != None):
        df = df[df.PriceEth <= max_price]
        
     
    if(accessory != None):
        if(accessory=='All Swords'):
            df = df[(df.Accessory == 'Sword of Earth') | (df.Accessory == 'Sword of the Sun') | (df.Accessory == 'Sword of the Moon') | (df.Accessory == 'Sword of Fire')]
        
        elif(accessory== 'All Potions'):
            df = df[(df.Accessory == 'Potion of Invisibility') | (df.Accessory == 'Potion of Telekinesis') | (df.Accessory == 'Potion of Summoning')]
        
        elif(accessory== 'All Swords and Potions'):
            df = df[(df.Accessory == 'Sword of Earth') | (df.Accessory == 'Sword of the Sun') | (df.Accessory == 'Sword of the Moon') | (df.Accessory == 'Sword of Fire') | (df.Accessory == 'Potion of Invisibility') | (df.Accessory == 'Potion of Telekinesis') | (df.Accessory == 'Potion of Summoning')]
        else:
            df = df[df.Accessory == accessory]
         
    if(clan != None):
         df = df[df.Clan == clan]
    
    if(form != None):
         df = df[df.Form == form]
    
    if(type_cloak != None):
         df = df[df.Type == type_cloak]
    
    if(amulet != None):
         df = df[df.Amulet == amulet]

    return df
     

def getListings():
    contract = '0x0c56f29B8D90eea71D57CAdEB3216b4Ef7494abC'
    API_KEY = 'b7908546-3720-5bf5-ab46-4688bffb078b'
    
    url = 'https://api.reservoir.tools/orders/asks/v5?contracts=0x0c56f29B8D90eea71D57CAdEB3216b4Ef7494abC&limit=1000'
    
    cursor = ''
    nextPage = ''
    tokens_list = []
    price_eth_list = []
    price_usd_list = []
    marketplace_list = []
    marketplace_icon_list = []
    url_list = []
    seller_list = []
    royalty_list = []
    
    for i in range(3):
        try:
            if(i == 0):
                url = f'https://api.reservoir.tools/orders/asks/v5?contracts={contract}&limit=1000'
            else:
                url = f'https://api.reservoir.tools/orders/asks/v5?contracts={contract}&limit=1000&continuation={nextPage}'
            headers = {
                "accept": "*/*",
                "x-api-key": API_KEY,
                'continuation': '{0}'.format(cursor)
                }
            response = requests.get(url, headers=headers)
            df_temp = pd.read_json(response.text)
            #print(df_temp)
            
            for i in range(len(df_temp)):
                price_eth = df_temp.orders.iloc[i]['price']['amount']['decimal']
                price_eth_list.append(round(price_eth,3))
                
                price_usd = df_temp.orders.iloc[i]['price']['amount']['usd']
                price_usd_list.append(round(price_usd,3))
                
                token = int(df_temp.orders.iloc[i]['criteria']['data']['token']['tokenId'])
                tokens_list.append(token)
                
                marketplace = df_temp.orders.iloc[i]['source']['name']
                marketplace_list.append(marketplace)
                
                marketplace_icon = df_temp.orders.iloc[i]['source']['icon']
                marketplace_icon_list.append(marketplace_icon)
                
                try:
                    if(marketplace == 'OpenSea'):
                        royalty = str(df_temp.orders.iloc[i]['feeBreakdown'][1]['bps'] / 100) + '%'
                        
                    elif(marketplace == 'Blur'):
                        royalty = str(df_temp.orders.iloc[i]['feeBreakdown'][0]['bps'] / 100) + '%'
                except:
                    royalty = 'No royalty info available'  
                    
                royalty_list.append(royalty)
                
                
                try:
                    url = df_temp.orders.iloc[i]['source']['url']
                except:
                    url = 'No URL available'
                url_list.append(url)    
               
                
               
                try:    
                    seller = df_temp.orders.iloc[i]['maker'] 
                except:
                    seller = 'No seller info available'
                seller_list.append(seller)              
                                        
                
            nextPage = df_temp.continuation.iloc[-1]
          
        except: break
    
    
    #pull up the meatadata file 
    df = pd.read_csv('/Users/jordan/solidity/Cloaks Bot/CloaksTraitTableWithImages.csv', keep_default_na=False)
    
    #modified df sorted by overall avg stats for adding to the listing
    overall_avg_df = pd.read_csv('/Users/jordan/solidity/Cloaks Bot/Data/CloaksTraitTableWithAVGStatsOverallRanking.csv', keep_default_na=False)                         
    
    
    clan_list = []
    type_list = []
    form_list = []
    power_list = []
    magic_list = []
    agility_list = []
    stats_avg_list  = []
    
    accessory_list = []
    amulet_list = []
    
    
    img_list = []
    
    collection_rank_list = []
    collection_percentile_list = []
    
    for token in tokens_list:
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
        
        accessory = df['Accessory'].iloc[token]
        accessory_list.append(accessory)
        
        amulet = df['Amulet'].iloc[token]
        amulet_list.append(amulet)
      
        stats_avg = round(sum([power, magic, agility])/3, 2)
        stats_avg_list.append(stats_avg)
        
        img = df.Image.iloc[token]
        img = 'https://ipfs.io/ipfs/' + re.split(r'[/]',img)[2]
        img_list.append(img) 
        
        collection_rank = overall_avg_df.OverallAvgRank[overall_avg_df.Token==token].iloc[0]
        collection_rank_list.append(collection_rank)
        
        collection_percentile = overall_avg_df.Percentile[overall_avg_df.Token==token].iloc[0]
        collection_percentile_list.append(collection_percentile)
        
    df2 = pd.DataFrame({'Token': tokens_list, 'PriceEth': price_eth_list, 'PriceUsd': price_usd_list,\
                        'Marketplace':marketplace_list, 'MarketplaceIcon':marketplace_icon_list, 'URL':url_list,\
                        'Royalty':royalty_list,'Seller':seller_list, 'Image':img_list,\
                        'Power': power_list, 'Magic': magic_list, 'Agility': agility_list, 'statsAvg':stats_avg_list,
                        'CollectionRank':collection_rank_list, 'Percentile': collection_percentile_list,\
                        'Accessory': accessory_list, 'Clan': clan_list, 'Form': form_list, 'Type': type_list, 'Amulet': amulet_list })


    unique_listings = []
    uniqueTokens = list(Counter(df2.Token).keys())
    for token in uniqueTokens:
        
        listing = df2[df2.Token == token].iloc[0]
        unique_listings.append(listing)
    df3 = pd.DataFrame(unique_listings)
    df3 = df3[(df3.Marketplace == 'OpenSea') | (df3.Marketplace == 'Blur')]
    print(df3)
    
    return df3
    
    
    
    