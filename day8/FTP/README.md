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
先运行src目录下的server.py，服务端开始监听。然后运行bin目录下的main.py
没有初始用户，请先注册进行新用户注册，然后登录进行操作

# 程序结构:
FTP/
|-- README.md
|-- bin #程序执行文件
|   |-- main.py
|-- db  #数据存储
|   |-- client  #客户端
|   |   |-- home  #所有用户的家目录
|   |       |-- kaye #用户kaye的家目录
|   |       |-- leo  #用户leo的家目录
|   |-- server #服务端
|       |-- inventory #服务端上的公共目录
|       |-- log  #所有用户在服务端的操作日志
|       |-- users  #存储服务端上所有用户的对象文件
|           |-- kaye  #用户kaye的对象文件
|           |-- leo  #用户leo的对象文件
|-- lib #通用模块
|   |-- login.py  # 登录/注册模块
|   |-- logger.py  #日志模块
|-- src #核心代码
    |-- user.py  # User类定义
    |-- server.py  #socket服务端


# 数据定义
User类
    字段：name,password,hmdir,log
    静态方法：
    socket_client() 处理客户端与服务端的通信（客户端向服务端发送请求，接收服务端返回的数据）
    list_inventory()列出服务端公共目录中的文件
    check_client()  下载时，检查客户端家目录中是否存在同名文件
    check_server()  上传时，检查服务端公共目录中是否存在同名文件
    动态方法：
    show_options()  获取用户输入的菜单选项
    list_hmdir()    列出当前用户家目录中的文件
    upload()        上传，用户把自己家目录中的文件上传到公共目录（FTP/db/server/inventory）
    download()      下载，用户把公共目录中的文件下载到自己的家目录（FTP/db/client/home/username/）
    logoff()        注销登录，返回欢迎界面
    write_log()     写日志，记录所有用户的登录、注销、上传、下载操作到日志文件log中
    show_log()      打印日志文件中的内容

# 模块
login模块：处理用户登录，若用户不存在，则注册新用户
logger模块：写日志到指定的日志文件
server模块：
    main()      服务端监听
    resp_list_inventory()   服务端响应客户端查看公共目录的请求
    resp_download()     服务端响应客户端的下载请求
    resp_upload()       服务端响应客户端的上传请求
    resp_logoff()       服务端响应客户端的注销请求
    resp_check_server() 服务端响应客户端
    handle_request()    服务端处理客户端请求

# 功能释义
目录FTP/db/server，代表服务端，存储服务端数据：包括公共目录（FTP/db/server/inventory）、用户对象文件、用户操作日志
目录FTP/db/client，代表客户端，存储客户端数据，即用户家目录及其中的文件
上传，就是用户把自己家目录中的文件上传到公共目录（FTP/db/server/inventory）
下载，就是用户把公共目录中的文件下载到自己的家目录（FTP/db/client/home/username/）
日志文件log会记录所有用户的登录、注销、上传、下载操作
