# -*- coding: utf-8 -*-
"""
    DWX_API - Superclass for all sub-APIs
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: June 29, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""
import os, requests
os.chdir('<INSERT-PATH-TO-PROJECT-DIR-HERE>')

from AUTH.dwx_oauth2_p3 import DWX_OAuth2
from MINIONS.dwx_file_io import load_config

class DWX_API(object):
    
    def __init__(self, 
                 _api_url='https://api.darwinex.com',
                 _api_name='darwininfo',
                 _version=1.5,
                 _demo=False):
        
        # OAuth2 object for access/refresh token retrieval
        if _demo:
            _creds_filename = 'CONFIG/creds_demo.cfg'
        else:
            _creds_filename = 'CONFIG/creds.cfg'
            
        self._auth = DWX_OAuth2(load_config(_creds_filename))
        
        # Construct main production url for tagging endpoints
        self._url = '{}/{}/{}'.format(_api_url, _api_name, _version)
        
        # Construct authorization header for all requests
        self._auth_headers = {'Authorization': 'Bearer {}'.format(self._auth._data['access_token'])}
        
        # Construct headers for POST requests
        self._post_headers = {**self._auth_headers,
                              **{'Content-type':'application/json',
                                 'Accept':'application/json'}}
        
    ##########################################################################
    """
    Call any endpoint provided in the Darwinex API documentation, and get JSON.
    """
    def _Call_API_(self, _endpoint, _type, _data, _json=True, _stream=False):
        
        # If 
        if _type not in ['GET','POST','PUT', 'DELETE']:
            print('Bad request type')
            return None
        
        try:
            
            if _type == 'GET':
                _ret = requests.get(self._url + _endpoint,
                                    headers=self._auth_headers,
                                    verify=True)
            elif _type == 'PUT':
                _ret = requests.put(self._url + _endpoint,
                                    headers=self._post_headers,
                                    data=_data,
                                    verify=True)
            elif _type == 'DELETE':
                _ret = requests.delete(self._url + _endpoint,
                                       headers=self._auth_headers,
                                       #data=_data,
                                       verify=True)
            else:
                if len(_data) == 0:
                    print('Data is empty..')
                    return None
                
                # For DARWIN Quotes API
                if _stream:
                    
                    # Add POST header for streaming quotes        
                    self._post_headers['connection'] = 'keep-alive'
                    return requests.Request('POST',
                                           self._url + _endpoint,
                                           headers=self._post_headers,
                                           data=_data)
                else:
                    _ret = requests.post(self._url + _endpoint,
                                         data=_data,
                                         headers = self._post_headers,
                                         verify=True)
        
            if _json:
                return _ret.json()
            else:
                return _ret
        
        except Exception as ex:
            print('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            
    ##########################################################################
