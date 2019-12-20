<?php
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);

    /*
        PHP function to request a new DARWIN API access token
        --
        @author: Darwinex Labs (www.darwinex.com)
        
        Last Updated: Dec 19, 2019
        
        Copyright (c) 2017-2019, Darwinex. All rights reserved.
        
        Licensed under the BSD 3-Clause License, you may not use this file except 
        in compliance with the License. 
        
        You may obtain a copy of the License at:    
        https://opensource.org/licenses/BSD-3-Clause
    */

    function dwx_refresh_tokens($dwx_token_ep,
                                $client_id, 
                                $client_secret, 
                                $refresh_token)
    {
        // Check if cURL is enabled
        if (function_exists('curl_version') == FALSE)
        {
            print('[ERROR] cURL must be enabled to use this script.. exiting.');
            exit();
        }

        // Set mandatory headers
        $headers = array();
        $headers[] = 'Authorization: Basic ' . base64_encode($client_id . ':' . $client_secret);
        $headers[] = 'Content-Type: application/x-www-form-urlencoded';
        
        // Set fields for refresh token request
        $opts = [
            'grant_type'        => 'refresh_token',
            'refresh_token'     => $refresh_token
        ];
        $opts_str = http_build_query($opts);

        // Initiate cURL connection
        $curl_handle = curl_init();

        // Set POST endpoint, options, request type
        curl_setopt($curl_handle, CURLOPT_URL, $dwx_token_ep);
        curl_setopt($curl_handle, CURLOPT_POST, true);
        curl_setopt($curl_handle, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($curl_handle, CURLOPT_POSTFIELDS, $opts_str);
        curl_setopt($curl_handle, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl_handle, CURLOPT_FOLLOWLOCATION, false);
        curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, true); 

        // Execute the request
        $ret = curl_exec($curl_handle);

        // Close connection
        curl_close($curl_handle);

        // Print the response
        return $ret;

    }

    /* /////////////////////////////////////////////////////////////// */

    // Test
    $ret = dwx_refresh_tokens('https://api.darwinex.com/token',
                              '<INSERT-CONSUMER-KEY-HERE>',
                              '<INSERT-CONSUMER-SECRET-HERE>',
                              '<INSERT-REFRESH-TOKEN-HERE>');

    var_dump(json_decode($ret, true));
?>
