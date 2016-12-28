Name:loginAPI
Auther: Kaye Gao
Blog:http://www.cnblogs.com/huamingao/

Function:

1.检查当前目录下是否有名为credential的文件，若没有就新建一个空的名为credential的文件，继续步骤2

2.用户输入用户名，判断用户是否存在于credential文件中，如果存在，flag置为1，如果不存在，直接进入步骤5

3.判断用户输入的密码是否与credential文件中相应密码一致，如果一致，则打印成功消息，退出程序；如果密码不一致，打印密码错误信息，计数器counter加1，并要求再次输入密码，直至counter=3

4.当counter=3时，打印账号被锁定，将credential文件中的counter值置为3，保存文件，退出程序

5.接步骤2，如果用户不存在于credential文件中，要求用户输入密码，counter置为0，将以上三项信息保存在credential文件中，文件内容格式如下。回到步骤2，要求用户输入用户名密码进行身份验证

username1:password1:counter1
username2:password2:counter2
username3:password3:counter3
