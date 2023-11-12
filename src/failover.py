#!/usr/bin/env python3

"""
@brief  This script will switch the default gateway depending on Internet 
        connection availability. It is meant to be run periodically, as it 
        checks whether Internet is working, and if not switches the default
        gateway to one that works.
        The list of --gateways MUST be passed to this script in order of 
        priority. The preferred gateway first.

@details  This code has been inspired by:

          https://ryanclouser.com/linux/2020/08/22/Linux-4G-LTE-Failover.html

@author Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com)
@date   12 Nov 2023.
"""

import argparse
import sys
import os
import re
import subprocess as sp


def shell(cmd: str, output_wanted: bool = False):
    """
    @brief Runs a command and gets you the output if you want it. Otherwise
           the output is sent to /dev/null and not printed.

    @param[in]  cmd            Command you want to run.
    @param[in]  output_wanted  Set it to True if you want the output returned.

    @returns None unless you set output_wanted to True.
    """
    if output_wanted:
        data = sp.Popen(cmd + ' 2>&1', shell=True, stdout=sp.PIPE).communicate()[0].decode('utf-8')
        return data
    else:
        sp.call(cmd, shell=True, stdout=open(os.devnull, 'w'))
        return None


def get_default_gateway() -> str:
    """
    @returns a string containing the IP of the default gateway if there is one.
             Otherwise returns None.
    """
    try:
        output = shell('ip route show', output_wanted=True) 
        m = re.match(r'default via (\d*\.\d*\.\d*\.\d*) dev', output)
        return m.group(1)
    except:
        return None


def dns_query(domain: str, test_dns_server):
    """
    @brief TODO

    @param[in]  dns_servers  List of strings containing IP addresses of DNS
                             servers.
    """
    return shell('dig +time=1 +tries=1 @' + test_dns_server + ' google.com | grep ANSWER',
                 output_wanted=True)

    
def gateway_works(gw_ip: str, test_ip='91.189.91.39') -> bool:
    """
    @brief  Checks whether a given gateway works or not. 
    
    @param[in]  gw_ip    IP address of the gateway.
    @param[in]  test_ip  IP of the DNS server we will try to connect
                         to in order to evaluate whether the gateway
                         works or not.

    @returns True if the gateway works. Otherwise returns False.
    """
    gateway_works = False
    
    # If the gateway does not even exist, we don't need to check the DNS
    output = shell('ip route add ' + test_ip + ' via ' + gw_ip, 
                   output_wanted=True)
    if 'invalid gateway' in output:
        return False
    
    # Route packets to test DNS server via the provided gateway
    output = shell('nc -zv -w 1 ' + test_ip + ' 80', output_wanted=True)
    if 'succeeded' in output:
        gateway_works = True
    shell('ip route del ' + test_ip)
    
    return gateway_works


def read_cmdline_params():
    cli = argparse.ArgumentParser()
    cli.add_argument("--gateways", nargs="*", type=str, required=True) 
    return cli.parse_args()


def main():
    # Read command line parameters
    args = read_cmdline_params()

    # Check if command dig is present 
    if not shell('dig', output_wanted=True):
        raise RuntimeError('[ERROR] Command dig is not available.')  
    
    # Get the IP of the gateway we are using right now
    current_gw_ip = get_default_gateway()

    # Switch gateway if needed
    for gw_ip in args.gateways:
        sys.stdout.write('[INFO] Checking if gateway ' + gw_ip + ' works... ')
        sys.stdout.flush()
        works = gateway_works(gw_ip)
        if works:
            sys.stdout.write("Yes!\n")
            if gw_ip == current_gw_ip:
                print('[INFO] ' + gw_ip + ' is the current gateway, and it is working, nothing will be changed.')
            else:
                shell('ip route del default')
                shell('ip route add default via ' + gw_ip)
                shell('ip route flush cache')
                print('[INFO] Default gateway changed to ' + gw_ip)
            break
        else:
            sys.stdout.write("No!\n")
        

if __name__ == "__main__":
    main()
