# -*- coding: utf-8 -*-
"""
    DARWIN API - Authentication Class
    --
    @author: Darwinex Labs (www.darwinex.com)
    
    Last Updated: May 16, 2019
    
    Copyright (c) 2017-2019, Darwinex. All rights reserved.
    
    Licensed under the BSD 3-Clause License, you may not use this file except 
    in compliance with the License. 
    
    You may obtain a copy of the License at:    
    https://opensource.org/licenses/BSD-3-Clause
"""

import json, base64, requests

class DWX_OAuth2():
    
    def __init__(self, 
                 _creds_dict={},
                 _token_url='https://api.darwinex.com/token'):
        
        # Get tokens from server
        self._data = self._get_tokens_(_creds_dict['username'],
                                       _creds_dict['password'],
                                       _creds_dict['client_id'],
                                       _creds_dict['client_secret'],
                                       _token_url)
    
    ##########################################################################
    
    # Function implements password flow.
    def _get_tokens_(self,
                     username, password,
                     client_id, client_secret,
                     token_url):
    
        data = {'grant_type': 'password',
                'username': username,
                'password': password,
                'scope': 'openid'}
    
        headers = {'Authorization': 'Basic {}'
                    .format(base64.b64encode(bytes('{}:{}'
                                                    .format(client_id,client_secret)
                                                    .encode('utf-8'))).decode('utf-8'))}
    
        try:
            _response = requests.post(token_url, headers=headers, data=data, verify=True, allow_redirects=False)
            
            print('\n\n--+--+--\n[KERNEL] Access & Refresh Tokens Retrieved Successfully\n--+--+--\n')
            
            return json.loads(_response.text)
            
        except Exception as ex:
            print('Type: {0}, Args: {1!r}'.format(type(ex).__name__, ex.args))
            return None
    
    ##########################################################################
