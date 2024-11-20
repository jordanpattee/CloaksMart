#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 14:32:05 2024

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


def create_collage(listofimages : List[str], save_fn: str = '', n_cols : int = 0, n_rows: int = 0, 
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
    
    all_thumbnails : List[Image.Image] = []
   
    for i in range(len(listofimages)):
            thumbnail = Image.open(listofimages[i])
             
            if thumbnail_width * thumbnail_scale < thumbnail.width:
                thumbnail_width = round(thumbnail_width * thumbnail_scale)
            if thumbnail_height * thumbnail_scale < thumbnail.height:
                thumbnail_height = round(thumbnail_height * thumbnail_scale)
            
            print(thumbnail.width, thumbnail.height)
            thumbnail.thumbnail((thumbnail_width, thumbnail_height))
            all_thumbnails.append(thumbnail)
        
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
    save_path = '/Users/jordan/solidity/Django/test_site/Cloaks/css/collages/collage.png'
    #save_path = f'collage_{save_fn}'.join(re.split(r"collage", save_path))
    new_im.save(save_path)
    return save_path