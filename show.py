#!/usr/bin/python3
# Author        : Slobodan Blatnjak <blatnjak@gmail.com>
# Platform      : Contrail 19|20xx
version = '1'
# Date          : 2021-02-29

# This script provides a cli demo  to list and retrieve contrail config object details.

import argcomplete, argparse
import sys
#import pdb
import os, sys
dir_path = os.path.dirname(os.path.realpath("__file__"))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from config.VN_CLI import VNCLI
from config.IP_CLI import IPCLI
from config.RTCLI import RTCLI
#from control.Control_CLI import BGPCLI
#from control.Control_VN_CLI


API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'
LavelMap = {
    "vrouter": "contrail-vrouter-agent",
    "control": "contrail-control",
    "config": "contrail-api",
}
class ShowBasic(object):
    common_parser = argparse.ArgumentParser(add_help=False)
    def __init__(self, parser):
        self.subparser = parser.add_subparsers()

class Show_config(ShowBasic):
    API_PASSWORD = 'vj2q9QvhPHUupDaXmBXXXF6Aj'
    def __init__(self, parser):
        super().__init__(parser)
        self.add_parse_args()

    def show_config_vn(self, args):
        config_vn_cli = VNCLI() 
        config_vn_cli.print_VNs()
        
    def show_config_ip(self, args):
        config_ip_cli = IPCLI() 
        config_ip_cli.print_IPs()

    def show_config_ri(self, args):
        config_vn_cli = VNCLI() 
        config_vn_cli.print_VNs()

    def show_config_rt(self, args):
        config_rt_cli = RTCLI() 
        config_rt_cli.print_RTs()

    """ def show_control(self, args):
        print(args.ri) """
        

    def add_parse_args(self):
        subp = self.subparser.add_parser('vn',
                                         parents = [self.common_parser],
                                         help='Show Virtual Network')
        subp.add_argument('all', nargs='?', default='', help='all VNs')
        subp.add_argument('-name', '--name', default='', help='VN name')
        subp.set_defaults(func=self.show_config_vn)

        subp = self.subparser.add_parser('ip',
                                         parents = [self.common_parser],
                                         help='Show IP adresses')
        subp.add_argument('all', nargs='?', default='', help='all IPs')
        subp.add_argument('-address', '--address', default='', help='IP address')
        subp.set_defaults(func=self.show_config_ip)

        subp = self.subparser.add_parser('ri',
                                         parents = [self.common_parser],
                                         help='Show Routing Instance ')
        subp.add_argument('name', nargs='?', default='', help='RI name')
        subp.add_argument('-u', '--uuid', default='', help='RI uuid')
        subp.set_defaults(func=self.show_config_ri)

        subp = self.subparser.add_parser('rt',
                                         parents = [self.common_parser],
                                         help='Show Route  Target ')
        subp.add_argument('name', nargs='?', default='', help='RT name')
        subp.add_argument('-u', '--uuid', default='', help='RT uuid')
        subp.set_defaults(func=self.show_config_rt)

""" class Show_control(ShowBasic):
    def __init__(self, parser):
        super().__init__(parser)
        self.add_parse_args()

    def show_control_bgp(self, args):
        config_cli_bgp = BGP_CLI() 
        #if args.all != ''
        config_cli_bgp.print_bgp_neighboors()

    def show_control_ri(self, args):
        config_vn_cli = VN_CLI() 
        config_vn_cli.print_VNs()

    def show_control(self, args):
        print(args.ri)
        

    def add_parse_args(self):
        subp = self.subparser.add_parser('bgp',
                                         parents = [self.common_parser],
                                         help='Show Virtual Network')
        subp.add_argument('all', nargs='?', default='', help='all VNs')
        subp.add_argument('-name', '--name', default='', help='VN name')
        subp.set_defaults(func=self.show_control_bgp)

        subp = self.subparser.add_parser('ri',
                                         parents = [self.common_parser],
                                         help='Show Routing Instance ')
        subp.add_argument('name', nargs='?', default='', help='RI name')
        subp.add_argument('-u', '--uuid', default='', help='RI uuid')
        subp.set_defaults(func=self.show_control_ri) """


def main():
    #argv = sys.argv[1:]
    
    parser = argparse.ArgumentParser(prog='show',
        description='CLI show.')
    
    roleparsers = parser.add_subparsers()
    
    for level in sorted(LavelMap.keys()):
        p = roleparsers.add_parser(level, help=LavelMap[level])
        if 'Show_%s' % (level) in globals():
            globals()['Show_%s' % (level)](p)
    
    args, unknown = parser.parse_known_args()
    
    if ("func" in args):
      args.func(args)
    else:
      parser.print_usage()

    
if __name__ == "__main__":
    main()