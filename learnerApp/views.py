from datetime import timezone
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.contrib.auth import decorators
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import JsonResponse,Http404, response
from django.forms.models import model_to_dict
from django.conf import settings
from .models import *
from .forms import *
import json
import random
import string
from io import BytesIO
from django.core.files import File
from html2image import Html2Image
from PIL import Image
from uuid import uuid1
from django.template.defaulttags import register, regroup
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
    # print(request.user.user_email)
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request,'learnerApp/home.html')

# @csrf_exempt
# def login(request):
#     if request.user.is_authenticated :
#         return redirect('dashboard')
#     else:
#         if(request.method == 'POST'):
#             user_data = json.loads(request.body)
#             print(user_data)
#             user = authenticate(username=user_data['username'],password=user_data['password'])
#             if user is None:
#                 return JsonResponse({'message':"Invalid Email or Password"},status="500")
#             else:
#                 auth_login(request,user)
#                 # return JsonResponse({'message':"success"})
#                 return redirect('dashboard')
#         else:
#             return render(request,'learnerApp/login.html')

@csrf_exempt
def login(request):
    if request.user.is_authenticated :
        return redirect('dashboard')
    else:
        if(request.method == 'POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(user_data)
            user = authenticate(username=username,password=password)
            if user is None:
                return JsonResponse({'message':"Invalid Email or Password"},status="500")
            else:
                auth_login(request,user)
                # return JsonResponse({'message':"success"})
                return redirect('dashboard')
        else:
            return render(request,'learnerApp/login_new.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def get_random_string():
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(8))
    return result_str

def allUser(request):
    # print(CustomUser.objects.all())
    # print("institutes")
    # print(Institute.objects.all())
    for i in CustomUser.objects.all():
        print(model_to_dict(i))
    # print(model_to_dict(Student.objects.get(user=CustomUser.objects.get(user_email="swati@gmail.com"))))
    # print(Student.objects.get(user=CustomUser.objects.get(user_email="swati@gmail.com")).institute)
    return render(request,'learnerApp/adminDashboard.html')

def adminDashboard(request):
    try:
        instituteList = Institute.objects.all()
        return render(request,'learnerApp/adminDashboard.html',context={'user':request.user,'instituteList':instituteList})
    except:
        return redirect('createAdmin')
def instituteDashboard(request):
    facultyList = Faculty.objects.filter(institute= Institute.objects.get(user=request.user))
    return render(request,'learnerApp/instituteDashboard.html',context={'user':request.user,'facultyList':facultyList})

def facultyDashboard(request):
    # return render(request,'learnerApp/facultyDashboard.html',context={'user':request.user})
    return studentList(request)

def studentDashboard(request):
    return redirect('classroomList')

# @login_required(login_url="/login/")
def dashboard(request):
    # print(request.user.is_authenticated)
    if request.user.is_admin:
        return adminDashboard(request)
    elif request.user.is_institute:
        return instituteDashboard(request)
    elif request.user.is_faculty:
        return facultyDashboard(request)
    elif request.user.is_student:
        return studentDashboard(request)
    else:
        raise Http404("User role does not exist")

@login_required(login_url="/login/")
def profile(request):
    if request.method == 'POST':
        form = None
        if request.user.is_admin:
            form = AdminForm(request.POST,request.FILES,instance=Admin.objects.get(user=request.user))
        elif request.user.is_institute:
            form = InstituteForm(request.POST,request.FILES,instance=Institute.objects.get(user=request.user))
        elif request.user.is_faculty:
            form = FacultyForm(request.POST,request.FILES,instance=Faculty.objects.get(user=request.user))
        elif request.user.is_student:
            form = StudentForm(request.POST,request.FILES,instance=Student.objects.get(user=request.user))
        else:
            raise Http404("User role does not exist")   
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('dashboard')  
    else:
        form = None
        if request.user.is_admin:
            instance = Admin.objects.get(user=request.user)
            form = AdminForm(instance=instance)
        elif request.user.is_institute:
            instance = Institute.objects.get(user=request.user)
            form = InstituteForm(instance=instance)
        elif request.user.is_faculty:
            instance = Faculty.objects.get(user=request.user)
            form = FacultyForm(instance=instance)
        elif request.user.is_student:
            instance = Student.objects.get(user=request.user)
            form = StudentForm(instance=instance)
        extemp = getBasetemp(request)
        image = instance.user_image.url
        return render(request,'learnerApp/profile.html',context={'user':request.user,'image':image,'form':form,'extemp':extemp})
    
def getBasetemp(request):
    if request.user.is_admin:
        extemp = "learnerApp/adminDashboard.html"
    elif request.user.is_institute:
        extemp = "learnerApp/instituteDashboard.html"
    elif request.user.is_faculty:
        extemp = "learnerApp/facultyDashboard.html"
    elif request.user.is_student:
        extemp = "learnerApp/studentDashboard.html"
    return extemp

@login_required(login_url="/login/")
def addInstitute(request):
    if request.method == "POST":
        password = get_random_string()
        user  = CustomUser.objects.create_user(user_email=request.POST.get('user_email'),role="institute",password=password)
        user.save()
        institute_name = request.POST.get('institute_name')
        obj = Institute.objects.create(user=user,institute_name=institute_name,institute_address=request.POST.get('institute_address'),institute_id=request.POST.get('institute_id'))
        sendPass(institute_name,user.user_email,password)
        createImage(request.POST.get('institute_name'))
        im = Image.open(settings.MEDIA_ROOT+'/learnerApp/images/test.png')
        blob = BytesIO()
        im.save(blob,'PNG')
        blob.seek(0)
        name = str(uuid1())+'.png'
        imfile = File(blob,name=name)
        obj.user_image.save(name,imfile,save=True)
        obj.save()
        return redirect('dashboard')
    else:
        extraFields = [
            {
                'label':"Institute Name",
                'name':'institute_name',
                'type':'text'
            },
            {
                'label':"Institute Id",
                'name':'institute_id',
                'type':'number'
            },
            {
                'label':"Institute Address",
                'name':'institute_address',
                'type':'text'
            },
            {
                'label':"Institute Number",
                'name':'institute_number',
                'type':'number'
            }
        ]
        extemp = getBasetemp(request)
        return render(request,'learnerApp/addUser.html',context={'extraFields':extraFields,'extemp':extemp})

@login_required(login_url="/login/")
def addFaculty(request):
    if request.method == "POST":
        password = get_random_string()
        user  = CustomUser.objects.create_user(user_email=request.POST.get('user_email'),role="faculty",password=password)
        user.save()
        institute = Institute.objects.get(user=request.user)
        faculty_id = request.POST.get('faculty_id')
        faculty_number = request.POST.get('faculty_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        obj = Faculty.objects.create(user=user,faculty_id=faculty_id,faculty_number=faculty_number,first_name=first_name,last_name=last_name,institute=institute)
        last_name = request.POST.get('last_name') if request.POST.get('last_name') else ""
        sendPass(request.POST.get('first_name')+" "+ last_name,request.POST.get('user_email'),password)
        createImage(request.POST.get('first_name')+" "+ last_name)
        im = Image.open(settings.MEDIA_ROOT+'/learnerApp/images/test.png')
        blob = BytesIO()
        im.save(blob,'PNG')
        blob.seek(0)
        name = str(uuid1())+'.png'
        imfile = File(blob,name=name)
        obj.user_image.save(name,imfile,save=True)
        obj.save()
        return redirect('dashboard')
    else:
        extraFields = [
            {
                'label':"First Name",
                'name':'first_name',
                'type':'text'
            },
            {
                'label':"Last Name",
                'name':'last_name',
                'type':'text'
            },
            {
                'label':"Faculty Id",
                'name':'faculty_id',
                'type':'text'
            },
            {
                'label':"Faculty Number",
                'name':'faculty_number',
                'type':'number'
            }
        ]
        extemp = getBasetemp(request)
        return render(request,'learnerApp/addUser.html',context={'extraFields':extraFields,'extemp':extemp})

@login_required(login_url="/login/")
def studentList(request):
    if request.user.is_institute:
        studentList = Student.objects.filter(institute= Institute.objects.get(user=request.user))
    elif request.user.is_faculty:
        studentList = Student.objects.filter(institute=Faculty.objects.get(user=request.user).institute)
    extemp = getBasetemp(request)
    return render(request,'learnerApp/studentList.html',context={'user':request.user,'studentList':studentList,'extemp':extemp})

@login_required(login_url="/login/")
def classroomList(request):
    if request.user.is_faculty:
        classroomList = Classroom.objects.filter(faculty=Faculty.objects.get(user=request.user))
    elif request.user.is_student:
        classroomList = Student.objects.get(user=request.user).classrooms.all()
    extemp = getBasetemp(request)
    return render(request,'learnerApp/classroomList.html',context={'user':request.user,'classroomList':classroomList,'extemp':extemp})

@login_required(login_url="/login/")
def addClassroom(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        faculty = Faculty.objects.get(user=request.user)
        createImage(title)
        im = Image.open(settings.MEDIA_ROOT+'/learnerApp/images/test.png')
        blob = BytesIO()
        im.save(blob,'PNG')
        blob.seek(0)
        name = str(uuid1())+'.png'
        imfile = File(blob,name=name)
        obj = Classroom.objects.create(faculty=faculty,title=title)
        obj.classroom_image.save(name,imfile,save=True)
        obj.save()
        return redirect('classroom',obj.classroom_id)
    else:
        return render(request, 'learnerApp/addClassroom.html')

@login_required(login_url="/login/")
def addStudent(request):
    if request.method == "POST":
        password = get_random_string()
        user  = CustomUser.objects.create_user(user_email=request.POST.get('user_email'),role="student",password=password)
        user.save()
        if request.user.is_institute:
            institute = Institute.objects.get(user=request.user)
        elif request.user.is_faculty:
            institute = Faculty.objects.get(user=request.user).institute
        else:
            raise Http404("User does not have permission to add student")
        student_id = request.POST.get('student_id')
        student_number = request.POST.get('student_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        obj = Student.objects.create(user=user,first_name=first_name,last_name=last_name,student_id=student_id,student_number=student_number,institute=institute)
        last = request.POST.get('last_name') if request.POST.get('last_name') else ""
        createImage(first_name+" "+ last)
        sendPass(first_name+" "+ last,user.user_email,password)
        im = Image.open(settings.MEDIA_ROOT+'/learnerApp/images/test.png')
        blob = BytesIO()
        im.save(blob,'PNG')
        blob.seek(0)
        name = str(uuid1())+'.png'
        imfile = File(blob,name=name)
        obj.user_image.save(name,imfile,save=True)
        obj.save()
        return redirect('studentList')
    else:
        extraFields = [
            {
                'label':"First Name",
                'name':'first_name',
                'type':'text'
            },
            {
                'label':"Last Name",
                'name':'last_name',
                'type':'text'
            },
            {
                'label':"Student Id",
                'name':'student_id',
                'type':'text'
            },
            {
                'label':"Student Number",
                'name':'student_number',
                'type':'number'
            }
        ]
        extemp = getBasetemp(request)
        return render(request,'learnerApp/addUser.html',context={'extraFields':extraFields,'extemp':extemp})

def createImage(title):
    lis = title.strip().split(" ")
    if len(lis) == 1:
        initials = lis[0][:2]
    else:
        initials = lis[0][0] + lis[1][0]
    html ="""<html>
    <head></head>
    <body><p>{initials}</p></body>
    </html>"""
    html = html.format(initials=initials)
    css = """
        *{
            width:100vh;
            height100vh;
            margin:0;
        }
        p{background-color:	#c12929;
        width:100%;
        height:60%;
        padding:20% 0;
        font-family: 'Calibri', sans-serif;
        color:white;
        text-align:center;
        line-height:100%;
        font-size:20em;
        }
        """
    hti = Html2Image(output_path=settings.MEDIA_ROOT+'/learnerApp/images/')
    hti.screenshot(html_str=html, css_str=css, save_as='test.png',size=(5000,5000))
    return None

def classFeedView(request,id):
    try:
        classroom = Classroom.objects.get(pk=id)    
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    if request.method == 'POST':
        sender = request.user
        message = request.POST.get('message')
        if(len(message)>0):
            ClassFeedMessage.objects.create(classroom=classroom,sender=sender,message=message)
        return redirect('classFeed',id)

    messages = ClassFeedMessage.objects.filter(classroom=classroom).order_by('timestamp')
    print(messages)
    return render(request,'learnerApp/classFeed.html',context={'id':id,'extemp':extemp,'classroom':classroom,'messages':messages})

def classTestsView(request,id):
    try:
        classroom = Classroom.objects.get(pk=id)    
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    if request.user.is_faculty:
        tests = Test.objects.filter(classroom = classroom)
        responses = None
    elif request.user.is_student:
        tests = Test.objects.filter(classroom=classroom, start_time__lte = timezone.localtime(timezone.now()), end_time__gte = timezone.localtime(timezone.now()), published = True).exclude(test_id__in=TestResponse.objects.filter(student = Student.objects.get(user=request.user)).values_list('test').values_list('test_id'))
        responses = TestResponse.objects.filter(student = Student.objects.get(user = request.user))
    return render(request,'learnerApp/classTests.html',context={'id':id,'extemp':extemp,'classroom':classroom,'tests':tests,'responses':responses})

def testAttend(request,id,tid):
    extemp = getBasetemp(request)
    try:
        classroom = Classroom.objects.get(pk=id)
        test = Test.objects.get(test_id = tid)
        questions = TestQuestion.objects.filter(test=test)    
    except:
        return redirect('dashboard')
    if request.method == 'POST':
        testResponse = TestResponse.objects.create(test=test,student = Student.objects.get(user = request.user))
        testResponse.save()
        for question in questions:
            answer = request.POST.get(str(question.question_id))
            is_correct = answer == question.correct
            TestQuestionResponse.objects.create(response=testResponse,question = question,option = answer,is_correct = is_correct)
        return redirect('classTests',id)
    else:
        questions = TestQuestion.objects.filter(test=test)
        return render(request,'learnerApp/testAttend.html',context={'extemp':extemp,'id':id,'test':test,'classroom':classroom,'questions':questions})

def viewResponse(request,id,tid,rid):
    try:
        classroom = Classroom.objects.get(classroom_id=id)
        test = Test.objects.get(test_id = tid)
        response = TestResponse.objects.get(response_id = rid)
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    answers = TestQuestionResponse.objects.filter(response=response)
    return render(request,'learnerApp/viewResponse.html',context={'id':id,'tid':tid,'extemp':extemp,'classroom':classroom,'test':test,'response':response,'answers':answers})

def classMaterialView(request,id):
    try:
        classroom = Classroom.objects.get(pk=id)    
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    materials = ClassMaterial.objects.filter(classroom=classroom)
    print(materials)
    return render(request,'learnerApp/classMaterial.html',context={'id':id,'extemp':extemp,'classroom':classroom,'materials':materials})

def classMembersView(request,id):
    try:
        classroom = Classroom.objects.get(pk=id)
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(user_email=request.POST.get('user_email'))
            faculty = Faculty.objects.get(user=request.user)
            student = Student.objects.get(user=user,institute=faculty.institute)
            classroom.students.add(student)
            classroom.save()
            return redirect('classMembers',id)
        except:
            return render(request,'learnerApp/classMembers.html',context={'id':id,'extemp':extemp,'classroom':classroom,'error':"Entered Email ID is Incorrect"})
    print(classroom.students.all())
    return render(request,'learnerApp/classMembers.html',context={'id':id,'extemp':extemp,'classroom':classroom,'students':classroom.students.all()})

def classFacultyTransfer(request,id):
    try:
        classroom = Classroom.objects.get(pk=id)
        presentFaculty = Faculty.objects.get(user=request.user)
    except:
        return redirect('dashboard')
    try:
        newFaculty = request.POST.get('user_email')
        userInst = CustomUser.objects.get(user_email=newFaculty)
        faculty = Faculty.objects.get(user = userInst)
        classroom.faculty = faculty
        classroom.save()
        return redirect('classroomList')
    except:
        return redirect('classMembers',id=id)
    return redirect('dashboard')

def classCallView(request,id):
    try:
        classroom = Classroom.objects.get(pk=id)
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    if request.user.is_faculty:
        user = Faculty.objects.get(user=request.user)
    else:
        user = Student.objects.get(user=request.user)
    return render(request,'learnerApp/videoCall.html',context={'id':id,'extemp':extemp,'classroom':classroom,'meet':json.dumps({'data':classroom.classroom_id,'email':request.user.user_email,'name':user.first_name + user.last_name})})

def classAddMaterial(request,id):
    extemp = getBasetemp(request)
    if request.method == 'POST':
        classroom = Classroom.objects.get(classroom_id=id)
        title = request.POST.get('title')
        material = request.FILES.get('material')
        print(material)
        print(request.FILES)
        classMaterial = ClassMaterial.objects.create(title=title,classroom=classroom)
        classMaterial.material.save(str(uuid1()) +'.'+ material.name.split('.')[-1],material)
        return redirect('classMaterial',id)
    else:
        return render(request,'learnerApp/addClassMaterial.html',context={'extemp':extemp})

def clearMaterial(request):
    ClassMaterial.objects.all().delete()
    redirect('dashboard')

def classMaterialDiscussion(request,id,mid):
    try:
        material = ClassMaterial.objects.get(material_id=mid)
        classroom = Classroom.objects.get(pk=id)
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    if request.method == 'POST':
        sender = request.user
        message = request.POST.get('message')
        if(len(message)>0):
            ClassMaterialMessage.objects.create(material=material,sender=sender,message=message)
        return redirect('classMaterialDiscussion',id,mid)

    messages = ClassMaterialMessage.objects.filter(material=material).order_by('timestamp')
    print(messages)
    return render(request,'learnerApp/classMaterialDiscussion.html',context={'id':id,'extemp':extemp,'messages':messages,'material':material,'classroom':classroom})

def addClassTest(request,id):
    extemp = getBasetemp(request)
    classroom = Classroom.objects.get(classroom_id=id)
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.classroom = classroom
            test.save()
            return redirect('classTestManage',id,test.test_id)
        else:
            return render(request,'learnerApp/addClassTest.html',context={'extemp':extemp,'form':form})    
    else:
        form = TestForm()
        return render(request,'learnerApp/addClassTest.html',context={'id':id,'classroom':classroom,'extemp':extemp,'form':form})

def classTestManage(request,id,tid):
    try:
        classroom = Classroom.objects.get(classroom_id=id)
        if not Faculty.objects.get(user=request.user) == classroom.faculty:
            return redirect('dashboard')
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    test = Test.objects.get(test_id = tid)
    questions = TestQuestion.objects.filter(test=test)
    responses = TestResponse.objects.filter(test=test)
    return render(request,'learnerApp/classTestManage.html',context={'id':id,'tid':tid,'extemp':extemp,'classroom':classroom,'test':test,'questions':questions,'responses':responses})

def togglePublish(request,id,tid):
    try:
        test = Test.objects.get(test_id = tid)
        if test.classroom.faculty == Faculty.objects.get(user=request.user):
            if test.published:
                TestResponse.objects.filter(test = test).delete()
            test.published = not test.published
            test.save()
            return redirect('classTestManage',id=id,tid=tid)
    except:
        pass
    return redirect('dashboard')

def ClassAddQuestion(request,id,tid):
    try:
        classroom = Classroom.objects.get(classroom_id=id)
        if not Faculty.objects.get(user=request.user) == classroom.faculty:
            return redirect('dashboard')
    except:
        return redirect('dashboard')
    extemp = getBasetemp(request)
    test = Test.objects.get(test_id = tid)
    if request.method == 'POST':
        question = request.POST.get('question')
        option_1 = request.POST.get('option_1')
        option_2 = request.POST.get('option_2')
        option_3 = request.POST.get('option_3')
        option_4 = request.POST.get('option_4')
        correct = request.POST.get('correct')
        TestQuestion.objects.create(test=test,question=question,option_1=option_1,option_2=option_2,option_3=option_3,option_4=option_4,correct=correct)
        return redirect('classTestManage',id,tid)
    else:
        return render(request,'learnerApp/addQuestion.html',context={'id':id,'extemp':extemp,'classroom':classroom,'test':test})

def createAdmin(request):
    Admin.objects.create(user=request.user)
    return redirect('dashboard')

def courseList(request):
    myCourses = None
    extemp = getBasetemp(request)
    if request.user.is_faculty:
        courses = Course.objects.filter(faculty=Faculty.objects.get(user = request.user))
    elif request.user.is_student:
        student = Student.objects.get(user = request.user)
        courses = Course.objects.filter(faculty__institute = student.institute)
        myCourses = Course.objects.filter(students=student)
    else:
        raise Http404("Inavlid User Role")
    return render(request,'learnerApp/courseList.html',context={'extemp':extemp,'courses':courses,'myCourses':myCourses})

@login_required(login_url="/login/")
def addCourse(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        decription = request.POST.get('description')
        faculty = Faculty.objects.get(user=request.user)
        createImage(title)
        im = Image.open(settings.MEDIA_ROOT+'/learnerApp/images/test.png')
        blob = BytesIO()
        im.save(blob,'PNG')
        blob.seek(0)
        name = str(uuid1())+'.png'
        imfile = File(blob,name=name)
        obj = Course.objects.create(faculty=faculty,title=title,description=decription)
        obj.course_image.save(name,imfile,save=True)
        obj.save()
        return redirect('courseList')
    else:
        return render(request, 'learnerApp/addCourse.html')

def viewCourse(request,id):
    extemp = getBasetemp(request)
    try:
        course = Course.objects.get(course_id=id)
    except:
        return redirect('dashboard')
    videos = CourseVideo.objects.filter(course=course)
    student = None
    registered = None
    if request.user.is_student:
        student = Student.objects.get(user = request.user)
        registered = student in course.students.all()
    return render(request,'learnerApp/course.html',context={'id':id,'course':course,'extemp':extemp,'videos':videos,'student':student,'registered':registered})

def courseAddVideo(request,id):
    extemp = getBasetemp(request)
    if request.method == 'POST':
        course = Course.objects.get(course_id=id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')
        print(request.FILES)
        courseVideo = CourseVideo.objects.create(title=title,course=course,description=description)
        courseVideo.video.save(str(uuid1()) +'.'+ video.name.split('.')[-1],video)
        return redirect('course',id)
    else:
        return render(request,'learnerApp/addCourseVideo.html',context={'id':id,'extemp':extemp})

def courseRegister(request,id):
    try:
        course = Course.objects.get(course_id=id)
        student = Student.objects.get(user=request.user)
        course.students.add(student)
        course.save()
        return redirect('course',id)
    except:
        return redirect('dashboard')

def sendPass(name,email,password):
    subject = 'Welcome to E-class'
    message = f'''Hi {name},You have been registered to E-class.
    your username: {email}
    your password: {password}'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail( subject, message, email_from, recipient_list )
