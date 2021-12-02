from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.http import response

class CustomUserManager(BaseUserManager):
    def create_user(self, user_email, role = "", password=None):
        if not user_email:
            raise ValueError('Users must have an email')

        user = self.model(user_email=user_email)
        if role == "institute" :
            user.is_institute=True
        elif role == "faculty" :
            user.is_faculty=True
        elif role == "student" :
            user.is_student=True       
        else:
            user.is_admin=True

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email="xyz@gmail.com", password=None):
        user = self.create_user(
            user_email=user_email,
            password=password
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    is_admin = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    user_email = models.EmailField(verbose_name='Email',primary_key=True,unique=True)
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'user_email'
    # REQUIRED_FIELDS = ['is_admin','is_institute','is_faculty','is_student']

    objects = CustomUserManager()

    def __str__(self):
        if self.is_admin:
            return str(Admin.objects.get(user=self).first_name)
        elif self.is_faculty:
            try:
                return str(Faculty.objects.get(user=self).first_name)
            except:
                None
        elif self.is_institute:
            try:
                return str(Institute.objects.get(user=self).institute_name)
            except:
                None
        elif self.is_student:
            return str(Student.objects.get(user=self).first_name)
        return str(self.user_email)

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    def getImage(self):
        if self.is_admin:
            return Admin.objects.get(user=self).user_image
        elif self.is_faculty:
            return Admin.objects.get(user=self).user_image
        elif self.is_institute:
            return Institute.objects.get(user=self).user_image
        elif self.is_student:
            return Student.objects.get(user=self).user_image

class Admin(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75,verbose_name="First Name",null=True,blank=True)
    last_name = models.CharField(max_length=75,verbose_name="Last Name",null=True,blank=True)
    admin_number = models.PositiveIntegerField(blank=True,verbose_name="Mobile Number",null=True)
    user_image = models.ImageField(upload_to='learnerApp/profile_images/admin',blank=True)

class Student(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    student_id = models.CharField(max_length=75,verbose_name="Student ID",null=True,blank=True)
    first_name = models.CharField(max_length=75,verbose_name="First Name",null=True,blank=True)
    last_name = models.CharField(max_length=75,verbose_name="Last Name",null=True,blank=True)
    student_number = models.PositiveIntegerField(verbose_name="Mobile Number",null=True,blank=True)
    institute = models.ForeignKey('Institute',on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='learnerApp/profile_images/student',blank=True)
    class Meta:
        unique_together = [['student_id','institute']]

class Institute(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=75,verbose_name="Institute Name",null=True,blank=True)
    institute_address = models.TextField(max_length=100,verbose_name="Address",null=True,blank=True)
    institute_number = models.PositiveBigIntegerField(verbose_name="Mobile Number",null=True,blank=True)
    institute_id = models.IntegerField(unique=True,verbose_name="Institute Id",null=True,blank=True)
    user_image = models.ImageField(upload_to='learnerApp/profile_images/institute',blank=True)

class Faculty(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=75,verbose_name="Faculty Id",null=True,blank=True)
    first_name = models.CharField(max_length=75,verbose_name="First Name",null=True,blank=True)
    last_name = models.CharField(max_length=75,verbose_name="Last Name",null=True,blank=True)
    faculty_number = models.PositiveIntegerField(verbose_name="Mobile Number",null=True,blank=True)
    institute = models.ForeignKey('Institute',on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='learnerApp/profile_images/faculty',blank=True)
    class Meta:
        unique_together = [['faculty_id','institute']]

class Classroom(models.Model):
    classroom_id = models.BigAutoField(primary_key=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,related_name='classrooms')
    title = models.CharField(max_length=50)
    classroom_image = models.ImageField(upload_to='learnerApp/classsroom_images',blank=True)

class ClassFeedMessage(models.Model):
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def user_image(self):
        if self.sender.is_faculty:
            return Faculty.objects.get(user=self.sender).user_image.url
        else:
            return Student.objects.get(user=self.sender).user_image.url
    
    @property
    def user_name(self):
        if self.sender.is_faculty:
            user = Faculty.objects.get(user=self.sender)
        else:
            user = Student.objects.get(user=self.sender)
        return(str(user.first_name + user.last_name))

class ClassMaterial(models.Model):
    material_id = models.BigAutoField(primary_key=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    material = models.FileField(upload_to='learnerApp/material')
    added_on = models.DateTimeField(auto_now_add=True)

class ClassMaterialMessage(models.Model):
    material = models.ForeignKey('ClassMaterial', on_delete=models.CASCADE)
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def user_image(self):
        if self.sender.is_faculty:
            return Faculty.objects.get(user=self.sender).user_image.url
        else:
            return Student.objects.get(user=self.sender).user_image.url
    
    @property
    def user_name(self):
        if self.sender.is_faculty:
            user = Faculty.objects.get(user=self.sender)
        else:
            user = Student.objects.get(user=self.sender)
        return(str(user.first_name + user.last_name))

class Course(models.Model):
    course_id = models.BigAutoField(primary_key=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,related_name='courses',blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    course_image = models.ImageField(upload_to='learnerApp/classsroom_images',blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

class CourseVideo(models.Model):
    video_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    description = models.CharField(max_length = 200, null = True, blank = True)
    video = models.FileField(upload_to = 'learnerApp/videos')
    added_on = models.DateTimeField(auto_now_add = True)

class Test(models.Model):
    test_id = models.BigAutoField(primary_key=True)
    classroom = models.ForeignKey('Classroom',models.CASCADE)
    title = models.CharField(max_length = 50)
    start_time = models.DateTimeField(help_text="yyyy-mm-dd hh:mm")
    end_time = models.DateTimeField(help_text="yyyy-mm-dd hh:mm")
    published = models.BooleanField(default=False)

class TestQuestion(models.Model):
    question_id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey('Test',on_delete=models.CASCADE)
    question = models.CharField(max_length = 200)
    option_1 = models.CharField(max_length = 100)
    option_2 = models.CharField(max_length = 100)
    option_3 = models.CharField(max_length = 100)
    option_4 = models.CharField(max_length = 100)
    correct = models.CharField(max_length = 50)

class TestResponse(models.Model):
    response_id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey('Test',on_delete = models.CASCADE)
    student = models.ForeignKey('Student',on_delete=models.CASCADE)

    @property
    def score(self):
        answers = TestQuestionResponse.objects.filter(response = self)
        correct = answers.filter(is_correct = True)
        return(str(correct.count()) + '/' + str(answers.count()))

class TestQuestionResponse(models.Model):
    q_response_id = models.BigAutoField(primary_key=True)
    response = models.ForeignKey('TestResponse',on_delete=models.CASCADE)
    question = models.ForeignKey('TestQuestion',on_delete=models.CASCADE)
    option = models.CharField(max_length=50)
    is_correct = models.BooleanField()

class CourseTest(models.Model):
    course = models.OneToOneField('Course',models.CASCADE,primary_key=True)
    published = models.BooleanField(default=False)

class CourseTestQuestion(models.Model):
    question_id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey('CourseTest',on_delete=models.CASCADE)
    question = models.CharField(max_length = 200)
    option_1 = models.CharField(max_length = 100)
    option_2 = models.CharField(max_length = 100)
    option_3 = models.CharField(max_length = 100)
    option_4 = models.CharField(max_length = 100)
    correct = models.CharField(max_length = 50)

class CourseTestResponse(models.Model):
    response_id = models.BigAutoField(primary_key=True)
    test = models.ForeignKey('CourseTest',on_delete = models.CASCADE)
    student = models.ForeignKey('Student',on_delete=models.CASCADE)

    @property
    def score(self):
        answers = CourseTestQuestionResponse.objects.filter(response = self)
        correct = answers.filter(is_correct = True)
        return(str(correct.count()) + '/' + str(answers.count()))

class CourseTestQuestionResponse(models.Model):
    q_response_id = models.BigAutoField(primary_key=True)
    response = models.ForeignKey('CourseTestResponse',on_delete=models.CASCADE)
    question = models.ForeignKey('CourseTestQuestion',on_delete=models.CASCADE)
    option = models.CharField(max_length=50)
    is_correct = models.BooleanField()