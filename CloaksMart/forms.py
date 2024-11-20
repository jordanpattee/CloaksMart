#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:30:51 2024

@author: jordan
"""

from django import forms
import django_select2.forms as s2forms
from itertools import combinations
from .models import FilteredListings

from collections import Counter
import pandas as pd
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from web3auth.settings import app_settings
from web3auth.utils import validate_eth_address
import string


class LoginForm(forms.Form):
    signature = forms.CharField(widget=forms.HiddenInput, max_length=132)
    address = forms.CharField(widget=forms.HiddenInput, max_length=42, validators=[validate_eth_address])

    def __init__(self, token, *args, **kwargs):
        self.token = token
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_signature(self):
        sig = self.cleaned_data['signature']
        if any([
            len(sig) != 132,
            sig[130:] != '1b' and sig[130:] != '1c',
            not all(c in string.hexdigits for c in sig[2:])
        ]):
            raise forms.ValidationError(_('Invalid signature'))
        return sig


# list(set()) here is to eliminate the possibility of double including the address field
signup_fields = list(set(app_settings.WEB3AUTH_USER_SIGNUP_FIELDS + [app_settings.WEB3AUTH_USER_ADDRESS_FIELD]))



class SortBy(forms.Form):
    sort_rarity_desc = False
    label_suffix=""
    df = pd.read_csv('/Users/jordan/solidity/Cloaks Bot/CloaksTraitTableWithImages.csv', keep_default_na=False)
    width = 175
    
    
    #sort_traits_by = forms.BooleanField(label='Alphabetical Sort:', required=False)
    
    ''' show '''
    show_options = [('buyNow', 'Buy Now'),
                       ('all', 'All')]
    show = forms.ChoiceField(widget=forms.Select(attrs={'style':f' margin-bottom: 1em; width: {width//1.5}px;', 'class':'px-0 mt-3'}),label="Show", label_suffix=label_suffix, choices = show_options)
    
    
    ''' sort by '''
    sort_by_options = [('priceEthLow2High', 'Price ETH (Low to High)'),
                       ('priceEthHigh2Low', 'Price ETH (High to Low)'),
                       ('averageStatsLow2High', 'Stats AVG (Low to High)'),
                       ('averageStatsHigh2Low', 'Stats AVG (High to Low)'),
                       ('numTraitsLow2High', '# Traits (Low to High)'),
                       ('numTraitsHigh2Low', '# Traits (High to Low)'),
                       ('power', 'Power'),
                       ('magic', 'Magic'),
                       ('agility', 'Agility')]
    sort_by = forms.ChoiceField(widget=forms.Select(attrs={'style':f' margin-bottom: 1em; width: {width//1.5}px;', 'class':'px-0 mt-3'}),label="Sort By", label_suffix=label_suffix, choices = sort_by_options)
    
    '''max price'''
    max_price = forms.FloatField(widget=forms.NumberInput(attrs={'step':'0.005','style':f'margin-bottom: 1em; width: {width//2}px;'}), initial=0.5, label='Max Price (ETH)', label_suffix=label_suffix, required=False)
    
    
    '''special'''
    special_options = [('None', 'None'),
                       ('No Cloak', 'No Cloak'),
                       ('All Swords and Potions', 'All Swords and Potions'),
                       ('All Sorceresses', 'All Sorceresses'),
                       ('All Wizards', 'All Wizards'),
                       ('All Headbands', 'All Headbands'),
                       ('Trigram Amulets', 'Trigram Amulets'),
                       ('All Symbols', 'All Symbols')]
    special = forms.ChoiceField(widget=forms.Select(attrs={'style':f' margin-bottom: 1em; width: {width//1.5}px;', 'class':'px-0 mt-3'}),label="Special", label_suffix=label_suffix,choices = special_options, required=False)
    
    
    '''traits'''
    #accesory
    accessories = {k: v for k, v in sorted(Counter(df.Accessory).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    accessory_traits = list(accessories.keys())
    accessory_options = []
    for trait in accessory_traits:
        num_cloaks_with_trait = accessories[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        accessory_options.append(option)
        
    accessory_options.extend([('All Swords', 'All Swords'),
                              ('All Potions', 'All Potions'),
                              ('All Swords and Potions', 'All Swords and Potions')])
    
    accessory = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Accessory", label_suffix=label_suffix, choices = accessory_options, required=False)
    
    #amulet
    amulet_options = (('Key of Secrets', 'Key of Secrets'),
                         ('Star of Saturn', 'Star of Saturn'),
                         ('X of Death', 'X of Death'),
                         ('Amulet Of Li', 'Amulet Of Li'),
                         ('Amulet Of Dui', 'Amulet Of Dui'),
                         ('Amulet Of Zhen', 'Amulet Of Zhen'),
                         ('Amulet Of Xun', 'Amulet Of Xun'),
                         ('Amulet Of Kan', 'Amulet Of Kan'),
                         ('Amulet Of Gen', 'Amulet Of Gen'),
                         ('Amulet Of Kuhn', 'Amulet Of Kuhn'),
                         ('Amulet Of Qian', 'Amulet Of Qian'))
    
    amulet = {k: v for k, v in sorted(Counter(df.Amulet).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    amulet_traits = list(amulet.keys())
    amulet_options = []
    for trait in amulet_traits:
        num_cloaks_with_trait = amulet[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        amulet_options.append(option)
        
    amulet = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Amulet", label_suffix=label_suffix, choices = amulet_options, required=False)
    
    
    
    #animal wrap
    animal_wrap_options = (('Python', 'Python'),
                         ('Mink', 'Mink'),
                         ('Fox', 'Fox'),
                         ('Viper', 'Viper'))
    
    animal_wrap = {k: v for k, v in sorted(Counter(df['Animal Wrap']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    animal_wrap_traits = list(animal_wrap.keys())
    animal_wrap_options = []
    for trait in animal_wrap_traits:
        num_cloaks_with_trait = animal_wrap[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        animal_wrap_options.append(option)
        
    animal_wrap = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Animal Wrap", label_suffix=label_suffix, choices = animal_wrap_options, required=False)
    
    #archer ears
    archer_ears_options = (('Crystal', 'Crystal'),
                            ('Earth', 'Earth'),
                            ('Fire', 'Fire'),
                            ('Sky', 'Sky'),
                            ('Steel', 'Steel'),
                            ('Water', 'Water'))
    
    archer_ears = {k: v for k, v in sorted(Counter(df['Archer Ears']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    archer_ears_traits = list(archer_ears.keys())
    archer_ears_options = []
    for trait in archer_ears_traits:
        num_cloaks_with_trait = archer_ears[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        archer_ears_options.append(option)
        
    archer_ears = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Archer Ears", label_suffix=label_suffix, choices = archer_ears_options, required=False)
    
    #archer hair
    archer_hair_options = (('Black', 'Black'),
                            ('Silver', 'Silver'),
                            ('Blue', 'Blue'),
                            ('Orange', 'Orange'),
                            ('Rose', 'Rose'),
                            ('Gold', 'Gold'))
    
    archer_hair = {k: v for k, v in sorted(Counter(df['Archer Hair']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    archer_hair_traits = list(archer_hair.keys())
    archer_hair_options = []
    for trait in archer_hair_traits:
        num_cloaks_with_trait = archer_hair[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        archer_hair_options.append(option)
        
    archer_hair = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Archer Hair", label_suffix=label_suffix, choices = archer_hair_options, required=False)
    
    #arm style
    arm_style_options = (('Warrior Tat', 'Warrior Tat'),
                            ('Metal Arm', 'Metal Arm'),
                            ('Sleeve Tat', 'Sleeve Tat'))
    
    arm_style = {k: v for k, v in sorted(Counter(df['Arm Style']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    arm_style_traits = list(arm_style.keys())
    arm_style_options = []
    for trait in arm_style_traits:
        num_cloaks_with_trait = arm_style[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        arm_style_options.append(option)
    
    arm_style = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Arm Style", label_suffix=label_suffix, choices = arm_style_options, required=False)
    
    #beard
    beard_options = (('White Beard', 'White Beard'),
                            ('Black Beard', 'Black Beard'))
    
    beard = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Beard", label_suffix=label_suffix, choices = beard_options, required=False)
    
    
    chain = {k: v for k, v in sorted(Counter(df['Chain']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    chain_traits = list(chain.keys())
    chain_options = []
    for trait in chain_traits:
        num_cloaks_with_trait = chain[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        chain_options.append(option)
        
    chain = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Chain", label_suffix=label_suffix, choices = chain_options, required=False)

    
    chest = {k: v for k, v in sorted(Counter(df['Chest']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    chest_traits = list(chest.keys())
    chest_options = []
    for trait in chest_traits:
        num_cloaks_with_trait = chest[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        chest_options.append(option)
        
    chest = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Chest", label_suffix=label_suffix, choices = chest_options, required=False)
    
    clans = {k: v for k, v in sorted(Counter(df.Clan).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    clan_traits = list(clans.keys())
    clan_options = []
    for trait in clan_traits:
        num_cloaks_with_trait = clans[trait]
        
        if(trait == 'None'): 
            trait = 'No Clan'
            
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        clan_options.append(option)
    
    
    #clan = forms.ChoiceField(widget=forms.Select(attrs={'style':'width: 100px;', 'class':'px-0 mt-3'}),initial='Optional',label="Clan", choices = clan_options, required=False)
    clan = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'width: {width}px;', 'class':'px-1 mt-3'}),label="Clan", label_suffix=label_suffix, choices = clan_options, required=False)
    
    
    cloak = {k: v for k, v in sorted(Counter(df['Cloak']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    cloak_traits = list(cloak.keys())
    cloak_options = []
    for trait in cloak_traits:
        num_cloaks_with_trait = cloak[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        cloak_options.append(option)
        
    cloak = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Cloak", label_suffix=label_suffix, choices = cloak_options, required=False)
    
    eyewear = {k: v for k, v in sorted(Counter(df['Eyewear']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    eyewear_traits = list(eyewear.keys())
    eyewear_options = []
    for trait in eyewear_traits:
        num_cloaks_with_trait = eyewear[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        eyewear_options.append(option)
        
    eyewear = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Eyewear", label_suffix=label_suffix, choices = eyewear_options, required=False)
    
    
    face_mask = {k: v for k, v in sorted(Counter(df['Face Mask']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    face_mask_traits = list(face_mask.keys())
    face_mask_options = []
    for trait in face_mask_traits:
        num_cloaks_with_trait = face_mask[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        face_mask_options.append(option)
        
    face_mask = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Face Mask", label_suffix=label_suffix, choices = face_mask_options, required=False)
    
    form = {k: v for k, v in sorted(Counter(df.Form).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    form_traits = list(form.keys())
    form_options = []
    for trait in form_traits:
        num_cloaks_with_trait = form[trait]
        
        if(trait == 'None'): 
            trait = 'No Form'
            
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        form_options.append(option)
    
    #form = forms.ChoiceField(widget=forms.Select(attrs={'style':'width: 100px;', 'class':'px-0  mt-3'}),initial='Optional', label='Form', choices=form_options, required=False)
    form = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-3 mt-3'}), label='Form', label_suffix=label_suffix, choices=form_options, required=False)
    
    
    headband = {k: v for k, v in sorted(Counter(df['Headband']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    headband_traits = list(headband.keys())
    headband_options = []
    for trait in headband_traits:
        num_cloaks_with_trait = headband[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        headband_options.append(option)
        
    headband = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Headband", label_suffix=label_suffix, choices = headband_options, required=False)
    
    
    headgear = {k: v for k, v in sorted(Counter(df['Headgear']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    headgear_traits = list(headgear.keys())
    headgear_options = []
    for trait in headgear_traits:
        num_cloaks_with_trait = headgear[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        headgear_options.append(option)
        
    headgear = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Headgear", label_suffix=label_suffix, choices = headgear_options, required=False)
    
    
    mouth = {k: v for k, v in sorted(Counter(df['Mouth']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    mouth_traits = list(mouth.keys())
    mouth_options = []
    for trait in mouth_traits:
        num_cloaks_with_trait = mouth[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        mouth_options.append(option)
        
    mouth = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Mouth", label_suffix=label_suffix, choices = mouth_options, required=False)
    
    
    shoulder_gear = {k: v for k, v in sorted(Counter(df['Shoulder Gear']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    shoulder_gear_traits = list(shoulder_gear.keys())
    shoulder_gear_options = []
    for trait in shoulder_gear_traits:
        num_cloaks_with_trait = shoulder_gear[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        shoulder_gear_options.append(option)
        
    shoulder_gear = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Shoulder Gear", label_suffix=label_suffix, choices = shoulder_gear_options, required=False)
    
    
    smoke = {k: v for k, v in sorted(Counter(df['Smoke']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    smoke_traits = list(smoke.keys())
    smoke_options = []
    for trait in smoke_traits:
        num_cloaks_with_trait = smoke[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        smoke_options.append(option)
        
    smoke = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Smoke", label_suffix=label_suffix, choices = smoke_options, required=False)
    
    symbol = {k: v for k, v in sorted(Counter(df['Symbol']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    symbol_traits = list(symbol.keys())
    symbol_options = []
    for trait in symbol_traits:
        num_cloaks_with_trait = symbol[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        symbol_options.append(option)
        
    symbol = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Symbol", label_suffix=label_suffix, choices = symbol_options, required=False)
    
    type_cloak = {k: v for k, v in sorted(Counter(df['Type']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    type_cloak_traits = list(type_cloak.keys())
    type_cloak_options = []
    for trait in type_cloak_traits:
        num_cloaks_with_trait = type_cloak[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        type_cloak_options.append(option)
        
    type_cloak = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-0 mt-3'}),label=mark_safe('Type\n'), label_suffix=label_suffix, choices=type_cloak_options, required=False)
    
    
    warpaint = {k: v for k, v in sorted(Counter(df['Warpaint']).items(), key=lambda x: x[1], reverse=sort_rarity_desc)}
    warpaint_traits = list(warpaint.keys())
    warpaint_options = []
    for trait in warpaint_traits:
        num_cloaks_with_trait = warpaint[trait]
        option = (trait, trait +  f' ({num_cloaks_with_trait})')
        warpaint_options.append(option)
        
    warpaint = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em; width: {width}px;', 'class':'px-2 mt-3'}), label="Warpaint", label_suffix=label_suffix, choices = warpaint_options, required=False)
    
    
  
class Dashboard(forms.Form):
    width = 550
    address = forms.CharField(widget=forms.TextInput(attrs={'style': f'width: {width}px;'}))
    
    
class CreatePost(forms.Form):
    width = 550
    title = forms.CharField(widget=forms.TextInput(attrs={'style': f'width: {width}px;'}), label="Title", required=True)
    text = forms.CharField(widget=forms.TextInput(attrs={'style': f'width: {width}px;'}), label="Text", required=True)
    files = forms.CharField(widget=forms.TextInput(attrs={'style': f'width: {width}px;'}), required=False)
    
    category_options = [('misc', 'Miscellaneous'),
                       ('buySellTrade', 'Buy/Sell/Trade')]
    category = forms.ChoiceField(widget=forms.Select(attrs={'style':f' margin-bottom: 1em; width: {width//1.5}px;', 'class':'px-0 mt-3'}),label="Category", choices = category_options, required=True)
    
class CreateTrade(forms.Form):
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('token_options', [])
        super().__init__(*args,**kwargs)
        self.fields['tokens'].choices = choices
    
    label_suffix=""
    
    tokens = forms.MultipleChoiceField(widget=s2forms.Select2MultipleWidget(attrs={'style':f'margin-bottom: 1em;', 'class':'px-2 mt-3'}), label="Tokens", label_suffix=label_suffix, choices = (), required=True)
    
    type_request_options = [('trade', 'Trade'),
                            ('trade_plus_eth', 'Trade + ETH'),
                            ('any', 'Any')]
    
    type_request = forms.ChoiceField(widget=forms.Select(attrs={'style':f' margin-bottom: 1em;', 'class':'px-0 mt-3'}),label="Trade Type", label_suffix=label_suffix, choices = type_request_options, required=True)
    
                                   
    preferred_traits = forms.CharField(widget=forms.TextInput(), required=False)
    additional_details = forms.CharField(widget=forms.TextInput(), required=True)
                                   
    
    

        
    