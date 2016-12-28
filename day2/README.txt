Name:myShoppingMall
Auther: Kaye Gao
Blog:http://www.cnblogs.com/huamingao/

# Requirement:
完美购物车
1. 用户登录
若为新用户，提示输入初始密码和金额；
若为老用户，输错3次密码，账号状态变为锁定，退出程序
账号状态为锁定的用户，必须由管理员手动更改账号状态，才能登录成功进行后面的操作
允许用户登录文件不存在

2. 商品信息显示
（1）商品展示格式如下：
    编号 商品名称 价格
（2）已购商品展示格式如下：
    编号 商品名称 单价 数量 总价 上次购买时间

3. 用户选项
输入商品类目编号，进入下一层商品类目或商品价格列表
进入商品价格列表后，输入商品编号，则购买该商品，余额不足时进行提醒
输入a，充值
输入b，返回上层菜单
输入c，查看已购商品
输入q，退出程序
其他任何输入，视为输入不合法，提示用户重新输入，直至输入正确为止
用户可重复购物，每轮购物结束时，若用户输入q则退出程序，若输入非q的任意键则可以继续购物

# Data Structure:

商品列表存储在一个三层字典中，该字典设置为常量，字典形如：
DIC = {'品类A'：{'品牌A':{'产品A':价格,'产品B':价格,...},'品牌B':{...},...},'品类B':{...},...}

shopcart文件内容按照以下格式存储：
用户名A:密码：账号状态：余额:商品A*数量*最后买入时间:商品B*数量*最后买入时间：商品C*数量*最后买入时间:.....
用户名B:密码：账号状态：余额:商品A*数量*最后买入时间:商品B*数量*最后买入时间：商品C*数量*最后买入时间:.....
用户名C:密码：账号状态：余额:商品A*数量*最后买入时间:商品B*数量*最后买入时间：商品C*数量*最后买入时间:.....

shopcart文件内容转换成字典，格式如下：
dictUsr = {
    userA:[
        password,
        account_status,
        money,[
           {productA:[quantity,last_purchase_date]},
           {productB:[quantity,last_purchase_date]},
            ...
            ]
        ],
    userB:[
        password,
        account_status,
        money,[
            {productA:[quantity,last_purchase_date]},
            {productB:[quantity,last_purchase_date]},
            ...
            ]
        ],
    ...
    }


# Function 函数功能介绍:

def mkDict(file): 通过读取文件内容，获得购物车历史信息，构建形如{usr:[pwd,stat,money,{productA:[quantity,last_purchase_time],...},...}的字典。

def dictToFile(file,dic): 将字典中的数据格式化写入文件（覆盖写），该文件存储购物车历史信息。

def get_embed_dic(current_dic, option):在打印商品列表时调用，根据option值和当前字典（当前所在商品层级），返回内嵌的下一级字典

def get_upper_dic(dic, current_dic):在打印商品列表时调用，根据当前字典和初始字典，返回当前字典的上一级字典（从当前商品层级返回上一级）

def login(file):登录模块，通过调用函数mkDict读取文件内容，若账号存在，检查账号状态，若状态为被锁定，返回[False,username]；否则，提示输入密码，输入正确返回[True,username]，
输错密码达到3次，锁定账号，通过调用函数dictToFile更新文件，返回[False,username]。若账号不存在，提示输入初始密码、初始金额，更新文件，返回[True,username]

def print_shopcart(all_user_shopcart,username):打印当前用户的已购入商品信息（商品，数量，最后一次购买时间）

def get_price(product_dic,product_name):根据商品名，从商品字典中获取商品单价，并返回

def input_isdigit(msg_prompt,invalid_prompt): 提示用户输入，输错打印'输入不合法'，直至输入合法为止






