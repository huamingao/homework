# 那些年被我坑过的Python———山外有山（第四天）

分类： 编程、Python3.5.x、代码解析、博客分享

---

## 作业一：博客：
[那些年被我坑过的Python——山外有山（第四章）][1]
------
## 作业二：银行ATM+银行后台管理+购物商城
### 结构说明
> 项目由五个目录构成：
ATM
|--bin
|--core
|--conf
|--data
|--logs

------

> bin -----应用程序
core-----模块接口
conf-----全局配置
data-----数据文件
logs-----日志文件


------

> bin目录包含
atm.py
mgmt.py
shopping.py
三个应用程序，分别对应银行ATM、银行后台管理、购物商城
1、ATM实现了：提现、转账、还款、余额查询、历史记录功能；
2、银行后台管理实现了：创建账户、冻结/解冻、更改额度、查看流水、查看历史操作、显示账户信息功能；
3、购物商城实现了：最简单的显示商品、添加到购物车、显示购物车、调用银行转账接口的支付接口。

------

> core目录包含：
bank.py
shopping.py
分别存放了银行和购物的相关模块用于应用程序的调用
其中bank.py中包含两个装饰器，三个装饰器，分别给相应函数增加了，认证功能、检测冻结功能和写操作日志的功能：
@auth
@checkFreeze
@writeJournal
其他19个接口分别是：
addAccount()
addAuth()
delAccount()
checkFreezeStatus()
freeze()
unFreeze()
setLimit()
transferAccounts()
showAccounts()
checkAuth()
checkCreditAmount()
withdraw()
repayment()
checkAccountExist()
addJournal()
showJournalByAccount()
showAllJournal()
showManipulate()
showBalanceByAccount()

> shopping.py模块调用了atm的auth装饰器实现认证
@atm.auth
主要提供了4个接口：
showList()
showCart()
loadData()
payment()

------

> data目录主要存放数据文件：
account.txt
auth.txt
production.txt
分别是账户信息、认证信息和商品信息

------
> logs目录用于流水、日志的存放：
journal.log
mgmt.log
分别是用户流水信息和后台管理操作日志

------
> conf目录的功能是记录全局配置信息
这里没有具体实现，本来想存放默认额度和购物商城账号

------
### 使用说明：
> atm、mgmt、shopping三个应用程序相对独立
1、atm认证须知:
`账号的格式：0001、0002...`
`密码全为123456`

> 2、mgmt认证须知:
`管理员账号:admin`
`管理员密码：123`

> 3、shopping认证须知:
`认证方式与atm相同，都采用统一的银行账号密码认证`

> 具体运行时请参照程序流程图即可,更多详细功能不再赘述，时间紧任务重，有一些功能实现的不那么完善请多多谅解。


  [1]: http://www.cnblogs.com/tntxyz/p/5785564.html