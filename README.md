# fuck_gfw_scan_ipv6

python2(win_64)

hosts_to_scan_domain.py:

        2404:6800:4008:801::2013 www.blog.google #ghs-svc-https-sni.ghs-ssl.googlehosted.com 
        --->
        www.blog.google

scan.py:
        
        www.blog.google
        --->
        2404:6800:4008:801::2013 www.blog.google


need to newfile:

        tmp.txt(Ex:Hosts)
        
        host.txt(hosts_to_scan_domain.py --->domain)
        
        host_not_out.txt(scan.py --->Not Ping or Not Ipv6)
        
        host_out.txt(scan.py --->final txt)
        
        
hosts:
        
        有重复
        ipv6
        
