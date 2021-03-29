from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

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
        elif role == "admin" :
            user.is_admin=True

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email="xyz@gmail.com", password=None):
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
    REQUIRED_FIELDS = ['is_admin','is_institute','is_faculty','is_student']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.user_email)

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class Student(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    student_id = models.CharField(max_length=75)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    student_number = models.PositiveIntegerField(blank=True)
    institute = models.ForeignKey('Institute',on_delete=models.CASCADE)
    class Meta:
        unique_together = [['student_id','institute']]

class Institute(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=75)
    institute_address = models.CharField(max_length=75)
    institute_number = models.PositiveBigIntegerField()
    institute_id = models.IntegerField(unique=True)

class Faculty(models.Model):
    user = models.OneToOneField('CustomUser',primary_key=True,on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=75)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    faculty_number = models.PositiveIntegerField(blank=True)
    institute = models.ForeignKey('Institute',on_delete=models.CASCADE)
    class Meta:
        unique_together = [['faculty_id','institute']]

