作者:cc
版本:v0.1
1.博客地址：http://www.cnblogs.com/cocc/p/5770642.html
2.程序介绍:
    实现ATM+购物车常用功能
    功能全部用python的基础知识实现,用到了time\os\sys\json\open\logging\函数\模块知识, 主要练习一个简单的模块化编程

    注意:只实现了ATM系统下管理员模式（用户名cc，密码123456）的冻结账户、额度调整、添加账户、解锁账户；
    用户模式（用户名tt,密码123456）下的额度查询、账单查询和还款；

程序结构:
atm/
├── README
├──  #A主程目录
│   ├── __init__.py
│   ├── bin #程序执行文件 目录
│   │   ├── __init__.py
│   │   ├── apply.py  #程序执行程序
│   ├── conf #配置文件
│   │   ├── __init__.py
│   ├── core #主要程序逻辑都 在这个目录 里
│   │   ├── __init__.py
│   │   ├── atm.py  #atm程序入口
│   │   ├── auth.py    #用户认证模块--未实现
│   │   ├── login.py   #登录--未实现
│   │   ├── main.py    #主逻辑交互程序
│   │   ├── manager.py  #管理员程序
│   │   ├── public.py   #公共模块
│   │   ├── shoppingmall.py   购物程序
│   │   └── user.py  #atm用户模块
│   ├── db  #用户数据存储的地方
│   │   ├── __init__.py
│   │   ├── bill.json#记录账单信息
│   │   ├── user.json#记录用户信息
│   │   ├── user_status.txt#记录登录信息--未实现
│   └── log #日志目录
│       ├── __init__.py
│       ├── access.log #用户访问和操作的相关日志--未实现
│       └── atm.log    #所有的ATM日志
└── shopping_mall #电子商城程序,需单独实现
    └── __init__.py