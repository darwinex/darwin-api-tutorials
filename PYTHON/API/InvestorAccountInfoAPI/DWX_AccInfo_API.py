# -*- coding: utf-8 -*-
"""
    DWX_AccInfo_API.py - Investor AccountInfo API (Subclass of DWX_API)
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

class DWX_AccInfo_API(DWX_API):
    
    def __init__(self,
                 _api_url='https://api.darwinex.com',
                 _api_name='investoraccountinfo',
                 _version=1.1,
                 _demo=True):
        
        super(DWX_AccInfo_API, self).__init__(_api_url,_api_name,_version,_demo)
        
        if _demo:
            print(f'--+--+--\n[KERNEL] InvestorAccountInfoAPI v{_version} initialized in DEMO environment\n--+--+--')
        else:
            print(f'--+--+--\n[KERNEL] InvestorAccountInfoAPI v{_version} initialized in REAL environment\n--+--+--')
        
    ######################################################################### 
    
    def _Get_Accounts_(self):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts', 
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            
    #########################################################################
    
    def _Get_Account_Info_(self, _id=0):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/' + str(_id), 
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Get_Trade_by_ID_(self, _id=0, _tid=0):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/' 
                                   + str(_id)
                                   + '/trades/'
                                   + str(_tid), 
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Get_Order_by_ID_(self, _id=0, _oid=0):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/' 
                                   + str(_id)
                                   + '/orders/'
                                   + str(_oid), 
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
    
    #########################################################################
    
    def _Get_Conditional_Order_by_ID_(self, _id=0, _oid=0):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/' 
                                   + str(_id)
                                   + '/conditionalorders/'
                                   + str(_oid), 
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            
    #########################################################################
    
    def _Get_Conditional_Orders_by_Status_(self, 
                                           _id=0, 
                                           _darwin='',
                                           _status='pending',
                                           _page=0,
                                           _perpage=1):
        
        # If valid _status given, then:
        if _status in ['pending','executed','rejected','cancelled','deleted']:
            
            try:
                return self._Call_API_(_endpoint='/investoraccounts/' 
                                       + str(_id)
                                       + '/conditionalorders/'
                                       + str(_status)
                                       + '?productName=' + str(_darwin)
                                       + '&page=' + str(_page)
                                       + '&per_page=' + str(_perpage),
                                       _type='GET', _data='')
            except Exception as ex:
                _exstr = "Exception Type {0}. Args:\n{1!r}"
                _msg = _exstr.format(type(ex).__name__, ex.args)
                print(_msg)
        else:
            print('[ERROR] Invalid Conditional Order Status -> Must be one \
                  of pending, rejected, executed or cancelled.')
            
    #########################################################################
    
    def _Get_Current_Open_Positions_(self, 
                                     _id=0,
                                     _darwin=''):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/' 
                                   + str(_id)
                                   + '/currentpositions'
                                   + '?productName=' + str(_darwin),
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            
    #########################################################################
    
    def _Get_Executed_Orders_(self, 
                               _id=0, 
                               _darwin='PLF.4.1',
                               _page=0,
                               _perpage=1):
        
        try:
            return self._Call_API_(_endpoint='/investoraccounts/' 
                                   + str(_id)
                                   + '/orders/executed'
                                   + '?productName=' + str(_darwin)
                                   + '&page=' + str(_page)
                                   + '&per_page=' + str(_perpage),
                                   _type='GET', _data='')
        except Exception as ex:
            _exstr = "Exception Type {0}. Args:\n{1!r}"
            _msg = _exstr.format(type(ex).__name__, ex.args)
            print(_msg)
            
    #########################################################################
    
    def _Get_Trades_by_Status_(self, 
                               _id=0, 
                               _darwin='PLF.4.1',
                               _status='open',
                               _page=0,
                               _perpage=1):
        
        # If valid _status given, then:
        if _status in ['open','closed']:
            
            try:
                return self._Call_API_(_endpoint='/investoraccounts/' 
                                       + str(_id)
                                       + '/trades/'
                                       + _status
                                       + '?productName=' + str(_darwin)
                                       + '&page=' + str(_page)
                                       + '&per_page=' + str(_perpage),
                                       _type='GET', _data='')
            except Exception as ex:
                _exstr = "Exception Type {0}. Args:\n{1!r}"
                _msg = _exstr.format(type(ex).__name__, ex.args)
                print(_msg)
        else:
            print('[ERROR] Invalid Trade Status -> Must be one \
                  of open or closed.')
            
    #########################################################################
