欢迎使用本程序！

本节课总结：
多层装饰器、迭代器&生成器
Python学习总结【第三篇】：Python之函数(自定义函数、内置函数、lambda表达式、装饰器、迭代器&生成器)
http://www.cnblogs.com/madsnotes/articles/5515410.html

字符串格式（百分号，format方式）
Python学习总结【第二篇】：Python数据结构（字符串、列表、元组、字典、set集合）
http://www.cnblogs.com/madsnotes/articles/5492004.html

模块
Python学习总结【第六篇】：Python之模块
http://www.cnblogs.com/madsnotes/articles/5537947.html

程序目录规范：
bin                 # 存放可执行程序，入口文件
config              # 存放配置信息
   settings.py      # 全局配置文件
db                  # 存放数据文件
docs                # 相关文档说明
examples            # 案例或者临时文件存放目录
lib                 # 存放通用的库(例如：md5加密)
src                 # 源文件存放目录，功能模块及业务代码存放位置
log                 # log存放目录
README.txt          # readme文件

程序说明（实现功能）：
1、申请信用卡
密码存储：获取用户密码进行md5加密，将用户名的密码的md5值存储到文件

2、账号登录

3、额度管理
1）待完善，降低用户额度

4、提现功能
1）登录以后先获取用户信息，打印目前的账号信息
2）提示用户输入提现的金额，判断提现的额度是否大于等于提现的金额（提现费用为提现金额的%5），大于或者等于则进行提现操作
3）将账号的的用户额度-提现金额*2-提现费用*2  （为何*2 用户额度和取现额度的换算），将修改结果记录到文件
4）退出前大于提现后的账号信息

5、账单查询
1）已出账单
2）未出账单
3）分期申请
账单记录存储：用户消费、提现、还款记录
方法1：将信息存储到字典
'card_record':{
    '2016.01.01':{'record_type': 1,'record_sum':1000.0}
}

# record_type 1=提现 2=消费 3=还款

方法2：将消费记录单独存储到一个以用户名命名的目录下，每天一个文件进行存储

6、转账功能
1）显示用户现有的账号信息
2）提示用户输入要转账的账号，判断账号存在，继续转账操作
3）提示用户输入要转账的金额，判断现有取现额度大于转账金额+手续费金额，如果大于继续转账操作
4）将账号可以取现额度-转账金额-转账金额*0.05，被转账账号的账号余额增加被转账金额
5）将两个用户的被修改信息，利用pickel存回文件

7、还款功能
1）显示用户现有的账号信息，询问用户是否立即还款，用户确认后，接收用户要还款的金额，计算要恢复用户信用额度余额，增加用户额度
2）待还款的金额计算 待还款金额=用户额度-剩余用户额度-账号余额（暂时不考虑是否在账单本月账单内还是账单外）
3）用户退出前打印账户信息

8、ATM用户管理
1）审批用户申请，授权额度完成
2) 用户额度管理完成
3）冻结账号完成，但是登录验证时候出触发死循环

9、信用卡用户信息存储格式说明
式化JSON：
{
    "song": {
        "agree_flag": 1,
        "agree_register": 0,
        "email": "123@qq.com",
        "password": "123",
        "refund_date": "13",
        "phone_number": "123",
        "area_info": "beijing",
        "account_stat": 0,
        "card_limit_surplus": 12900,
        "card_limit": 20000,
        "account_name": "song",
        "bill_date": "25",
        "account_balance": 5000
    },
    "lin": {
        "agree_flag": 1,
        "agree_register": 0,
        "email": "123@qq.com",
        "password": "123",
        "refund_date": "13",
        "phone_number": "112",
        "area_info": "shanghai",
        "account_stat": 0,
        "card_limit_surplus": 50000,
        "card_limit": 60000,
        "account_name": "lin",
        "bill_date": "25",
        "account_balance": 5000
    },
    "admin": {
        "agree_flag": 0,            	# 信用卡审批状态 0 未审批 1 审批完成
        "agree_register": 0,        	# 信用卡审批结果 0 审批失败 1 审批成功
        "email": "admin@qq.com",
        "password": "202cb962ac59075b964b07152d234b70",      		# 管理员密码(md5加密过的)
        "refund_date": "13",
        "phone_number": 12432423423,
        "area_info": "北京",
        "account_stat": 0,         		# 0 账号正常使用 1 账号冻结
        "card_limit_surplus": 0,   		# 用户信用额度余额  用户取现额度余额=用户信用额度余额/2
        "card_limit": 0,           		# 用户信用额度，默认额度为0，审批通过然后进行额度授权  用户取现额度=用户信用额度余额/2
        "account_name": "admin",   		# 管理员账号
        "bill_date": "25",
        "account_balance": 0       		# 账户余额
    }
}



用到的知识点
函数、文件读写、pickel序列化，用户输入、while、for语句使用、颜色输出、列表、datetime\logging模块应用


测试环境说明（两个平台都能正常实现程序功能）：
Linux：
OS:Ubuntu 16.04 LTS
Python:Python 3.5.1+

Windows：
OS:Windows 7 旗舰版
Python:Python 3.5.0
PyCharm版本：PyCharm 2016.1.2

需要将相关程序及文件都传到测试环境
程序运行：
cd bin
python3 my_init.py

bug及优化方向
1）优化代码，在保证程序功能的前提下，增加重复代码的重用，减少代码量
2）注册时可以添加一个生成随机字符串的功能，确保站点不被恶意注册
3) 程序功能完善，分期管理

功能测试记录
测试账号使用：
商城：
用户：mds 密码：123（或者自己注册）

信用卡：
管理员权限     用户：admin 密码：123
普通用户权限   用户：sun  密码：123



