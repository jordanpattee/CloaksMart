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

def combine_listed_and_unlisted_items(df):
    #df2 = pd.read_csv('/Users/jordan/solidity/Cloaks Bot/Data/CloaksTraitTableWithAVGStatsOverallRanking.csv', keep_default_na=False)
    df2 = pd.read_csv('/Users/jordan/solidity/Cloaks Bot/Data/CloaksTraitTablewithRankingNumTraits.csv', keep_default_na=False)
    #rename cols to match listungs df
    df2 = df2.rename(columns={'OverallAvgRank': 'CollectionRank', 'Power/Strength': 'Power', 'Speed/Agility': 'Agility', 'Wisdom/Magic': 'Magic', 'AvgStats': 'statsAvg'})
    
    #make a var to track if item is listed or not
    df['Listed'] = 'True'
    df2['Listed'] = 'False'
    
    df2 = df2[~df2.Token.isin(df.Token)]
    
    df3 = pd.concat([df, df2], ignore_index=True, sort=False).fillna('1010')
    print(df3)
    
    return df3
    
def sort_df(df, sort_by = str, max_price=None, show=None, accessory=None, clan=None, form=None,
            type_cloak=None, amulet=None ,animal_wrap=None, archer_ears=None, archer_hair=None,
            arm_style=None, beard=None, chain=None, chest=None, cloak=None, eyewear=None, face_mask=None,
            headband=None, headgear=None, mouth=None, shoulder_gear=None, smoke=None,symbol=None,
            warpaint=None, special=None):
    
    
    #special
    if(special != None):
        if(special == 'No Cloak'):
            df = df[df.Cloak == 'None']
        elif(special == 'All Swords and Potions'):
            accessory = ['All Swords and Potions']
            
        elif(special == 'All Sorceresses'):
            cloak = ['Sorceress Cloak Blue', 'Sorceress Cloak Brown', 
      
                     'Sorceress Cloak Grey', 'Sorceress Cloak Olive']
            
        elif(special == 'All Wizards'):
            cloak = ['Wizard Blue', 'Wizard Brown', 
      
                     'Wizard Grey', 'Wizard Olive']
            
        elif(special == 'All Headbands'):
            headband = ['Blue', 'Yellow', 'Red', 'Orange', 'Purple']
        
        elif(special == 'Trigram Amulets'):
            amulet = ['Amulet Of Li', 'Amulet Of Dui',
                        'Amulet Of Zhen', 'Amulet Of Xun',
                        'Amulet Of Kan', 'Amulet Of Gen',
                        'Amulet Of Kuhn', 'Amulet Of Qian']
            
        elif(special == 'All Symbols'):
            symbol = ['Symbol Of Infinity', 'Symbol Of Totality',
                        'Symbol Of Balance', 'Symbol Of Defense',
                        'Symbol Of Bravery', 'Symbol Of Victory',
                        'Symbol Of Life']
            
    traits = {'Clan':clan, 'Form':form, 'Type':type_cloak, 'Amulet':amulet, 'Animal Wrap':animal_wrap,
              'Archer Ears':archer_ears, 'Archer Hair':archer_hair, 'Arm Style':arm_style, 'Beard': beard, 
              'Chain': chain, 'Chest':chest, 'Cloak':cloak, 'Eyewear':eyewear, 'Face Mask':face_mask, 
              'Headband':headband, 'Headgear':headgear, 'Mouth':mouth, 'Shoulder Gear':shoulder_gear,
              'Smoke':smoke, 'Symbol':symbol, 'Warpaint':warpaint}
    #accesory
    frames = []
    if(accessory != None):
        for acc in accessory:
            if(acc=='All Swords'):
                df_temp = df[(df.Accessory == 'Sword of Earth') | (df.Accessory == 'Sword of the Sun') | (df.Accessory == 'Sword of the Moon') | (df.Accessory == 'Sword of Fire')]
            
            elif(acc== 'All Potions'):
                df_temp = df[(df.Accessory == 'Potion of Invisibility') | (df.Accessory == 'Potion of Telekinesis') | (df.Accessory == 'Potion of Summoning')]
            
            elif(acc== 'All Swords and Potions'):
                df_temp = df[(df.Accessory == 'Sword of Earth') | (df.Accessory == 'Sword of the Sun') | (df.Accessory == 'Sword of the Moon') | (df.Accessory == 'Sword of Fire') | (df.Accessory == 'Potion of Invisibility') | (df.Accessory == 'Potion of Telekinesis') | (df.Accessory == 'Potion of Summoning')]

            else:
                df_temp = df[df.Accessory == acc]
            frames.append(df_temp)
            
    if(len(frames)>=1):
        df = pd.concat(frames,ignore_index=True)   
    
    
    for trait in traits:
        frames = []     
        if(traits[trait] != None):
            for i in range(len(traits[trait])):
                df_temp = df[df[trait] == traits[trait][i]]
                frames.append(df_temp)
                
        if(len(frames)>=1):
            df = pd.concat(frames,ignore_index=True) 
    
    if((max_price != None ) and (show != 'all')):
        df = df[df.PriceEth <= max_price]
        
    #sort final df by price, stats, etc.,        
    if(sort_by == 'priceEthLow2High'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by='PriceEth', ascending=True) #lowest to highest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by='PriceEth', ascending=True) #lowest to highest
        
    
    elif(sort_by == 'priceEthHigh2Low'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by='PriceEth', ascending=False) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by='PriceEth', ascending=False) #highest to lowest
        #df = df.sort_values(by='PriceEth', ascending=False) #highest to lowest
    
    elif(sort_by== 'numTraitsLow2High'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['Num Traits', 'PriceEth'], ascending=[True,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by=['Num Traits', 'PriceEth'], ascending=[True,True]) #highest to lowest
        #df = df.sort_values(by='Num Traits', ascending=True) #lowest to highest
        
        
    elif(sort_by== 'numTraitsHigh2Low'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['Num Traits', 'PriceEth'], ascending=[False,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False'].sort_values(by=['Num Traits'], ascending=[False])
            df = pd.concat([df1,df2],ignore_index=True)
        
        else:
            df = df.sort_values(by='Num Traits', ascending=False) #highest to lowest
       #df = df.sort_values(by='Num Traits', ascending=False) #highest to lowest
        
    elif(sort_by== 'power'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['Power', 'PriceEth'], ascending=[False,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by=['Power', 'PriceEth'], ascending=[False,True]) #highest to lowest
        #df = df.sort_values(by='Power', ascending=False) #highest to lowest
        
    elif(sort_by == 'magic'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['Magic', 'PriceEth'], ascending=[False,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by=['Magic', 'PriceEth'], ascending=[False,True]) #highest to lowest
        #df = df.sort_values(by='Magic', ascending=False) #highest to lowest
        
    elif(sort_by == 'agility'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['Agility', 'PriceEth'], ascending=[False,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by=['Agility', 'PriceEth'], ascending=[False,True]) #highest to lowest
        #df = df.sort_values(by='Agility', ascending=False) #highest to lowest 
        
    elif(sort_by == 'averageStatsLow2High'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['statsAvg', 'PriceEth'], ascending=[True,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by=['statsAvg', 'PriceEth'], ascending=[True,True]) #highest to lowest
        #df = df.sort_values(by='statsAvg', ascending=True) #lowest to highest
        
    elif(sort_by == 'averageStatsHigh2Low'):
        if(show == 'all' ):
            df1 = df[df['Listed'] == 'True'].sort_values(by=['statsAvg', 'PriceEth'], ascending=[False,True]) #highest to lowest
            df2 = df[df['Listed'] == 'False']
            df = pd.concat([df1,df2],ignore_index=True)
        else:
            df = df.sort_values(by=['statsAvg', 'PriceEth'], ascending=[False,True]) #highest to lowest
        #df = df.sort_values(by='statsAvg', ascending=False) #highest to lowest
        
    else:
        df = df.sort_values(by='PriceEth')
        
    print(df)

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
    animal_wrap_list = []
    archer_ears_list = []
    archer_hair_list = []
    arm_style_list = []
    beard_list = []
    chain_list = []
    chest_list = []
    cloak_list = []
    eyewear_list = []
    face_mask_list = []
    headband_list = []
    headgear_list = []
    mouth_list = []
    shoulder_gear_list = []
    smoke_list = []
    symbol_list = []
    warpaint_list = []
    
    img_list = []
    
    collection_rank_list = []
    collection_percentile_list = []
    
    num_traits_list = []
    
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
        
        animal_wrap = df['Animal Wrap'].iloc[token]
        animal_wrap_list.append(animal_wrap)
        
        archer_ears = df['Archer Ears'].iloc[token]
        archer_ears_list.append(archer_ears)
        
        archer_hair = df['Archer Hair'].iloc[token]
        archer_hair_list.append(archer_hair)
        
        arm_style = df['Arm Style'].iloc[token]
        arm_style_list.append(arm_style)
      
        beard = df['Beard'].iloc[token]
        beard_list.append(beard)
        
        chain = df['Chain'].iloc[token]
        chain_list.append(chain)
        
        chest = df['Chest'].iloc[token]
        chest_list.append(chest)
        
        cloak = df['Cloak'].iloc[token]
        cloak_list.append(cloak)
      
        eyewear = df['Eyewear'].iloc[token]
        eyewear_list.append(eyewear)
        
        face_mask = df['Face Mask'].iloc[token]
        face_mask_list.append(face_mask)
        
        headband = df['Headband'].iloc[token]
        headband_list.append(headband)
        
        headgear = df['Headgear'].iloc[token]
        headgear_list.append(headgear)
        
        mouth = df['Mouth'].iloc[token]
        mouth_list.append(mouth)
        
        shoulder_gear = df['Shoulder Gear'].iloc[token]
        shoulder_gear_list.append(shoulder_gear)
        
        smoke = df['Smoke'].iloc[token]
        smoke_list.append(smoke)
        
        symbol = df['Symbol'].iloc[token]
        symbol_list.append(symbol)
        
        warpaint = df['Warpaint'].iloc[token]
        warpaint_list.append(warpaint)
        
        
        stats_avg = round(sum([power, magic, agility])/3, 2)
        stats_avg_list.append(stats_avg)
        
        img = df.Image.iloc[token]
        img = 'https://ipfs.io/ipfs/' + re.split(r'[/]',img)[2]
        img_list.append(img) 
        
        collection_rank = overall_avg_df.OverallAvgRank[overall_avg_df.Token==token].iloc[0]
        collection_rank_list.append(collection_rank)
        
        collection_percentile = overall_avg_df.Percentile[overall_avg_df.Token==token].iloc[0]
        collection_percentile_list.append(collection_percentile)
    
    
        
        cols = df.columns
        cols = cols.drop(['Token Id', 'Image', 'Speed/Agility', 'Wisdom/Magic', 'Power/Strength'])
        num_traits = 0
        for col in cols:
            if((df[col].iloc[token] != 'No Clan') and (df[col].iloc[token] != 'No Form') and (df[col].iloc[token] != 'None')):
                num_traits += 1
            
        num_traits_list.append(num_traits)
            
        
    
    df2 = pd.DataFrame({'Token': tokens_list, 'PriceEth': price_eth_list, 'PriceUsd': price_usd_list,\
                        'Marketplace':marketplace_list, 'MarketplaceIcon':marketplace_icon_list, 'URL':url_list,\
                        'Royalty':royalty_list,'Seller':seller_list, 'Image':img_list,\
                        'Power': power_list, 'Magic': magic_list, 'Agility': agility_list, 'statsAvg':stats_avg_list,
                        'CollectionRank':collection_rank_list, 'Percentile': collection_percentile_list,\
                        'Accessory': accessory_list, 'Clan': clan_list, 'Form': form_list, 'Type': type_list, 'Amulet': amulet_list,\
                        'Animal Wrap': animal_wrap_list, 'Archer Ears': archer_ears_list, 'Archer Hair': archer_hair_list,\
                        'Arm Style': arm_style_list, 'Beard': beard_list, 'Chain': chain_list, 'Chest': chest_list, 'Cloak': cloak_list,\
                        'Eyewear': eyewear_list, 'Face Mask': face_mask_list, 'Headband': headband_list, 'Headgear': headgear_list,\
                        'Mouth': mouth_list, 'Shoulder Gear': shoulder_gear_list, 'Smoke': smoke_list, 'Symbol': symbol_list, 'Warpaint': warpaint_list,
                        'Num Traits': num_traits_list})


    unique_listings = []
    uniqueTokens = list(Counter(df2.Token).keys())
    for token in uniqueTokens:
        
        listing = df2[df2.Token == token].iloc[0]
        unique_listings.append(listing)
    df3 = pd.DataFrame(unique_listings)
    df3 = df3[(df3.Marketplace == 'OpenSea') | (df3.Marketplace == 'Blur')]
    
    return df3
    
    
    
    