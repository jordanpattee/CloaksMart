from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser
#from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
import requests
import pandas as pd
import numpy as np
import os
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider

import json
import time
import math
from collections import Counter
import ast


#import CloaksStats as getCloaksData
import CloaksDeals as getCloaksListings
#import CloaksInventory as getCloaksInventory
#import getCloaksRanking
#import CloaksCollage
#import CloaksGifs


import re
#from lxml import html
#from websocket import create_connection
#import discord
import os
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

class FilteredListings(models.Model):
    
    #token_id_range = np.arange(0,20000)
    token_id = models.IntegerField()
    
    price_eth = models.FloatField()
    price_usd = models.FloatField()
    
    mp_choices = [('os', 'OpenSea'), ('blur', 'Blur')]
    marketplace = models.CharField(max_length=200, choices=mp_choices)
    marketplace_icon = models.CharField(max_length=200)
    
    url = models.CharField(max_length=200)
    royalty =  models.CharField(max_length=200)
    seller = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    
    power = models.IntegerField()
    magic = models.IntegerField()
    agility = models.IntegerField()
    
    statsAvg = models.FloatField()
    collection_rank = models.IntegerField()
    percentile = models.FloatField()
    
    
    accessory = models.CharField(max_length=200)
    amulet = models.CharField(max_length=200)
    animal_wrap = models.CharField(max_length=200)
    archer_ears = models.CharField(max_length=200)
    archer_hair = models.CharField(max_length=200)
    arm_style = models.CharField(max_length=200)
    beard = models.CharField(max_length=200)
    clan = models.CharField(max_length=200)
    chain = models.CharField(max_length=200)
    chest = models.CharField(max_length=200)
    cloak = models.CharField(max_length=200)
    eyewear = models.CharField(max_length=200)
    face_mask = models.CharField(max_length=200)
    headband = models.CharField(max_length=200)
    headgear = models.CharField(max_length=200)
    mouth = models.CharField(max_length=200)
    shoulder_gear = models.CharField(max_length=200)
    smoke = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    warpaint = models.CharField(max_length=200)
   
    form = models.CharField(max_length=200)
    type_cloak = models.CharField(max_length=200)
    
    num_traits = models.CharField(max_length=200)
    
    
    def __str__(self):
        return '%s' % self.name

class UserCloaks(models.Model):
    address = models.CharField(max_length=200)
    
class Posts(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
   
class Holder(AbstractUser):
    username = models.CharField(max_length=42, unique=True)
