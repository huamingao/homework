Name:multimenu
Auther: Kaye Gao
Blog:http://www.cnblogs.com/huamingao/

Requirement:
用户交互方式选择三级菜单

Function:
1. 数据存入多层嵌套的字典，最底层是一组列表
2. 创建函数msg(layer,option)，返回值是一个列表类型，留到主函数中打印。使用if语句对不同的layer层做不同处理
3. 以格式化字符串形式打印初始信息
4. 如果输入q，则退出程序；输入b，回退到上一层（其实现方法是，将option置为上一次执行函数时的option值，然后调用函数msg）;对于其他输入，默认认为是正确的输入，layer加1后循环下一次打印信息
