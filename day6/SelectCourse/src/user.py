#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Auther: Kaye Gao

import builtins
import datetime
import time
import pickle
import os
import sys
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(PROJECT_DIR,'db','students')
TEACHERS_DIR = os.path.join(PROJECT_DIR,'db','teachers')
COURSES_DIR = os.path.join(PROJECT_DIR,'db','courses')


from src import course as src_course


# User类的交互文字
FAIL_LOGIN = '登录失败，请重新尝试登录'
INPUT_ACCOUNT = '请输入登录账号：'
REGISTER_ACCOUNT = '请输入注册账号：'
INVALID_ACCOUNT = '您输入的账号不存在！注册账号？y/n'
INPUT_PWD = '请输入登录密码：'
INVALID_PWD = '您输入的密码有误，请重新输入！'
SUCCESS_LOGIN = '您已成功登录选课系统！'
COURSE_NAME = '请输入课程名称，以评价该课程老师：'
THANK_EVALUATE = '感谢你的评价！'
TEACHER_INFO = '{0}老师的当前资产为：{1}'
ACCOUNT_EXIST = '该账号名已被占用！请尝试输入其他账号名！'
USER_TYPE = """请输入要注册的用户类型
1. 学生
2. 老师
请输入编号："""

# Student类中的交互文字
STU_OPTIONS = '''
1. 选课
2. 签到
3. 查看已选课程
4. 查看上课记录
5. 评价老师
请输入编号进入相应操作，注销登录请输q：'''
SUCCESS_LOGOFF = '您已成功注销登录'
SET_PWD = '正在为您注册账号{0}，请设置登录密码:'
SET_USERNAME = '请输入您的名字：'
SET_SEX = '请输入您的性别：'
SET_AGE = '请输入您的年龄：'
SUCCESS_REGISTER = '恭喜您已成功注册！下面自动跳转到登录界面...'
INVALID_OPTION = '您输入的选项有误，请重新输入！'
COURSE_LIST = '编号\t课程名称\t上课时间\t课程老师\t老师评分\t课时费'
COURSE_INFO = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'
ADD_COURSE_NUM = '请输入您要选择的课程编号,退出请输q：'
ATTEND_COURSE_NUM = '请输入您要签到的课程编号，退出请输q:'
INVALID_COURSE = '您输入的课程编号不存在，请重新输入！'
INVALID_COURSE_NAME = '您的上课记录中没有该课程，请重新输入课程名称！'
SUCCESS_SELECT_COURSE = '您已成功选定课程：'
SUCCESS_ATTEND_COURSE = '您已成功签到以下课程：'
ATTEND_LIST = '编号\t课程名称\t上课时间\t课程老师\t课时费\t签到时间'
ATTEND_INFO = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'
EVA_OPTIONS = """请输入编号，以对{0}老师做出评价：
1. 满意
2. 一般
3. 不满意
"""
ALREADY_SELECT = '您已选过该课程！请重新输入'
NO_COURSE = '您尚未选课！'
NO_ATTEND_COURSE = '你尚无上课记录！'
NO_ATTEND_RECORD = '您尚未签到任何课程，无权对课程老师进行评价！'
SELECTED_TITLE = '以下是{0}课程表中的课程：'
COURSE_TITLE = '以下是所有可选课程：'
ATTEND_TITLE = '以下是{0}的上课记录：'
ALREADY_ATTEND = '您今天已经为该课程签过到了！自动跳转到上级目录...'


# Admin类中的交互文字
ADMIN_OPTIONS = '''
1. 创建老师
2. 创建课程
3. 查看学生信息
4. 查看老师信息
请输入编号进入相应操作，注销登录请输q：'''
SET_TEAC_ACCOUNT = '您正在为老师创建账号，请输入老师账号名：'
SET_TEAC_NAME = '请输入老师的姓名：'
SET_TEAC_PASSWORD = '请输入老师的登录密码：'
SET_TEAC_SEX = '请输入老师的性别：'
SET_TEAC_AGE = '请输入老师的年龄：'
SUCCESS_CREATE_TEA = '您已成功创建了上述老师！'
SET_COUR_NAME = '请输入课程名称：'
SET_COUR_TIME = '请输入上课时间：'
SET_COUR_FEE = '请输入课时费：'
INVALID_FEE = '课时费必须是数字，请重新输入'
SET_COUR_TEAC = '请输入上课老师：'
INVALID_TEACHER = '您输入的老师不存在！创建该老师？y/n:'
SUCCESS_CREATE_COUR = '您已成功创建了上述课程！'
STUDENT_ACCOUNT= '请输入要查询的学生账号：'
INVALID_STUDENT = '您输入的学生不存在！请重新输入；退出请输q'
FAIL_CREATE = '创建失败，请重新尝试'



# Teacher类中的交互文字
INPUT_TEACHER_ACCOUNT = '请输入老师的账号名：'
TEACHER_COURSE_LIST = '''以下是{0}老师要教的课程：
编号\t课程名称\t上课时间\t课时费'''
TEACHER_OPTIONS = """
1. 查看当前资产
2. 查看老师课表
继续请输入编号，退出请输q："""
TEACHER_NO_COURSE = '管理员尚未安排您要教的课程！'



class User:

    @staticmethod
    def login():
        """
        静态方法，登录
        :return:
        """
        # try:
        while True:
            account = input(INPUT_ACCOUNT)
            if account == 'q':
                exit()
            else:
                student_file = os.path.join(STUDENTS_DIR,account)
                teacher_file = os.path.join(TEACHERS_DIR,account)
                admin_file = os.path.join(PROJECT_DIR,'db',account)
                result = list(map(os.path.exists,(teacher_file,student_file,admin_file)))
                # 如果账账户文件存在，获取账号对象
                if any(result):
                    if result[0]:
                        user_obj = pickle.load(open(teacher_file, 'rb'))
                    elif result[1]:
                        user_obj = pickle.load(open(student_file, 'rb'))
                    elif result[2]:
                        user_obj = pickle.load(open(admin_file, 'rb'))
                    input_pwd = input(INPUT_PWD)
                    # 从文件读取user对象
                    if input_pwd != user_obj.password:
                        print(INVALID_PWD)
                        continue
                    else:
                        print(user_obj.account,SUCCESS_LOGIN)
                        user_obj.show_options()
                # 如果账号文件不存在，询问是否调转到注册界面
                else:
                    option = input(INVALID_ACCOUNT)
                    if option == 'y':
                        User.register_user()
                        continue
                    else:
                        continue
        # except:
        #     print(FAIL_LOGIN)

    @staticmethod
    def register_user():
        """
        新用户注册
        :param account:
        :return:
        """
        while True:
            account = input(REGISTER_ACCOUNT)
            if account == 'q':
                exit()
            else:
                teacher_file = os.path.join(TEACHERS_DIR,account)
                student_file = os.path.join(STUDENTS_DIR,account)
                admin_file = os.path.join(PROJECT_DIR,'db',account)
                # 如果账户存在，提示账户名已被占用
                result = list(map(os.path.exists,(teacher_file,student_file,admin_file)))
                if any(result):
                    option = input(ACCOUNT_EXIST)
                    continue
                # 如果账户不存在，注册产生账户文件
                else:
                    password = input(SET_PWD.format(account))
                    username = input(SET_USERNAME)
                    sex = input(SET_SEX)
                    age = input(SET_AGE)
                    type = input(USER_TYPE)
                    if type == '1':
                        student_obj = Student(account,password,username,sex,age)
                        pickle.dump(student_obj, open(student_obj.file, 'wb'))
                    elif type == '2':
                        teacher_obj = Teacher(account,password,username,age)
                        pickle.dump(teacher_obj, open(teacher_obj.file, 'wb'))
                    print(SUCCESS_REGISTER)
                    User.login()


class Student(User):

    def __init__(self,account=None,password=None,username=None,sex=None,age=None,course=[],attend_record={}):
        self.account = account
        self.password = password
        self.username = username
        self.sex = sex
        self.age = age
        self.course = course
        self.attend_record = attend_record
        self.file = os.path.join(STUDENTS_DIR,account)

    def show_options(self):
        """
        学生登录后菜单选项
        :return:
        """
        while True:
            option = input(STU_OPTIONS)
            if option == 'q':
                print(self.account, SUCCESS_LOGOFF)
                self.login()
            elif option == '1':
                self.add_course()
            elif option == '2':
                self.attend_course()
            elif option == '3':
                self.show_selected_course()
            elif option == '4':
                self.show_attend()
            elif option == '5':
                self.evaluate_teacher()
            else:
                print(INVALID_OPTION)

    @staticmethod
    def show_all_course():
        """
        显示所有可选课程
        :return:
        """
        print(COURSE_TITLE)
        print(COURSE_LIST)
        for i,course_name in enumerate(os.listdir(COURSES_DIR)):
            course_file = os.path.join(COURSES_DIR,course_name)
            course_obj = pickle.load(open(course_file,'rb'))
            print(COURSE_INFO.format(i+1,
                                     course_obj.name,
                                     course_obj.time,
                                     course_obj.teacher_obj.username,
                                     course_obj.teacher_obj.asset,
                                     course_obj.fee))

    def select_course(self,choice):
        """
        根据用户输入，获取课程对象
        :return:
        """
        while True:
            option = choice
            if option in ['q','']:
                self.show_options()
            elif not option.isdigit():
                print(INVALID_COURSE)
                return None
            # elif int(option) not in range(len(os.listdir(COURSES_DIR))+1):
            #     print(INVALID_COURSE)
            #     return None
            else:
                # 获取所选课程对象
                course_name = os.listdir(COURSES_DIR)[int(option)-1]
                course_file = os.path.join(COURSES_DIR, course_name)
                course_obj = pickle.load(open(course_file, 'rb'))
                return course_obj

    def add_course(self):
        """
        添加课程到课表
        :return:
        """
        while True:
            Student.show_all_course()
            option = input(ADD_COURSE_NUM)
            if option.isdigit:
                if int(option) not in range(len(os.listdir(COURSES_DIR))+1):
                    print(INVALID_COURSE)
                    continue
            course_obj = self.select_course(option)
            # 如果所选课程已在学生的当前课表中，打印已选过该课程，要求选课
            i = 0
            for course in self.course:
                if course_obj.name == course.name:
                    i = 1
                    print(ALREADY_SELECT)
                    break
            # 如果所选课程不在学生的当前课表中
            if i == 0:
                self.course.append(course_obj)
                pickle.dump(self,open(self.file,'wb'))
                # 打印签到成功
                print(SUCCESS_SELECT_COURSE,course_obj.name)
                return None

    def attend_course(self):
        """
        签到
        :return:
        """
        while True:
            self.show_selected_course()
            # 根据用户输入，获取课程对象
            option = input(ATTEND_COURSE_NUM)
            if option.isdigit:
                if int(option) not in range(len(self.course)+1):
                    print(INVALID_COURSE)
                    continue
            course_obj = self.select_course(option)
            # 如果返回None,
            if not course_obj:
                continue
            # 如果输入的课程已在签到记录中，检查是否已经有当天的签到记录
            i = 0
            for attend_course_obj in self.attend_record.keys():
                if attend_course_obj.name == course_obj.name:
                    if datetime.date.today() in self.attend_record.values():
                        print(ALREADY_ATTEND)
                        i == 1
                        return None
            if i == 0:
                # 加入课程到学生上课记录
                self.attend_record[course_obj] = datetime.date.today()
                pickle.dump(self,open(self.file,'wb'))
                # 老师收入课时费
                course_obj.teacher_obj.asset += course_obj.fee
                teacher_obj_file = os.path.join(TEACHERS_DIR,course_obj.teacher_obj.username)
                pickle.dump(course_obj.teacher_obj,open(teacher_obj_file,'wb'))
                course_obj_file = os.path.join(COURSES_DIR,course_obj.name)
                pickle.dump(course_obj, open(course_obj_file, 'wb'))
                # 打印签到成功
                print(SUCCESS_ATTEND_COURSE)
                print(COURSE_LIST)
                print(COURSE_INFO.format('',
                                         course_obj.name,
                                         course_obj.time,
                                         course_obj.teacher_obj.username,
                                         course_obj.teacher_obj.asset,
                                         course_obj.fee))
                return None

    def show_selected_course(self):
        """
        显示当前学生所选课程
        :return:
        """
        # 如果学生当前课程表为空，打印尚未选课
        if not self.course:
            print(NO_COURSE)
        else:
            print(SELECTED_TITLE.format(self.username))
            print(COURSE_LIST)
            for i,course_obj in enumerate(self.course):
                print(COURSE_INFO.format(i+1,
                                         course_obj.name,
                                         course_obj.time,
                                         course_obj.teacher_obj.username,
                                         course_obj.teacher_obj.asset,
                                         course_obj.fee))

    def show_attend(self):
        """
        显示当前学生上课记录（即，已签到的课程）
        :return:
        """
        # 如果学生当前课程表为空，打印尚未选课
        if not self.attend_record:
            print(NO_ATTEND_COURSE)
        else:
            print(ATTEND_TITLE.format(self.username))
            print(ATTEND_LIST)
            for i,course_obj in enumerate(self.attend_record):
                print(ATTEND_INFO.format(i+1,
                                         course_obj.name,
                                         course_obj.time,
                                         course_obj.teacher_obj.username,
                                         course_obj.fee,
                                         self.attend_record[course_obj]))

    def evaluate_teacher(self):
        """
        学生对老师评分
        :return:
        """
        # 如果没有签到记录，提示无法对老师作评价，自动跳转到签到界面
        if not self.attend_record:
            print(NO_ATTEND_RECORD)
        else:
            self.show_attend()
            while True:
                course_name = input(COURSE_NAME)
                if course_name == 'q':
                    return None
                else:
                    course_obj_file = os.path.join(COURSES_DIR, course_name)
                    if not os.path.exists(course_obj_file):
                        print(INVALID_COURSE_NAME)
                    else:
                        course_obj = pickle.load(open(course_obj_file,'rb'))
                        for attend_course_obj in self.attend_record.keys():
                            if attend_course_obj.name == course_obj.name:
                                while True:
                                    option = input(EVA_OPTIONS.format(course_obj.teacher_obj.username))
                                    # 学生给差评，老师收入减少50元
                                    if option == '3':
                                        course_obj.teacher_obj.asset -= 50
                                        teacher_obj_file = os.path.join(TEACHERS_DIR, course_obj.teacher_obj.account)
                                        pickle.dump(course_obj.teacher_obj, open(teacher_obj_file, 'wb'))
                                        course_obj_file = os.path.join(COURSES_DIR, course_obj.name)
                                        pickle.dump(course_obj, open(course_obj_file, 'wb'))
                                        print(THANK_EVALUATE)
                                        return None
                                    elif option in ['1','2']:
                                        print(THANK_EVALUATE)
                                        return None
                                    else:
                                        print(INVALID_OPTION)
                        print(INVALID_COURSE_NAME)



class Teacher(User):

    def __init__(self,account,password=None,username=None,sex=None,age=None,course=[],asset=0):
        self.account = account
        self.username = username
        self.password = password
        self.sex = sex
        self.age = age
        self.course = course
        self.asset = asset
        self.file = os.path.join(TEACHERS_DIR,account)

    def show_options(self):
        """
        老师功能选项
        :return:
        """
        while True:
            option = input(TEACHER_OPTIONS)
            if option == 'q':
                print(self.account,SUCCESS_LOGOFF)
                self.login()
            elif option == '1':
                self.show_asset()
            elif option == '2':
                self.show_course()
            else:
                print(INVALID_OPTION)

    def show_asset(self):
        teacher_obj = pickle.load(open(self.file,'rb'))
        print(TEACHER_INFO.format(teacher_obj.username,teacher_obj.asset))

    def show_course(self):
        teacher_obj = pickle.load(open(self.file,'rb'))
        if not teacher_obj.course:
            print(TEACHER_NO_COURSE)
        else:
            print(TEACHER_COURSE_LIST.format(teacher_obj.username))
            for i,course_obj in enumerate(teacher_obj.course):
                print(i+1,course_obj.name,course_obj.time,course_obj.fee)

class Admin(User):

    def __init__(self, account, password=None):
        self.account = account
        self.password = password
        self.file = os.path.join(STUDENTS_DIR,account)

    def show_options(self):
        """
        管理员登录后菜单选项
        :return:
        """
        while True:
            option = input(ADMIN_OPTIONS)
            if option == 'q':
                print(self.account,SUCCESS_LOGOFF)
                self.login()
            elif option == '1':
                self.create_teacher()
            elif option == '2':
                self.create_course()
            elif option == '3':
                Admin.show_student()
            elif option == '4':
                Admin.show_teacher()
            else:
                print(INVALID_OPTION)

    @staticmethod
    def create_teacher():
        """
        创建老师
        :return:
        """
        try:
            while True:
                account = input(SET_TEAC_ACCOUNT)
                if os.path.exists(os.path.join(TEACHERS_DIR,account)):
                    print('您要创建的账号名已存在，请重新输入！')
                else:
                    username = input(SET_TEAC_NAME)
                    password = input(SET_TEAC_PASSWORD)
                    age = input(SET_TEAC_AGE)
                    sex = input(SET_TEAC_SEX)
                    asset = 0
                    tea_obj = Teacher(account,password,username,age,sex,[],asset)
                    pickle.dump(tea_obj,open(tea_obj.file,'wb'))
                    print(SUCCESS_CREATE_TEA)
                    break
        except:
            print(FAIL_CREATE)

    @staticmethod
    def create_course():
        """
        创建课程
        :return:
        """
        try:
            name = input(SET_COUR_NAME)
            time = input(SET_COUR_TIME)
            while True:
                fee = input(SET_COUR_FEE)
                if not fee.isdigit():
                    print(INVALID_FEE)
                else:
                    fee = int(fee)
                    break
            while True:
                teacher = input(SET_COUR_TEAC)
                tea_file = os.path.join(TEACHERS_DIR,teacher)
                # 如果老师文件不存在，询问是否创建老师，输入y跳转到创建老师，输入其他则放弃创建课程
                if os.path.exists(tea_file):
                    break
                else:
                    option = input(INVALID_TEACHER)
                    if option == 'y':
                        Admin.create_teacher()
                        break
                    else:
                        continue
            tea_obj = pickle.load(open(tea_file,'rb'))
            # 老师对象关联到课程对象
            course_obj = src_course.Course(name,time,fee,tea_obj)
            pickle.dump(course_obj,open(course_obj.file,'wb'))
            # 课程对象关联到老师对象
            tea_obj.course.append(course_obj)
            pickle.dump(tea_obj,open(tea_file,'wb'))
            # 将更新过的老师对象关联到课程对象
            course_obj = src_course.Course(name,time,fee,tea_obj)
            pickle.dump(course_obj,open(course_obj.file,'wb'))
            print(SUCCESS_CREATE_COUR)
        except:
            print(FAIL_CREATE)

    @staticmethod
    def show_student():
        while True:
            stu_name = input(STUDENT_ACCOUNT)
            if stu_name in ['q','']:
                return None
            stu_obj_file = os.path.join(STUDENTS_DIR, stu_name)
            if not os.path.exists(stu_obj_file):
                print(INVALID_STUDENT)
            else:
                stu_obj = pickle.load(open(stu_obj_file, 'rb'))
                stu_obj.show_selected_course()
                stu_obj.show_attend()
                return None

    @staticmethod
    def show_teacher():
        while True:
            teacher_account = input(INPUT_TEACHER_ACCOUNT)
            teacher_obj_file = os.path.join(TEACHERS_DIR,teacher_account)
            if not os.path.exists(teacher_obj_file):
                option = input(INVALID_TEACHER)
                if option != 'y':
                    return None
                else:
                    Admin.create_teacher()
            else:
                teacher_obj = pickle.load(open(teacher_obj_file,'rb'))
                if not teacher_obj.course:
                    print(TEACHER_NO_COURSE)
                    break
                else:
                    print(TEACHER_INFO.format(teacher_obj.username,teacher_obj.asset))
                    print(TEACHER_COURSE_LIST.format(teacher_obj.account))
                    for i,course_obj in enumerate(teacher_obj.course):
                        print(i+1,course_obj.name,course_obj.time,course_obj.fee)
                    break


