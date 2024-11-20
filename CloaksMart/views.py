from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django_select2.forms import ModelSelect2MultipleWidget

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

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


import CloaksStats as getCloaksData
import CloaksDeals as getCloaksListings
import CloaksInventory as getCloaksInventory
#import getCloaksRanking
import CloaksCollage
import generic_collage
#import CloaksGifs

import re

import nest_asyncio

import asyncio
from typing import Optional
import random
import typing

from io import BytesIO
from PIL import Image
import functools
import logging

from itertools import cycle
from .models import FilteredListings, UserCloaks, Posts
from .forms import SortBy, Dashboard, CreatePost, CreateTrade, LoginForm
from asgiref.sync import sync_to_async

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from datetime import datetime, timedelta, timezone
import string
from django.utils.translation import gettext_lazy as _
import web3auth

def login_api(request):
    if request.method == 'GET':
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(32))
        request.session['login_token'] = token
        return JsonResponse({'data': token, 'success': True})
    else:
        token = request.session.get('login_token')
        if not token:
            return JsonResponse({'error': _(
                "No login token in session, please request token again by sending GET request to this url"),
                'success': False})
        else:
            form = LoginForm(token, request.POST)
            if form.is_valid():
                signature, address = form.cleaned_data.get("signature"), form.cleaned_data.get("address")
                del request.session['login_token']
                user = authenticate(request, token=token, address=address, signature=signature)
                if user:
                    login(request, user, 'web3auth.backend.Web3Backend')

                    return JsonResponse({'success': True})
                else:
                    error = _("Can't find a user for the provided signature with address {address}").format(
                        address=address)
                    user = form.save(commit=False)
                    addr_field = web3auth.app_settings.WEB3AUTH_USER_ADDRESS_FIELD
                    setattr(user, addr_field, form.cleaned_data[addr_field])
                    user.save()
                    login(request, user, 'web3auth.backend.Web3Backend')
                        

                    return JsonResponse({'success': False, 'error': error})
            else:
                return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})


def home(request):
    return render(request, 'home.html', {})

def codex(request):
    return render(request, 'codex.html', {})

async def my_profile(request, address=None):
    clans = []
    num_clans = []
    types = []
    num_types = []
    cloak_forms = []
    num_forms = []
    
    #df2 vars 
    form_strings = []
    all_forms = []
    
    type_strings = []
    all_types = []
    
    amulet_strings = []
    all_amulets = []
    
    acc_strings = []
    all_accs = []
    
    symbol_strings = []
    all_symbols = []
    
    df2_clans = []
    df2_members = [] 
    
    total_power = []
    total_magic = []
    total_agility = []
    
    images = []
    # if this is a POST request we need to process the form data
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        
         form_profile = Dashboard(request.POST)
         
         # check whether it's valid:
         if form_profile.is_valid():
             address = form_profile.cleaned_data["address"]
    else:
        form_profile =  Dashboard()
    
        
    df =  await run_blocking(getCloaksData.getCloaksByAddress,address=address)
    df2 =  await run_blocking(getCloaksInventory.getCloaksByAddress,address=address)
    
    print(df2)
    if(len(df2)>0):
        for i in range(len(df2)):
            df2_clans.append(df2.Name.iloc[i])
            df2_members.append(df2.Members.iloc[i])
            images.append(ast.literal_eval(df2.Image.iloc[i]))
            
            
            form_d = dict(Counter(ast.literal_eval(df2.iloc[i].Forms)).most_common())
            
            for k, v in form_d.items():
                form_strings.append(f'{k}: {v} \n')  
            
            all_forms.append(form_strings)
            form_strings = []
            
            
            type_d = dict(Counter(ast.literal_eval(df2.iloc[i].Types)).most_common())
            
            for k, v in type_d.items():
                type_strings.append(f'{k}: {v} \n')  
            
            all_types.append(type_strings)
            type_strings = []
            
            acc_d = dict(Counter(ast.literal_eval(df2.iloc[i].Accessories)).most_common())
            
            for k, v in acc_d.items():
                acc_strings.append(f'{k}: {v} \n')  
            
            all_accs.append(acc_strings)
            acc_strings = []
            
            amulet_d = dict(Counter(ast.literal_eval(df2.iloc[i].Amulets)).most_common())
            
            for k, v in amulet_d.items():
                amulet_strings.append(f'{k}: {v} \n')  
            
            all_amulets.append(amulet_strings)
            amulet_strings = []
            
            symbol_d = dict(Counter(ast.literal_eval(df2.iloc[i].Symbols)).most_common())
            
            for k, v in symbol_d.items():
                symbol_strings.append(f'{k}: {v} \n')  
            
            all_symbols.append(symbol_strings)
            symbol_strings = []
            
            power = sum(ast.literal_eval(df2.iloc[i].Power))
            magic = sum(ast.literal_eval(df2.iloc[i].Magic))
            agility = sum(ast.literal_eval(df2.iloc[i].Agility))
            
            total_power.append(power)
            total_magic.append(magic)
            total_agility.append(agility)
            
    if(len(df)>0):
        
        cloaks_list = ast.literal_eval(df.Tokens.iloc[0])
        
        img_dict = ast.literal_eval(df.Image.iloc[0])
        #img_dict = {k: v for k, v in sorted(img_dict.items(), key=lambda x: x[1], reverse=True)}
        clan_dict = ast.literal_eval(df.ClanDict.iloc[0])
        clan_dict = {k: v for k, v in sorted(clan_dict.items(), key=lambda x: x[1], reverse=True)}
        for k, v in clan_dict.items():
            clans.append(k)
            num_clans.append(v)
    
        type_dict = ast.literal_eval(df.TypeDict.iloc[0])
        type_dict = {k: v for k, v in sorted(type_dict.items(), key=lambda x: x[1], reverse=True)}
        for k, v in type_dict.items():
            types.append(k)
            num_types.append(v)
        
        
        form_dict = ast.literal_eval(df.FormDict.iloc[0])
        form_dict = {k: v for k, v in sorted(form_dict.items(), key=lambda x: x[1], reverse=True)}
        for k, v in form_dict.items():
            cloak_forms.append(k)
            num_forms.append(v)
        
        
    context =  {
    'form_profile': form_profile,
    'clans': clans,
    'num_clans': num_clans,
    'types': types, 
    'num_types': num_types,
    'cloak_forms': cloak_forms,
    'num_forms': num_forms,
    'df2': df2,
    'form_strings':form_strings,
    'all_forms': all_forms,
    'df2_clans': df2_clans,
    'df2_members': df2_members,
    'type_strings':type_strings,
    'all_types': all_types,
    'all_accs': all_accs,
    'all_amulets': all_amulets,
    'all_symbols': all_symbols,
    'total_power': total_power,
    'total_magic': total_magic,
    'total_agility': total_agility,
    'images': images
    }
    
   

    return render(request, 'profile.html', context)


async def collage_maker(request, address='0x50109fFA4e759038121A751C3d7c25020bd1Af19', sort_by=None, n_cols=0, n_rows=0):
    
    # if this is a POST request we need to process the form data
    
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        
         form_profile = Dashboard(request.POST)
         
         # check whether it's valid:
         if form_profile.is_valid():
             address = form_profile.cleaned_data["address"]
    else:
        form_profile =  Dashboard()
    
        
    df =  await run_blocking(CloaksCollage.getCloaksByAddress,address=address)
    src_dir = '/Users/jordan/solidity/Django/test_site/Cloaks/css/Images/'
    img_list = [src_dir + f'{df.Token[i]}.png' for i in range(len(df))]
    collage_loc = await run_blocking(generic_collage.create_collage, img_list)
    

    context =  {
    'collage_loc': collage_loc,
    'form_profile': form_profile
    }
    
    
    return render(request, 'collage_maker.html', context)




def index(request):
    print('hi')

'''    template = loader.get_template('/Users/jordan/solidity/Django/test_site/Cloaks/CloaksMart/templates/login.html')
    
    #print(context,template)
    return render(request, 'login.html', {})
    
'''

#function for running blocking functions as async
#use when processing pandas dataframes or API calls from import files

async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    
    loop = asyncio.get_running_loop()
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await loop.run_in_executor(None, func)

async def create_trade_request(request,
                               type_of_request='any',
                               preferred_traits=None,
                               additional_details=None,
                               tokens=None):
    
    address = '0x50109fFA4e759038121A751C3d7c25020bd1Af19'
    user_tokens = await run_blocking(CloaksCollage.getCloaksByAddressNoMeta,address=address)
    
    token_options = [(f'{user_tokens[i]}', f'{user_tokens[i]}') for i in range(len(user_tokens))]
    
    #if user selects to make a trade request
    if request.method == 'POST':
        form_trade_request = CreateTrade(request.POST, token_options=token_options)
        
        if form_trade_request.is_valid():
            
            tokens = form_trade_request.cleaned_data["tokens"]
            type_request = form_trade_request.cleaned_data["type_request"]
            additional_details = form_trade_request.cleaned_data["additional_details"] 
            
            if(form_trade_request['preferred_traits']):
                preferred_traits = form_trade_request.cleaned_data["preferred_traits"]
                
    else: form_trade_request = CreateTrade(token_options=token_options)
    
    #append new trade request to db
    
    
    context = {'form_trade_request': form_trade_request}     
    
    
    return render(request, 'CloaksList.html', context)
    
    
async def listings(request, sort_by='priceEth',
                   max_price=0.5,
                   accessory=None,
                   clan=None,
                   form=None,
                   type_cloak=None,
                   amulet=None,
                   animal_wrap=None,
                   archer_ears=None,
                   archer_hair=None,
                   arm_style=None,
                   beard=None,
                   chain=None,
                   chest=None,
                   cloak=None,
                   eyewear=None,
                   face_mask=None,
                   headband=None,
                   headgear=None,
                   mouth=None,
                   shoulder_gear=None,
                   smoke=None,
                   symbol=None,
                   warpaint=None,
                   sort_traits_by=False,
                   show=None,
                   special=None):
     
    @sync_to_async
    def clear_db():
        
        try:
            FilteredListings.objects.all().delete()
        except: pass
        
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form_django = SortBy(request.POST)
        
        # check whether it's valid:
        if form_django.is_valid():
            sort_by = form_django.cleaned_data["sort_by"]
            
            if(form_django["clan"]):
                clan = form_django.cleaned_data["clan"]
                
            if(form_django["accessory"]):
                accessory = form_django.cleaned_data["accessory"]
                
            if(form_django["amulet"]):
                amulet = form_django.cleaned_data["amulet"]
                
            if(form_django["animal_wrap"]):
                animal_wrap = form_django.cleaned_data["animal_wrap"]
                
            if(form_django["archer_ears"]):
                archer_ears = form_django.cleaned_data["archer_ears"]
                
            if(form_django["archer_hair"]):
                archer_hair = form_django.cleaned_data["archer_hair"]
            
            if(form_django["arm_style"]):
                arm_style = form_django.cleaned_data["arm_style"]
                
            if(form_django["beard"]):
                beard = form_django.cleaned_data["beard"]
                
            if(form_django["chain"]):
                chain = form_django.cleaned_data["chain"]
            
            if(form_django["chest"]):
                chest = form_django.cleaned_data["chest"]
            
            if(form_django["cloak"]):
                cloak = form_django.cleaned_data["cloak"]
            
            if(form_django["eyewear"]):
                eyewear = form_django.cleaned_data["eyewear"]
                
            if(form_django["face_mask"]):
                face_mask = form_django.cleaned_data["face_mask"]
            
            if(form_django["form"]):
                form = form_django.cleaned_data["form"]
                
            if(form_django["headband"]):
                headband = form_django.cleaned_data["headband"]
                
            if(form_django["headgear"]):
                headgear = form_django.cleaned_data["headgear"]
            
            if(form_django["mouth"]):
                mouth = form_django.cleaned_data["mouth"]
            
            if(form_django["shoulder_gear"]):
                shoulder_gear = form_django.cleaned_data["shoulder_gear"]
                
            if(form_django["smoke"]):
                smoke = form_django.cleaned_data["smoke"]
                
            if(form_django["symbol"]):
                symbol = form_django.cleaned_data["symbol"]
            
            if(form_django["type_cloak"]):
                type_cloak = form_django.cleaned_data["type_cloak"]
            
            if(form_django["warpaint"]):
                warpaint = form_django.cleaned_data["warpaint"]
          
            if(form_django["max_price"]):
                max_price = form_django.cleaned_data["max_price"]
                
            if(form_django["show"]):
                show = form_django.cleaned_data["show"]
            
            if(form_django["special"]):
                special = form_django.cleaned_data["special"]
                

    else:
        form_django = SortBy()
               
        
    df =  await run_blocking(getCloaksListings.getListings)
    
    df_by_price = await run_blocking(getCloaksListings.sort_df, df, sort_by='priceEth')
    
    fp = df_by_price.PriceEth.iloc[0]
    
    if(show == 'all'):
        df = await run_blocking(getCloaksListings.combine_listed_and_unlisted_items, df)
        print(show)
       
    df =  await run_blocking(getCloaksListings.sort_df, df, sort_by=sort_by, show=show, max_price=max_price,
                             accessory=accessory, clan=clan, form=form, type_cloak=type_cloak, amulet=amulet, 
                             animal_wrap=animal_wrap, archer_ears=archer_ears, archer_hair=archer_hair, arm_style=arm_style,
                             beard=beard,chain=chain, chest=chest, cloak=cloak, eyewear=eyewear, face_mask=face_mask, 
                             headband=headband, headgear=headgear, mouth=mouth, shoulder_gear=shoulder_gear, smoke=smoke,
                             symbol=symbol, warpaint=warpaint, special=special)
    #df = df.reset_index(drop=True)
    df.to_csv('/Users/jordan/solidity/Cloaks Bot/django_listings_df.csv', header=True)
    #print(df.Power)
    
    
    
    @sync_to_async
    def pd_2_db():
        
        try:
            FilteredListings.objects.all().delete()
        except: pass
        
        for index, row in df.iterrows():   
        #for i in range(len(df)):
            #print(index,row)
           
            obj = FilteredListings.objects.create(token_id=row['Token'],
                                 price_eth=row['PriceEth'],
                                 price_usd=row['PriceUsd'],
                                 marketplace=row['Marketplace'],
                                 marketplace_icon=row['MarketplaceIcon'],
                                 url=row['URL'],
                                 royalty=row['Royalty'],
                                 seller=row['Seller'],
                                 image=row['Image'],
                                 power=row['Power'],
                                 magic=row['Magic'],
                                 agility=row['Agility'],
                                 statsAvg=row['statsAvg'],
                                 collection_rank=row['CollectionRank'],
                                 percentile=row['Percentile'],
                                 accessory=row['Accessory'],
                                 clan=row['Clan'],
                                 form=row['Form'],
                                 type_cloak=row['Type'],
                                 amulet=row['Amulet'],
                                 animal_wrap=row['Animal Wrap'],
                                 archer_ears=row['Archer Ears'],
                                 archer_hair=row['Archer Hair'],
                                 arm_style=row['Arm Style'],
                                 beard=row['Beard'],
                                 chain=row['Chain'],
                                 chest=row['Chest'],
                                 cloak=row['Cloak'],
                                 eyewear=row['Eyewear'],
                                 face_mask=row['Face Mask'],
                                 headband=row['Headband'],
                                 headgear=row['Headgear'],
                                 mouth=row['Mouth'],
                                 shoulder_gear=row['Shoulder Gear'],
                                 smoke=row['Smoke'],
                                 symbol=row['Symbol'],
                                 warpaint=row['Warpaint'],
                                 num_traits = row['Num Traits'])
  
            
            obj.save()
          
        #global listings_db, template, context
        
        #listings_db = FilteredListings.objects.all().values()[:200]
        listings_db = FilteredListings.objects.all().values()[:500]
        #print(listings_db)
        template = loader.get_template('/Users/jordan/solidity/Django/test_site/Cloaks/CloaksMart/templates/CloaksMart.html')
        context =  {
        'listings_db': listings_db,
        'floor_price': fp,
        'form_django': form_django
        }
        
        #print(context,template)
        return template.render(context, request)
    
    await clear_db()
    res =  await pd_2_db()
    
    return HttpResponse(res)


#setting up web3 wallet connect with Moralis
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjZmOWU1OGUxLWY5NzEtNDM1Ny1hMGE2LWUyZjc4OTM3YzFjOCIsIm9yZ0lkIjoiNDA2OTAwIiwidXNlcklkIjoiNDE4MTEwIiwidHlwZUlkIjoiZWMyNTNmYzYtNzdhZS00YjdjLWJjNDYtMDExZDdhN2MxNjIzIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MjUzNjY2MjYsImV4cCI6NDg4MTEyNjYyNn0.CkyOfZgb269Fds_jYgIkcBXwc08wmuWNVka0HpxiaOY'




def forum_home(request, 
               title=None,
               text=None,
               files=None,
               category=None):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        post_form = CreatePost(request.POST)
        
        # check whether it's valid:
        if post_form.is_valid():
            title = post_form.cleaned_data["title"]
            text = post_form.cleaned_data["text"]
            category = post_form.cleaned_data["category"]
            
            if(post_form["files"]):
                files = post_form.cleaned_data["files"]
                
            present = datetime.now(timezone.utc)    
            obj = Posts.objects.create(title=title,
                                       content=text,
                                       created_at=present,
                                       created_by="shark",
                                       category=category)
            
            obj.save()
            
    else: post_form = CreatePost()
            
    posts_db = Posts.objects.all().values()
    
    
    context =  {
    'posts_db': posts_db,
    'post_form': post_form
    }
        
    return render(request, 'forum_home.html', context)

def forum_detail(request):
    return render(request, 'detail.html', {})

def forum_posts(request):
    return render(request, 'posts.html', {})

def request_message(request):
    data = json.loads(request.body)
    print(data)

    #setting request expiration time to 1 minute after the present->
    present = datetime.now(timezone.utc)
    present_plus_one_m = present + timedelta(minutes=1)
    expirationTime = str(present_plus_one_m.isoformat())
    expirationTime = str(expirationTime[:-6]) + 'Z'

    REQUEST_URL = 'https://authapi.moralis.io/challenge/request/evm'
    request_object = {
      "domain": "127.0.0.1:8000/",
      "chainId": 1,
      "address": data['address'],
      "statement": "Please confirm",
      "uri": "http://127.0.0.1:8000/",
      "expirationTime": expirationTime,
      "notBefore": "2020-01-01T00:00:00.000Z",
      "timeout": 15
    }
    x = requests.post(
        REQUEST_URL,
        json=request_object,
        headers={'X-API-KEY': API_KEY})

    return JsonResponse(json.loads(x.text))

def verify_message(request):
    data = json.loads(request.body)
    print(data)

    REQUEST_URL = 'https://authapi.moralis.io/challenge/verify/evm'
    x = requests.post(
        REQUEST_URL,
        json=data,
        headers={'X-API-KEY': API_KEY})
    print(json.loads(x.text))
    print(x.status_code)
    if x.status_code == 201:
        # user can authenticate
        eth_address=json.loads(x.text).get('address')
        print("eth address", eth_address)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            user = User(username=eth_address)
            user.is_staff = False
            user.is_superuser = False
            user.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['auth_info'] = data
                request.session['verified_data'] = json.loads(x.text)
                return JsonResponse({'user': user.username})
            else:
                return JsonResponse({'error': 'account disabled'})
    else:
        return JsonResponse(json.loads(x.text))
    