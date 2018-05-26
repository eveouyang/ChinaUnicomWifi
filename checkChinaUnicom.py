#!/bin/env python3
# -*- coding:utf-8 -*-

import requests
import os, time, random, datetime
import logging
import ChinaUnicomUserInfo

class ChinaUnicom():
    '''
    Auto auth ChinaUnicom wifi function.
    '''

    def __init__(self):
        '''
        Set the default status to False
        '''
        self.status = False

    def login(self):
        '''
        Auth process
        '''
        headers = {}
        headers['Accept'] = 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
        headers['Referer'] = 'http://portal.gd165.com/index.do'
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        '''
        ChinaUnicomUserInfo.py
        #!/bin/env python3
        #! -*- coding: utf-8 -*-

        USERINFO = ['PHONE_NUMBER', 'PASSWORD']

        '''
        username = ChinaUnicomUserInfo.USERINFO[0]
        password = ChinaUnicomUserInfo.USERINFO[1]
        url = 'http://portal.gd165.com/login.do?callback=jQuery171024185281451507334_1527222491595&username=%s&password=%s&passwordType=6&wlanuserip=&userOpenAddress=gd&checkbox=0&basname=&setUserOnline=&sap=&macAddr=&bandMacAuth=0&isMacAuth=&basPushUrl=http%%253A%%252F%%252Fportal.gd165.com%%252F&passwordkey=asiainfo&_=1527222495041' % (username,password)
        check_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            url_request = requests.get(url,headers=headers)
            # self.test()
            # print('[ %s ] request:%s, Auth finally\n' % (check_time, url_request))
            logging.INFO('request: %s, Auth finish.\n')
        except requests.exceptions.ConnectionError as err:
            # print('[ %s ] requests.exceptions.ConnectionError\n' % check_time)
            logging.ERROR('requests.exceptions.ConnectionError, reconnect the wifi\n')
            os.system('nmcli connection down ChinaUnicom')
            os.system('nmcli connection up ChinaUnicom')
        except Exception as err:
            logging.ERROR('login exception\n%s\n' % err)
            # print('[ %s ] login exception\n%s\n' % (check_time, err))

    def login_test(self):
        '''
        Check the internet connection
        1. If the request test switch to the auth website, then retry the auth process.
        2. Try to ping the test url. If ping fail, then try to reconnect the ChinaUnicom wifi.
        '''
        while True:
            url_list = ['http://cn.bing.com',
                        'http://www.baidu.com',
                        'http://www.mydrivers.com']
            target_url = url_list[round(random.uniform(0,2))]
            ping_url = target_url.split('http://')[1]
            check_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            try:
                response = requests.get(target_url)
                if response.url.startswith('http://portal.gd165.com/'):
                    self.status = False
                else:
                    self.status = True
                if not self.status:
                    # print('[ %s ] Auth fail, try to reconnect the internet.\n' % check_time)
                    logging.WARNING('Auth fail, try to reconnect the internet.\n')
                    self.login()

                ping_test = os.system('ping %s -c 3 > /dev/null' % ping_url)
                if ping_test != 0:
                    # print('[ %s ] ping fail, reconnect the wifi\n' % check_time)
                    logging.WARNING('Ping fail, reconnect the wifi\n')
                    os.system('nmcli connection down ChinaUnicom')
                    os.system('nmcli connection up ChinaUnicom')
            except requests.exceptions.ConnectionError as err:
                # print('[ %s ] requests.exceptions.ConnectionError\n' % check_time)
                logging.ERROR('requests.exceptions.ConnectionError, reconnect the wifi\n')
                os.system('nmcli connection down ChinaUnicom')
                os.system('nmcli connection up ChinaUnicom')
            except Exception as err:
                # print('[ %s ] Exception\n' % check_time)
                logging.ERROR('Exception:\n' % err)

            time.sleep(round(random.uniform(3,8)))

        def log_setting(self):
            check_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            FORMAT = '[ %(asctime)-15s ] %(levelname)s: %(message)s'
            LOG_FILE = '/tmp/ChinaUnicom_wifi_.log'
            logging.getLogger('log').setLevel(logging.INFO)
            logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', filename=LOG_FILE)


if __name__ == '__main__':
    connect = ChinaUnicom()
    connect.log_setting()
    connect.login()
    connect.login_test()
