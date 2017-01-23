Name:SelectCourse
Auther: Kaye Gao
Blog:http://www.cnblogs.com/huamingao/
``
# Requirement
简单FTP，实现功能：
1. 用户登陆
2. 上传/下载文件
3. 不同用户家目录不同
4. 查看当前目录下文件
5. 充分使用面向对象知识

# 测试步骤
开启服务端: 运行NewFTP/server/bin/main.py
开启客户端： 运行client/bin/main.py
有两个初始用户kaye和leo，密码都是pwd
可以执行系统命令，并返回执行结果或错误提示
可以执行自定义命令update和download，命令格式为：
update 文件名
download 文件名

# 服务端程序结构:
server/
|-- bin 
|   |-- main.py  #程序执行文件
|-- conf 
|   |-- conf.py  #配置文件，包括所有中文字符
|-- db  #数据存储
|   |-- inventory  #服务端上的公共目录
|   |   |-- fileA   # 测试文件A
|   |   |-- fileB   # 测试文件B    
|   |-- user_home #用户家目录
|   |   |-- kaye  #用户kaye的家目录
|   |       |--fileA  #测试文件A
|   |   |-- leo  #用户leo的家目录
|   |-- user_obj #用户对象文件
|   |   |-- kaye  #用户kaye的对象文件
|   |   |-- leo  #用户leo的对象文件
|-- src #核心代码
    |-- user.py  # 服务端的User类定义
    |-- server.py  #socket服务端
    
# 客户端程序结构:
client/
|-- bin 
|   |-- main.py  #程序执行文件
|-- conf 
|   |-- conf.py  #配置文件，包括所有中文字符
|-- src #核心代码
    |-- user.py  # 客户端的User类定义

# 数据定义
User类
    字段：name,password
    静态方法：
    socket_client() 处理客户端与服务端的通信（客户端向服务端发送请求，接收服务端返回的数据）
    print_inventory_dir()  打印公共目录的绝对路径
    login()     用户登录
    register()   新用户注册
    动态方法：
    print_home_dir()    打印当前用户家目录的绝对路径
    run_cmd()   执行命令
    
server模块：
    list_inventory()   响应客户端查看公共目录的请求
    download()     响应客户端的下载请求
    upload()       响应客户端的上传请求
    handle_request()   分类客户端请求
    login()       响应客户端的登录请求
    register()    响应客户端的注册请求
    server_socket()     处理客户端与服务端的同学（接收客户端发来的请求，返回数据给客户端）
    run_cmd()   执行客户端传来的命令
    print_home_dir()    打印当前用户家目录的绝对路径
    print_inventory_dir()  打印公共目录的绝对路径
    overwrite_home_dir()   覆盖家目录中的文件
    overwrite_inventory_dir()   覆盖公共目录中的文件
    
# 功能释义
公共目录： NewFTP/server/db/inventory
用户家目录： NewFTP/server/db/user_home/<username>
上传，就是用户把自己家目录中的文件上传到公共目录
下载，就是用户把公共目录中的文件下载到自己的家目录
如果上传或下载中发现同名文件已存在，调用overwrite_XXX_dir函数，询问是否覆盖同名文件
