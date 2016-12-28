#作者信息：

# @Author  : 陈益波
# @blog: http://www.cnblogs.com/willpower-chen/


实现功能：ATM + 购物商城程序
    1、额度 15000或自定义
    2、实现购物商城，买东西加入 购物车，调用信用卡接口结账
    3、可以提现，手续费5%
    4、每月22号出账单，每月10号为还款日，过期未还，按欠款总额 万分之5 每日计息
    5、支持多账户登录
    6、支持账户间转账
    7、记录每月日常消费流水
    8、提供还款接口
    9、ATM记录操作日志
    10、提供管理接口，包括添加账户、用户额度，冻结账户等。。。

程序结构：
.
├── shopping.py               #=> 商城主程序
├── atm_admin.py              #=> ATM后台程序
├── atm_daily.py              #=> ATM每日定时任务程序
├── atm_main.py               #=> ATM主程序
├── conf.py                   #=> 配置文件
├── dbs                       #=> 数据目录
│   ├── account.db            #=> ATM账户数据
│   ├── customer.db           #=> 商城用户数据
│   ├── goods.db              #=> 商城商品数据
│   └── __init__.py
├── libs                       #=> 库目录
│   ├── __init__.py
│   └── mylib.py              #=> 自定义库文件
├── log                       #=> 日志目录
│   ├── atm.log               #=> ATM日志
│   └── shopping.log          #=> 购物日志
├── model                     #=> 模块目录
│   ├── account.py
│   ├── atm.py
│   ├── customer.py
│   ├── goods.py
│   ├── __init__.py
│   └── shopping.py
└── README.md


程序配置：
    配置文件conf.py
    # 全局
    MAX_PER_PAGE = 5    #=> 分页，表示每一页最多显示多少项

    # 银行相关
    ATM_LOG = 'log/atm.log'     #=> ATM日志文件
    ACCOUNT_FILE = 'dbs/account.db'      #=> 账户数据文件
    MAX_BALANCE = 15000.0       #=> 默认可用额度
    DEFAULT_PASSWORD = '123.com'     #=> 默认账户密码
    MAX_ERROR_COUNT = 3     #=> 银行密码输入错误计数器阀值，达到这个值将会被锁定
    ADMIN_USER = 'admin'     #=> 银行后台密码
    ADMIN_PASSWORD = 'cbff36039c3d0212b3e34c23dcde1456'    #=> 银行后台密码

    # 银行每日任务相关
    BILL_DAY = 22     #=> 账单日
    REPAYMENT_DAY = 10     #=> 还款日


    # 商城相关
    CUSTOMER_FILE = 'dbs/customer.db'    #=> 用户数据文件
    GOODS_FILE = 'dbs/goods.db'    #=> 商品数据文件
    SHOPPING_LOG = 'log/shopping.log'    #=> 商城日志文件


运行环境：Python3.0或以上版本并配置好环境变量（linux主机为了和自带的python2.x版本不冲突，需将python3.X的可执行文件重名为python3或创建名为python3的软链接链接到python的可知文件）

执行方法：
    Linux：直接执行# python3 myEval.py或#./myEval.py（需要给主程序文件添加可执行权限）

