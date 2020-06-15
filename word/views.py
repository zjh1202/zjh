from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from .word_algorithm import *
import datetime
from django.http import HttpResponse


# Create your views here.


# def index(request):
#     if request.method == "GET":
#         return render(request, 'index.html')
#     else:
#         word_text = request.POST.get('word_text')
#         word_answer = request.POST.get('word_answer')
#
#     #验证是否为空
#     result = False
#     if word_text and word_answer:
#         result = True
#         s1 = word_text
#         s2 = word_answer
#         vec1, vec2 = get_word_vector(s1, s2)
#         word_text2 = cos_dist(vec1, vec2)
#     if result:
#         return render(request, "index.html", {"word_text": word_text2})

def index(request):
    pass
    return render(request, 'index.html')


def student_login(request):
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            job_number = login_form.cleaned_data['job_number']
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            test_number = login_form.cleaned_data['test_number']
            num = login_form.cleaned_data['num']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                        if user.number == job_number:
                            request.session['is_login'] = True
                            request.session['user_number'] = user.number
                            request.session['user_name'] = user.name
                            request.session['test_number'] = test_number
                            request.session['num'] = num
                            return redirect('/student/')
                        else:
                            message = "学号错误！"
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def teacher_login(request):
    if request.method == "POST":
        login_form = forms.TeacherUserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            job_number = login_form.cleaned_data.get('job_number')
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            num = login_form.cleaned_data.get('num')
            test_number = login_form.cleaned_data.get('test_number')
            try:
                user = models.TeacherUser.objects.get(Teacher_name=username)
                if user.password == password:
                    if user.Teacher_number == job_number:
                        request.session['is_login'] = True
                        request.session['user_number'] = user.Teacher_number
                        request.session['user_name'] = user.Teacher_name
                        request.session['num'] = num
                        request.session['test_number'] = test_number
                        return redirect('/teacher/')
                    else:
                        message = "学号错误！"
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'teacher_login.html', locals())

    login_form = forms.TeacherUserForm()
    return render(request, 'teacher_login.html', locals())


def register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            job_number = register_form.cleaned_data['job_number']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            school = register_form.cleaned_data['school']
            object = register_form.cleaned_data['object']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            same_number_user = models.User.objects.filter(number=job_number)
            if same_number_user:  # 学号/工号唯一
                message = '学号已经存在，请重新选择学号！'
                return render(request, 'register.html', locals())
            same_email_user = models.User.objects.filter(email=email)
            if same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(request, 'register.html', locals())
            # 当一切都OK的情况下，创建新用户
            number = datetime.datetime.now().year
            i = 0
            exam_num = "101"  # 设置考试号
            t_num = 100
            t_num_len = len(str(t_num))
            while i < t_num:
                teacher_num = str(i + 1).zfill(t_num_len)
                num = str(number) + exam_num + teacher_num
                b = models.User.objects.filter(num=num)
                if b:
                    i += 1
                else:
                    # 当一切都OK的情况下，创建新用户
                    new_user = models.User()
                    new_user.number = job_number
                    new_user.name = username
                    new_user.password = password1
                    new_user.email = email
                    new_user.school = school
                    new_user.object = object
                    new_user.num = num
                    new_user.save()
                    message = "您的做题的编号为：" + num + "，谨记该编号！请返回登录界面进行登录"
                    break
            # return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def teacher_register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return redirect("/index/")
    if request.method == "POST":
        register_form = forms.TeacherRegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            job_number = register_form.cleaned_data['job_number']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            school = register_form.cleaned_data['school']
            object = register_form.cleaned_data['object']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'teacher_register.html', locals())
            same_number_user = models.TeacherUser.objects.filter(Teacher_number=job_number)
            if same_number_user:  # 学号/工号唯一
                message = '学号已经存在，请重新选择学号！'
                return render(request, 'teacher_register.html', locals())
            same_email_user = models.TeacherUser.objects.filter(email=email)
            if same_email_user:  # 邮箱地址唯一
                message = '该邮箱地址已被注册，请使用别的邮箱！'
                return render(request, 'teacher_register.html', locals())

            number = datetime.datetime.now().year
            i = 0
            exam_num = "01"  # 设置考试号
            t_num = 100
            t_num_len = len(str(t_num))
            while i < t_num:
                teacher_num = str(i + 1).zfill(t_num_len)
                num = str(number) + exam_num + teacher_num
                b = models.TeacherUser.objects.filter(num=num)
                if b:
                    i += 1
                else:
                    # 当一切都OK的情况下，创建新用户
                    new_user = models.TeacherUser()
                    new_user.Teacher_number = job_number
                    new_user.Teacher_name = username
                    new_user.password = password1
                    new_user.email = email
                    new_user.school = school
                    new_user.object = object
                    new_user.num = num
                    new_user.save()
                    message = "您出题的编号为："+num +"，谨记该编号！请返回登录界面进行登录"
                    break
            # return redirect('/teacher_login/')  # 自动跳转到登录页面
    register_form = forms.TeacherRegisterForm()
    return render(request, 'teacher_register.html', locals())


def base(request):
    pass
    return render(request, 'base.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # flush会一次性清空session中所有内容，可以使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def teacher_logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/teacher_login/")
    request.session.flush()
    # flush会一次性清空session中所有内容，可以使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/teacher_login/")


def admin_logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/admin_login/")
    request.session.flush()
    # flush会一次性清空session中所有内容，可以使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/admin_login/")


def teacher(request):
    if request.method == "GET":
        test_number = request.session.get('test_number')
        same_test_number = models.WordAdmin.objects.get(test_number=test_number)
        text_number = same_test_number.text_number
        number = range(1, same_test_number.text_number + 1)

    if request.method == "POST":
        if forms.TeacherForm(request.POST):
            teacher_form = forms.TeacherForm(request.POST)
            display = True
            if teacher_form.is_valid():  # 获取数据
                test_number = request.session.get('test_number')
                same_test_number = models.WordAdmin.objects.get(test_number=test_number)
                text_number = same_test_number.text_number
                number = range(1, same_test_number.text_number+1)
                subject = same_test_number.subject
                text = request.POST.getlist('text')
                keyword = request.POST.getlist('keyword')
                text_answer = request.POST.getlist('text_answer')
                name = request.session.get('user_name')
                teacher_number = request.session.get('user_number')
                # same_text_order = models.Teacher.objects.filter(text_order=text_order)
                # same_name = models.Teacher.objects.filter(name=name)
                num = request.session.get('num')
                for i in range(text_number):
                    new_text = models.Teacher()
                    new_text.text_order = i+1
                    new_text.text = text[i]
                    new_text.keyword = keyword[i]
                    new_text.name = name
                    new_text.number = teacher_number
                    new_text.answer = text_answer[i]
                    new_text.num = num
                    new_text.subject = subject
                    new_text.test_number = test_number
                    new_text.save()
                    message = '题目提交成功！'
    teacher_form = forms.TeacherForm()
    return render(request, 'teacher.html', locals())


def student(request):
    if request.method == "GET":
        text = []
        text_order = []
        number = request.session.get('test_number')
        same_number = models.Teacher.objects.filter(test_number=number)
        count = models.Teacher.objects.filter(test_number=number).count()
        for i in range(count):
            if same_number:
                text.append(same_number[i].text)
                text_order.append(same_number[i].text_order)
                text_all = zip(text, text_order)

    if request.method == "POST":
        if forms.StForm(request.POST):
            st_form = forms.StForm(request.POST)
            text = []
            text_order = []
            number = request.session.get('test_number')
            same_number = models.Teacher.objects.filter(test_number=number)
            count = models.Teacher.objects.filter(test_number=number).count()

            for i in range(count):
                if same_number:
                    text.append(same_number[i].text)
                    text_order.append(same_number[i].text_order)
                    text_all = zip(text, text_order)

            if st_form.is_valid():
                student_answer = request.POST.getlist("answer")
                student_name = request.session.get('user_name')
                num = request.session.get('num')
                message = "提交成功"
                for i in range(count):
                    teacher_text = same_number[i].text
                    teacher_answer = same_number[i].answer
                    teacher_keywords = same_number[i].keyword
                    student_answers = student_answer[i]
                    grade = main(teacher_answer, teacher_keywords, student_answers)

                    new_text = models.Student()
                    new_text.name = student_name
                    new_text.answer = student_answer[i]
                    new_text.text_order = same_number[i].text_order
                    new_text.test_number = number
                    new_text.grade = grade
                    new_text.num = num
                    new_text.save()

    st_form = forms.StForm()
    return render(request, 'student.html', locals())


def student_result(request):
    if request.method == 'GET':
        test_number = []
        student_name = []
        student_answer = []
        student_grade = []
        word_test = []
        teacher_num = request.session.get('num')
        teacher_name = request.session.get('user_name')
        test_number = request.session.get('test_number')
        student_words = models.Student.objects.filter(test_number=test_number)
        num_count = models.Student.objects.filter(test_number=test_number).count()
        teacher_words = models.Teacher.objects.filter(num=teacher_num)
        for y in range(num_count):
            if teacher_words or student_words:
                word_test.append(student_words[y].test_number)
                student_name.append(student_words[y].name)
                student_answer.append(student_words[y].answer)
                student_grade.append(student_words[y].grade)

            result_all = zip(word_test, student_name, student_answer, student_grade)

        return render(request, 'result.html', locals())
    return render(request, 'result.html', locals())


def admin_login(request):
    if request.method == "POST":
        login_form = forms.AdminLogin(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                if password == "123456":
                    if username == "admin":
                        request.session['is_login'] = True
                        request.session['user_name'] = username
                        return redirect('/table/')
                    else:
                        message = "用户名错误"
                else:
                    message = "密码不正确！"
            except:
                message = "用户名和密码都不正确"
        return render(request, 'admin_login.html', locals())

    login_form = forms.AdminLogin()
    return render(request, 'admin_login.html', locals())


def table(request):
    if request.method == 'GET':
        test_number = []
        teacher_text = []
        teacher_name = []
        student_name = []
        student_answer = []
        student_grade = []
        word_test = []
        teacher_count = models.TeacherUser.objects.values_list('Teacher_number').count()
        teacher_all = models.TeacherUser.objects.values_list('Teacher_number', flat=True)
        student_count = models.User.objects.all().values_list('name').count()
        student_all = models.User.objects.values_list('name', flat=True)
        for i in range(teacher_count):
            teacher_number = teacher_all[i]
            teacher_words = models.Teacher.objects.filter(number=teacher_number)
            for y in range(student_count):
                student_test = student_all[y]
                student_words = models.Student.objects.filter(name=student_test)
                word_count = models.Student.objects.filter(name=student_test).count()
                for x in range(word_count):
                    word_test.append(student_words[x].test_number)
                    teacher_text.append(teacher_words[x].text)
                    teacher_name.append(teacher_words[x].name)
                    student_name.append(student_words[x].name)
                    student_answer.append(student_words[x].answer)
                    student_grade.append(student_words[x].grade)

        result_all = zip(word_test, teacher_name, student_name, teacher_text, student_answer, student_grade)
        return render(request, 'table.html', locals())
    return render(request, 'table.html', locals())


def teacher_table(request):
    if request.method == 'GET':
        test_number = []
        teacher_text = []
        teacher_name = []
        teacher_number = []
        teacher_num = []
        word_test = []
        test_count = models.WordAdmin.objects.all().values_list('test_number').count()
        test = models.WordAdmin.objects.values_list('test_number', flat=True)

        for i in range(test_count):
            test_number = test[i]
            word_count = models.Teacher.objects.filter(test_number=test_number).count()
            teacher_words = models.Teacher.objects.filter(test_number=test_number)
            if teacher_words:
                for x in range(word_count):
                    word_test.append(teacher_words[x].test_number)
                    teacher_number.append(teacher_words[x].number)
                    teacher_num.append(teacher_words[x].num)
                    teacher_name.append(teacher_words[x].name)
                    teacher_text.append(teacher_words[x].text)

            result_all = zip(word_test, teacher_number, teacher_num, teacher_name, teacher_text)

        return render(request, 'teacher_table.html', locals())
    return render(request, 'teacher_table.html', locals())


def student_table(request):
    if request.method == 'GET':
        test_number = []
        student_num = []
        student_name = []
        student_answer = []
        student_grade = []
        word_test = []
        test_count = models.WordAdmin.objects.all().values_list('test_number').count()
        test = models.WordAdmin.objects.values_list('test_number', flat=True)

        for i in range(test_count):
            test_number = test[i]
            student_words = models.Student.objects.filter(test_number=test_number)
            num_count = models.Student.objects.filter(test_number=test_number).count()
            for y in range(num_count):
                if student_words:
                    word_test.append(student_words[y].test_number)
                    student_num.append(student_words[y].num)
                    student_name.append(student_words[y].name)
                    student_answer.append(student_words[y].answer)
                    student_grade.append(student_words[y].grade)

                result_all = zip(word_test, student_num, student_name, student_answer, student_grade)

        return render(request, 'student_table.html', locals())
    return render(request, 'student_table.html', locals())


def submit(request):
    if request.method == "POST":
        submit_form = forms.Submit(request.POST)
        message = "请检查填写的内容！"
        if submit_form.is_valid():
            test_number = submit_form.cleaned_data['test_number']
            subject = submit_form.cleaned_data['subject']
            text_number = submit_form.cleaned_data['text_number']
            same_test_number = models.WordAdmin.objects.filter(test_number=test_number)
            if same_test_number:
                message = "该题号已存在"
            else:
                new_title = models.WordAdmin()
                new_title.test_number = test_number
                new_title.subject = subject
                new_title.text_number = text_number
                new_title.save()
                message = "添加成功"
    submit_form = forms.Submit()
    return render(request, 'submit.html', locals())

