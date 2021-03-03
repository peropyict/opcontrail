import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from rest.introspect import Introspect


class BGP:
    def __init__ (self):
        self.flag = ''

    def SnhShowBgpNeighborConfigReq(self, args=''):
            if 'search' in args:
                path = ('Snh_ShowBgpNeighborConfigReq?search_string=%s'
                    % (args.search))
            else:
                path = 'Snh_ShowBgpNeighborConfigReq'
            self.IST = Introspect()
            self.IST.get(path)
            xpath = '//ShowBgpNeighborConfig'
            '''if args.type == 'bgpaas':
                xpath += "[contains(router_type, '%s')]" % args.type
            elif args.type == 'fabric':
                xpath += "[router_type[not(normalize-space())]]"'''

            default_columns = ['name', 'admin_down', 'passive', 'router_type',
                            'local_as', 'autonomous_system', 'address',
                            'address_families', 'last_change_at']

            self.output_formatters(args, xpath, default_columns)
    
    def output_formatters(self, args, xpath, default_columns=[]):
        if args.format == 'text':
            self.IST.printText(xpath)
        else:
            max_width = args.max_width or Default_Max_Width
            if args.columns:
                self.IST.printTbl(xpath, max_width, *args.columns)
            else:
                self.IST.printTbl(xpath, max_width, *default_columns)