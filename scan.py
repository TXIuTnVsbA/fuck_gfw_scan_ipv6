# -*- coding: utf-8 -*-
import os,re,time
from multiprocessing import Pool
def ipv6_addr(addr):
    '''
    Returns True if the IPv6 address (and optional subnet) are valid, otherwise
    returns False.
    '''
    # From http://stackoverflow.com/questions/6276115/ipv6-regexp-python
    ip6_regex = (r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,6}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|'
                 r'(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4})'
                 r'{1,7}\Z)|(\A((([0-9a-f]{1,4}:){6})(25[0-5]|2[0-4]\d|[0-1]'
                 r'?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
                 r'(\A(([0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
                 r'(\A([0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,4}:(25[0-5]|'
                 r'2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d))'
                 r'{3}\Z)|(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,3}:'
                 r'(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?'
                 r'\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4})'
                 r'{1,2}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]'
                 r'{1,4}){1,1}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|'
                 r'2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A(([0-9a-f]{1,4}:){1,5}|:):'
                 r'(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?'
                 r'\d?\d)){3}\Z)|(\A:(:[0-9a-f]{1,4}){1,5}:(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)')
    return bool(re.match(ip6_regex, addr))
def dns_ipv6(domain):
    time.sleep(0.2)
    cmd = "nslookup -qt=AAAA {arg} 8.8.8.8".format(arg=domain)
    #cmd = "nslookup -qt=AAAA {arg}".format(arg=domain)
    try:
        tmp1 = str(os.popen(cmd).read())
        tmp2 = tmp1.split()[7]
        if ipv6_addr(tmp2):
            return tmp2
    except:
        return -1
    return -1
def ping(text):
    for i in range(3):
        cmd = "ping  -n 5 -w 1 {arg}".format(arg=text)
        tmp1 = str(os.popen(cmd).read())
        if re.findall('\\d+ms', tmp1):
            return 1
    return 0
def all(arg):
    fp = open("host_out.txt", "r")
    dm = arg.split("\r\n")[0]
    if fp.read().find(dm) == -1:
        ipv6 = dns_ipv6(dm)
        if ipv6 != -1:
            if fp.read().find(ipv6) == -1:
                fp = open("host_not_out.txt", "r")
                if fp.read().find(dm) == -1:
                    bool_ping = ping(ipv6)
                    if bool_ping == 0:
                        try:
                            fp = open("host_not_out.txt", "a")
                            fp.write(ipv6 + " " + dm + "\r\n")
                            fp.close()
                        finally:
                            print ipv6, dm
                    if bool_ping == 1:
                        try:
                            fp = open("host_out.txt", "a")
                            fp.write(ipv6 + " " + dm + "\r\n")
                            fp.close()
                        finally:
                            print ipv6, dm

            else:
                try:
                    fp = open("host_out.txt", "a")
                    fp.write(ipv6 + " " + dm + "\r\n")
                    fp.close()
                finally:
                    print ipv6, dm
        else:
            fp = open("host_not_out.txt", "r")
            if fp.read().find(dm) == -1:
                try:
                    fp = open("host_not_out.txt", "a")
                    fp.write(dm + "\r\n")
                    fp.close()
                finally:
                    print ipv6, dm
    #exit()
def main():
    pool = Pool(10)
    result = []
    # rl = pool.map(run, testFL)
    # pool.close()  # 关闭进程池，不再接受新的进程
    # pool.join()  # 主进程阻塞等待子进程的退出
    for line in open("host.txt", "r"):
        if line.find("#") == 0:
            continue
        result.append(pool.apply_async(all, (line,)))
    pool.close()
    pool.join()
    for res in result:
        print res.get()
    print "Sub-process(es) done."

if __name__ == "__main__":
    main()
