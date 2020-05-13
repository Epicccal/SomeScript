# Usage : python3 decode_remember.py "evilCookie like rememberMe=xxx"
# 注意 : 使用了 xxd 工具
import sys
import subprocess
import base64
import re
import binascii
from Crypto.Cipher import AES

def decode_rememberme_file(rbtxt):
    # Base64 解码
    b64txt = rbtxt[11:].strip()
    rawtxt = base64.b64decode(b64txt)
    # AES 解码
    key  =  "kPH+bIxk5D2deZiIxcaaaA=="
    mode =  AES.MODE_CBC
    IV   = b' ' * 16
    encryptor = AES.new(base64.b64decode(key), mode, IV=IV)
    remember_ser= encryptor.decrypt(rawtxt)
    return remember_ser

def getxxd(filename):
    xd = ""
    # 通过 xxd -u 参数,使得十六进制字符串以大写方式输出 , 避免类名影响正则判断
    ret = subprocess.getoutput('xxd  -i ' + filename)
    # 调用 xxd 工具后删除临时文件
    delfile = ('rm', '-rf', 'decrypt.ser')
    subprocess.call('%s %s %s' % delfile, shell=True)
    # 正则匹配 , 获取 xxd -i 的十六进制字符串
    pattern = re.compile(r'0x[a-z0-9]{2}')
    res = re.findall(pattern, ret)
    for i in res:
       xd = xd + i.strip()
    result = xd.replace("0x","")
    return result

def getcommand(serhex):
    # 尝试通过正则匹配获取攻击者要执行的命令
    pattern = re.compile(r'002e0100.*0800300100')
    res = re.findall(pattern, serhex)
    # 8位前缀 + 2位命令长度
    # 如果攻击者执行的命令长度大于 0xFF (255位) , 则解不出来 .
    commandhex = res[0][10:][:-10]
    print("\n攻击者要执行的命令为 : \n\n" + binascii.a2b_hex(commandhex).decode("utf8")+"\n")
    
            
if __name__ == '__main__':
    # 创建临时文件 , 后续将要用到 xxd 命令
    with open("./decrypt.ser", 'wb+') as fpw:
        fpw.write(decode_rememberme_file(sys.argv[1]))
    #print(getxxd("./decrypt.ser"))
    getcommand(getxxd("decrypt.ser"))
