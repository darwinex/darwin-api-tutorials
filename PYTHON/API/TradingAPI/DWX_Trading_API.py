# -*- coding: utf-8 -*-
"""
    DWX_Trading_API.py - DARWIN Trading API (Subclass of DWX_API)
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: July 29, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import os
os.chdir('<INSERT-PATH-TO-PROJECT-DIR-HERE>')

from API.dwx_api import DWX_API

class DWX_Trading_API(DWX_API):
    
    def __init__(self,
                 _api_url='https://api.darwinex.com',
                 _api_name='trading',
                 _version=1.0,
                 _demo=True):
        
        super(DWX_Trading_API, self).__init__(_api_url,_api_name,_version,_demo)
        
        if _demo:
            print(f'--+--+--\n[KERNEL] DARWIN Trading API v{_version} initialized in DEMO environment\n--+--+--')
        else:
            print(f'--+--+--\n[KERNEL] DARWIN Trading API v{_version} initialized in REAL environment\n--+--+--')
        
    #########################################################################
    
    def _Get_Permitted_Operations_(self):
        
        try:
            return self._Call_API_(_endpoint='/productmarket/status',
                                   _type='GET', _data='')
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Get_Account_Leverage_(self, _id=0):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/leverage',
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            
    #########################################################################
    
    # DUMMY ORDER GENERATORS BELOW -- DO NOT USE IN LIVE TRADING PLEASE!
    
    def _generate_dummy_buy_order_(self):
        
        return '{\
          "amount": 200.00,\
          "productName": "NTI.4.12",\
          "thresholdParameters": {\
            "quoteStopLoss": 100.00,\
            "quoteTakeProfit": 1000.00\
          }\
        }'
    
    def _generate_dummy_sell_order_(self):
        
        return '{\
          "amount": 200.00,\
          "productName": "NTI.4.12"\
        }'
        
    def _generate_dummy_buylimit_order_(self):
        
        return '{\
          "amount": 200.00,\
          "productName": "NTI.4.12",\
          "quote": 200.00,\
          "side": "BUY",\
          "type": "LESS_THAN_EQUAL",\
          "thresholdParameters": {\
            "quoteStopLoss": 100.00,\
            "quoteTakeProfit": 1000.00\
          }\
        }'
    
    def _generate_dummy_buystop_order_(self):
        
        return '{\
          "amount": 200.00,\
          "productName": "NTI.4.12",\
          "quote": 500.00,\
          "side": "BUY",\
          "type": "GREATER_THAN_EQUAL",\
          "thresholdParameters": {\
            "quoteStopLoss": 100.00,\
            "quoteTakeProfit": 1000.00\
          }\
        }'
    
    def _generate_dummy_conditional_update_order_(self):
        
        return '{\
          "amount": 200.00,\
          "quote": 150.00,\
          "thresholdParameters": {\
            "quoteStopLoss": 100.00,\
            "quoteTakeProfit": 999.99\
          }\
        }'
    
    # DUMMY ORDER GENERATORS ABOVE -- DO NOT USE IN LIVE TRADING PLEASE!
    
    #########################################################################
    
    def _Raise_Conditional_Order_(self, 
                                  _id=0, # Investor Account ID
                                  _order=None):
        
        # Construct Buy Order dict if arg _order = None
        if _order is None:
            _order = self._generate_dummy_buylimit_order_() # or buystop
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/conditionalorders',
                                   _type = 'POST',
                                   _data = _order)
            
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Update_Conditional_Order_(self, 
                                  _id=0, # Investor Account ID
                                  _oid=0, # Conditional Order ID
                                  _order=None):
        
        # Construct Conditional Order dict if arg _order = None
        if _order is None:
            _order = self._generate_dummy_conditional_update_order_()
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/conditionalorders/'
                                   + str(_oid),
                                   _type = 'PUT',
                                   _data = _order)
            
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Cancel_Conditional_Order_(self, 
                                   _id=0, # Investor Account ID
                                   _oid=0): # Conditional Order ID
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/conditionalorders/'
                                   + str(_oid),
                                   _type = 'DELETE',
                                   _data = '{"0": 0}') # No data required
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Buy_At_Market_(self, 
                        _id=0, # Investor Account ID
                        _order=None):
        
        # Construct Buy Order dict if arg _order = None
        if _order is None:
            _order = self._generate_dummy_buy_order_()
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/orders/buy',
                                   _type = 'POST',
                                   _data = _order)
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
        
    #########################################################################
    
    def _Sell_At_Market(self,
                        _id=0, 
                        _order=None):
        
        # Construct Sell Order dict if arg _order = None
        if _order is None:
            _order = self._generate_dummy_sell_order_()
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/orders/sell',
                                   _type = 'POST',
                                   _data = _order)
            
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            
    #########################################################################
    
    def _Close_All_Account_Trades_(self, _id=0):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/'
                                   + str(_id)
                                   + '/stopout',
                                   _type = 'POST',
                                   _data = '{"0": 0}') # No data required
            
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Close_All_DARWIN_Trades_(self, 
                                  _id=0,
                                  _darwin='PLF.4.1'):
        
        if _darwin != '':
            try:
                return self._Call_API_(_endpoint='/investoraccounts/'
                                       + str(_id)
                                       + '/stopout/'
                                       + str(_darwin),
                                       _type = 'POST',
                                       _data = '{"0": 0}') # No data required
                
            except Exception as ex:
                _exstr = "Exception Type {0}. Args:\n{1!r}"
                _msg = _exstr.format(type(ex).__name__, ex.args)
                print(_msg)
        else:
            print('[ERROR] No DARWIN Ticker Symbol provided.. please try again.')
    
    #########################################################################
