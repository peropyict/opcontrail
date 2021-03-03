import sys, os
import argparse
import socket, struct
import requests
try:
    from urllib.parse import urlencode # python3
except:
    from urllib import urlencode # python2
from datetime import datetime
from lxml import etree
from prettytable import PrettyTable
from uuid import UUID

debug = False
Default_Max_Width = 36
proxy = None
token = None


class Introspect:
    def __init__ (self, host='', port='', filename=''):
        host = "127.0.0.1"
        port = "8083"
        self.host_url = "http://" + host + ":" + str(port) + "/"
        
    def is_ipv4(self, addr):
        try:
            socket.inet_pton(socket.AF_INET, addr)
        except socket.error:
            return False
        return True

    def is_ipv6(self, addr):
        try:
            socket.inet_pton(socket.AF_INET6, addr)
        except socket.error:
            return False
        return True
    
    def addressInNetwork(self, addr, prefix):
        ipaddr = struct.unpack('!L',socket.inet_aton(addr))[0]
        pure_prefix = prefix.split(':')[-1]  # strip RD info if any
        netaddr,bits = pure_prefix.split('/')
        netaddr = struct.unpack('!L',socket.inet_aton(netaddr))[0]
        netmask = ((1<<(32-int(bits))) - 1)^0xffffffff
        return ipaddr & netmask == netaddr & netmask

    def addressInNetwork6(self, addr, prefix):
        addr_upper,addr_lower = struct.unpack(
                                '!QQ',socket.inet_pton(socket.AF_INET6, addr))
        netaddr,bits = prefix.split('/')
        net_upper,net_lower = struct.unpack(
                            '!QQ',socket.inet_pton(socket.AF_INET6, netaddr))
        if int(bits) < 65 :
            netmask = ((1<<(64-int(bits))) - 1)^0xffffffffffffffff
            return addr_upper & netmask == net_upper & netmask
        elif addr_upper != net_upper:
            return False
        else:
            netmask = ((1<<(128-int(bits))) - 1)^0xffffffffffffffff
            return addr_lower & netmask == net_lower & netmask

    def get (self, path):
        """ get introspect output """
        self.output_etree = []

        
        while True:
            url = self.host_url + path.replace(' ', '%20')
            headers = {}
            if proxy and token:
                url = proxy + "/forward-proxy?" + urlencode({'proxyURL': url})
                headers['X-Auth-Token'] = token
            if debug: print("DEBUG: retrieving url " + url)
            try:
                response = requests.get(url,headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                print('The server couldn\'t fulfill the request.')
                print('URL: ' + url)
                print('Error code: ', response.status_code)
                print('Error text: ', response.text)
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                print('Failed to reach destination')
                print('URL: ' + url)
                print('Reason: ', e)
                sys.exit(1)
            else:
                ISOutput = response.text
                response.close()

            self.output_etree.append(etree.fromstring(ISOutput))

            if 'Snh_PageReq?x=' in path:
                break

            # some routes output may be paginated
            pagination_path = "//Pagination/req/PageReqData"
            pagination = self.output_etree[-1].xpath(pagination_path)
            if len(pagination):
                if (pagination[0].find("next_page").text is not None):
                    all = pagination[0].find("all").text
                    if(all is not None):
                        path = 'Snh_PageReq?x=' + all
                        self.output_etree = []
                        continue
                    else:
                        print("Warning: all page in pagination is empty!")
                        break
                else:
                    break

            next_batch = self.output_etree[-1].xpath("//next_batch")

            if not len(next_batch):
                break

            if (next_batch[0].text and next_batch[0].attrib['link']):
                path = 'Snh_' + next_batch[0].attrib['link'] + \
                        '?x=' + next_batch[0].text
            else:
                break
            if debug: print("instrosepct get completes\n")
        if debug:
            for tree in self.output_etree:
                etree.dump(tree)

    def printTbl(self, xpathExpr, max_width=Default_Max_Width, *args):
        """ print introspect output in a table.
            args lists interested fields. """
        items = []
        for tree in self.output_etree:
            items = items + tree.xpath(xpathExpr)
        if len(items):
            Introspect.dumpTbl(items, max_width, args)

    def printText(self, xpathExpr):
        """ print introspect output in human readable text """
        for tree in self.output_etree:
            for element in tree.xpath(xpathExpr):
                print(Introspect.elementToStr('', element).rstrip())

    @staticmethod
    def dumpTbl(items, max_width, columns):

        if not len(items):
            return

        if len(columns):
            fields = columns
        else:
            fields = [ e.tag for e in items[0] if e.tag != "more"]

        tbl = PrettyTable(fields)
        tbl.align = 'l'
        tbl.max_width = max_width
        for entry in items:
            row = []
            for field in fields:
                f = entry.find(field)
                if f is not None:
                    if f.text:
                        row.append(f.text)
                    elif list(f):
                        for e in f:
                            row.append(Introspect.elementToStr('', e).rstrip())
                    else:
                        row.append("n/a")
                else:
                    row.append("-")
            tbl.add_row(row)
        print(tbl)

    @staticmethod
    def elementToStr(indent, etreenode):
        """ convernt etreenode sub-tree into string """
        elementStr=''

        if etreenode.tag == 'more':   #skip more element
            return elementStr

        if etreenode.text and etreenode.tag == 'element':
            return indent + etreenode.text + "\n"
        elif etreenode.text:
            return indent + etreenode.tag + ': ' + \
                    etreenode.text.replace('\n', '\n' + \
                    indent + (len(etreenode.tag)+2)*' ') + "\n"
        elif etreenode.tag != 'list':
            elementStr += indent + etreenode.tag + "\n"

        if 'type' in etreenode.attrib:
            if etreenode.attrib['type'] == 'list' and \
                    etreenode[0].attrib['size'] == '0':
                return elementStr

        for element in etreenode:
            elementStr += Introspect.elementToStr(indent + '  ', element)

        return elementStr

    @staticmethod
    def pathToStr(indent, path, mode):

        path_info = ''
        if mode == 'raw':
            for item in path:
                 path_info += Introspect.elementToStr(indent, item)
            return path_info.rstrip()

        now = datetime.utcnow()

        path_modified = path.find("last_modified").text
        t1 = datetime.strptime(path_modified, '%Y-%b-%d %H:%M:%S.%f')
        path_age = str(now - t1).replace(',', '')
        path_proto = path.find("protocol").text
        path_source = path.find("source").text
        path_lp = path.find("local_preference").text
        path_as = path.find("as_path").text
        path_nh = path.find("next_hop").text
        path_label = path.find("label").text
        path_vn = path.find("origin_vn").text
        path_pri_tbl = path.find("primary_table").text
        path_vn_path = str(path.xpath("origin_vn_path/list/element/text()"))
        path_encap = str(path.xpath("tunnel_encap/list/element/text()"))
        path_comm = str(path.xpath("communities/list/element/text()"))
        path_sqn = path.find("sequence_no").text
        path_flags = path.find("flags").text

        path_info = ("%s[%s|%s] age: %s, localpref: %s, nh: %s, "
                     "encap: %s, label: %s, AS path: %s" %
                    (indent, path_proto, path_source, path_age, path_lp,
                     path_nh, path_encap, path_label, path_as))

        if mode == 'detail':
            path_info += ("\n%sprimary table: %s, origin vn: %s, "
                          "origin_vn_path: %s" %
                          (2*indent, path_pri_tbl, path_vn, path_vn_path))
            path_info += "\n%scommunities: %s" % (2*indent, path_comm)
            path_info += "\n%slast modified: %s" % (2*indent, path_modified)

        return path_info

    @staticmethod
    def routeToStr(indent, route, mode):

        route_info = ''
        now = datetime.utcnow()

        prefix = route.find("prefix").text
        prefix_modified = route.find("last_modified").text
        t1 = datetime.strptime(prefix_modified, '%Y-%b-%d %H:%M:%S.%f')
        prefix_age = str(now - t1).replace(',', '')

        route_info += "%s%s, age: %s, last_modified: %s" % \
                    (indent, prefix, prefix_age, prefix_modified)

        for path in route.xpath('.//ShowRoutePath'):
            route_info += "\n" + Introspect.pathToStr(indent*2, path, mode)

        return route_info.rstrip()

    def showRoute_VR(self, xpathExpr, family, address, mode):
        """ method to show route output from vrouter intropsect """
        indent = ' ' * 4

        ADDR_INET4 = 4
        ADDR_INET6 = 6
        ADDR_NONE = 0

        addr_type = ADDR_NONE
        if self.is_ipv4(address):
            addr_type = ADDR_INET4
        elif self.is_ipv6(address):
            addr_type = ADDR_INET6

        for tree in self.output_etree:
            for route in tree.xpath(xpathExpr):
                if 'inet' in family:
                    prefix = route.find("src_ip").text + '/' + \
                                route.find("src_plen").text
                else:
                    prefix = route.find("mac").text

                if family == 'inet' and addr_type == ADDR_INET4:
                    if not self.addressInNetwork(address, prefix):
                        if debug: print("DEBUG: skipping " + prefix)
                        continue
                elif family == 'inet6' and addr_type == ADDR_INET6:
                    if not self.addressInNetwork6(address, prefix):
                        if debug: print("DEBUG: skipping " + prefix)
                        continue

                if mode == "raw":
                    print(Introspect.elementToStr('', route).rstrip())
                    continue

                output = prefix + "\n"

                for path in route.xpath(".//PathSandeshData"):
                    nh = path.xpath("nh/NhSandeshData")[0]

                    peer = path.find("peer").text
                    pref = path.xpath("path_preference_data/"
                                      "PathPreferenceSandeshData/"
                                      "preference")[0].text

                    path_info = "%s[%s] pref:%s\n" % (indent, peer, pref)

                    path_info += indent + ' '
                    nh_type = nh.find('type').text
                    if nh_type == "interface":
                        mac = nh.find('mac').text
                        itf = nh.find("itf").text
                        label = path.find("label").text
                        path_info += ("to %s via %s, assigned_label:%s, "
                                        % (mac, itf, label))

                    elif nh_type == "tunnel":
                        tunnel_type = nh.find("tunnel_type").text
                        dip = nh.find("dip").text
                        sip = nh.find("sip").text
                        label = path.find("label").text
                        if nh.find('mac') is not None:
                            mac = nh.find('mac').text
                            path_info += ("to %s via %s dip:%s "
                                          "sip:%s label:%s, "
                                          % (mac, tunnel_type, dip,
                                             sip, label))
                        else:
                            path_info += ("via %s dip:%s sip:%s label:%s, "
                                          % (tunnel_type, dip, sip, label))

                    elif nh_type == "receive":
                        itf = nh.find("itf").text
                        path_info += "via %s, " % (itf)

                    elif nh_type == "arp":
                        mac = nh.find('mac').text
                        itf = nh.find("itf").text
                        path_info += "via %s, " % (mac)

                    elif 'Composite' in str(nh_type):
                        comp_nh = str(nh.xpath(".//itf/text()"))
                        path_info += "via %s, " % (comp_nh)

                    elif 'vlan' in str(nh_type):
                        mac = nh.find('mac').text
                        itf = nh.find("itf").text
                        path_info += "to %s via %s, " % (mac, itf)

                    nh_index = nh.find("nh_index").text
                    if nh.find("policy") is not None:
                        policy = nh.find("policy").text
                    else:
                        policy = ''
                    active_label = path.find("active_label").text
                    vxlan_id = path.find("vxlan_id").text
                    path_info += ("nh_index:%s , nh_type:%s, nh_policy:%s, "
                                  "active_label:%s, vxlan_id:%s" %
                                 (nh_index, nh_type, policy,
                                  active_label, vxlan_id))

                    if mode == "detail":
                        path_info += "\n"
                        path_info += indent + ' dest_vn:' + \
                            str(path.xpath("dest_vn_list/list/element/text()"))
                        path_info += ', sg:' + \
                            str(path.xpath("sg_list/list/element/text()"))
                        path_info += ', communities:' +  \
                            str(path.xpath("communities/list/element/text()"))
                    output += path_info + "\n"

                print(output.rstrip())

    def showRoute_CTR(self, last, mode):
        """ show route output from control node intropsect """
        indent = ' ' * 4
        now = datetime.utcnow()
        printedTbl = {}
        xpath_tbl = '//ShowRouteTable'
        xpath_rt = './/ShowRoute'
        xpath_pth = './/ShowRoutePath'
        for tree in self.output_etree:
            for table in tree.xpath(xpath_tbl):
                tbl_name = table.find('routing_table_name').text
                prefix_count = table.find('prefixes').text
                tot_path_count = table.find('paths').text
                pri_path_count = table.find('primary_paths').text
                sec_path_count = table.find('secondary_paths').text
                ifs_path_count = table.find('infeasible_paths').text

                if not(tbl_name in printedTbl):
                    print(("\n%s: %s destinations, %s routes "
                            "(%s primary, %s secondary, %s infeasible)"
                            % (tbl_name, prefix_count, tot_path_count,
                               pri_path_count, sec_path_count,
                               ifs_path_count)))
                    printedTbl[tbl_name] = True


                # start processing each route
                for route in table.xpath(xpath_rt):
                    paths = route.xpath(xpath_pth)
                    if not (len(paths)):
                        continue
                    prefix = route.find("prefix").text
                    prefix_modified = route.find("last_modified").text
                    t1 = datetime.strptime(prefix_modified,
                                           '%Y-%b-%d %H:%M:%S.%f')
                    prefix_age = str(now - t1).replace(',', '')

                    if (last and (now - t1).total_seconds() > last):
                        for path in paths:
                            path_modified = path.find("last_modified").text
                            t1 = datetime.strptime(path_modified,
                                                   '%Y-%b-%d %H:%M:%S.%f')
                            path_age = str(now - t1).replace(',', '')
                            if not ((now - t1).total_seconds() > last) :
                                print(("\n%s, age: %s, last_modified: %s" %
                                        (prefix, prefix_age, prefix_modified)))
                                print(Introspect.pathToStr(indent, path, mode))
                    else:
                        print(("\n%s, age: %s, last_modified: %s" %
                                (prefix, prefix_age, prefix_modified)))
                        for path in paths:
                            print(Introspect.pathToStr(indent, path, mode))

    def showSCRoute(self, xpathExpr):

        # fields = ['src_virtual_network',
        #             'dest_virtual_network',
        #             'service_instance',
        #             'state',
        #             'connected_route',
        #             'more_specifics',
        #             'ext_connecting_rt']
        fields = ['service_instance',
                  'state',
                  'connected_route',
                  'more_specifics',
                  'ext_connecting_rt']

        tbl = PrettyTable(fields)
        tbl.align = 'l'

        # start building the table
        for tree in self.output_etree:
            for sc in tree.xpath(xpathExpr):
                row = []
                for field in fields[0:2]:
                    f = sc.find(field)
                    if f is not None:
                        if f.text:
                            row.append(f.text)
                        elif list(f):
                            row.append(Introspect.elementToStr('', f).rstrip())
                        else:
                            row.append("n/a")
                    else:
                        row.append("non-exist")

                sc_xpath = ('./connected_route/ConnectedRouteInfo'
                            '/service_chain_addr')
                service_chain_addr = sc.xpath(sc_xpath)[0]
                row.append(Introspect.elementToStr('', service_chain_addr).rstrip())

                specifics = ''
                spec_xpath = './more_specifics/list/PrefixToRouteListInfo'
                PrefixToRouteListInfo = sc.xpath(spec_xpath)
                for p in PrefixToRouteListInfo:
                    specifics += ("prefix: %s, aggregate: %s\n" %
                                (p.find('prefix').text,
                                 p.find('aggregate').text))
                row.append(specifics.rstrip())

                ext_rt = ''
                ext_xpath = './ext_connecting_rt_info_list//ext_rt_prefix'
                ext_rt_prefix_list = sc.xpath(ext_xpath)
                for p in ext_rt_prefix_list:
                    ext_rt += p.text + "\n"
                row.append(ext_rt.rstrip())

                tbl.add_row(row)

        print(tbl)

    def showSCRouteDetail(self, xpathExpr):

        indent = ' ' * 4

        fields = ['src_virtual_network', 'dest_virtual_network',
                  'service_instance', 'src_rt_instance',
                  'dest_rt_instance', 'state']
        for tree in self.output_etree:

            for sc in tree.xpath(xpathExpr):

                for field in fields:
                    print("%s: %s" % (field, sc.find(field).text))

                print("connectedRouteInfo:")
                sc_xpath = ('./connected_route/ConnectedRouteInfo'
                            '/service_chain_addr')
                print(("%sservice_chain_addr: %s" %
                       (indent, sc.xpath(sc_xpath)[0].text)))
                for route in sc.xpath('./connected_route//ShowRoute'):
                    print(Introspect.routeToStr(indent, route, 'detail'))

                print("more_specifics:")
                specifics = ''
                spec_xpath = './more_specifics/list/PrefixToRouteListInfo'
                PrefixToRouteListInfo = sc.xpath(spec_xpath)
                for p in PrefixToRouteListInfo:
                    specifics += ("%sprefix: %s, aggregate: %s\n" %
                                  (indent, p.find('prefix').text,
                                   p.find('aggregate').text))
                print(specifics.rstrip())

                print("ext_connecting_rt_info_list:")
                ext_xpath = './/ExtConnectRouteInfo/ext_rt_svc_rt/ShowRoute'
                for route in sc.xpath(ext_xpath):
                    print(Introspect.routeToStr(indent, route, 'detail'))

                print(("aggregate_enable:%s\n" %
                       (sc.find("aggregate_enable").text)))

    def showStaticRoute(self, xpathExpr, format, max_width, columns):
        if not columns:
            columns = []
        if not max_width:
            max_width = Default_Max_Width
        for tree in self.output_etree:
            for entry in tree.xpath(xpathExpr):
                if format == 'table':
                    print('ri_name: %s' % (entry.find('ri_name').text))
                    Introspect.dumpTbl(entry.xpath("//StaticRouteInfo"),
                                       max_width, columns)
                else:
                    print(Introspect.elementToStr('', entry))

