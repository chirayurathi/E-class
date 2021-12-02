from os import name
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import views
urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.login, name="login"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('profile/',views.profile, name="profile"),
    path('addInstitute/',views.addInstitute, name="addInstitute"),
    path('allUser/',views.allUser, name="allUser"),
    path('addFaculty/',views.addFaculty, name="addFaculty"),
    path('addStudent/',views.addStudent, name="addStudent"),
    path('addClassroom/',views.addClassroom, name="addClassroom"),
    path('students/',views.studentList, name="studentList"),
    path('classrooms/',views.classroomList, name="classroomList"),
    path('logout/',views.logout, name="logout"),
    path('classroom/<int:id>/',RedirectView.as_view(pattern_name='classFeed'), name="classroom"),
    path('classroom/<int:id>/feed/',views.classFeedView,name="classFeed"),
    path('classroom/<int:id>/tests/',views.classTestsView,name="classTests"),
    path('classroom/<int:id>/material/',views.classMaterialView,name="classMaterial"),
    path('classroom/<int:id>/members/',views.classMembersView,name="classMembers"),
    path('classroom/<int:id>/members/transfer',views.classFacultyTransfer,name="classTransfer"),
    path('classroom/<int:id>/classCall/',views.classCallView,name="classCall"),
    path('classroom/<int:id>/material/add/',views.classAddMaterial,name='addClassMaterial'),
    path('classroom/<int:id>/material/<int:mid>/',views.classMaterialDiscussion,name='classMaterialDiscussion'),
    path('classroom/<int:id>/tests/addTest/',views.addClassTest,name='addClassTest'),
    path('classroom/<int:id>/tests/<int:tid>/',views.classTestManage,name='classTestManage'),
    path('classroom/<int:id>/tests/<int:tid>/addQuestion/',views.ClassAddQuestion,name='addQuestion'),
    path('classroom/<int:id>/tests/<int:tid>/togglePublish/',views.togglePublish, name="togglePublish"),
    path('classroom/<int:id>/tests/<int:tid>/testAttend/',views.testAttend, name="testAttend"),
    path('classroom/<int:id>/tests/<int:tid>/response/<int:rid>/',views.viewResponse, name="viewResponse"),
    path('delete/',views.clearMaterial),
    path('createimg/',views.createImage),
    path('createAdmin/',views.createAdmin, name='createAdmin'),
    path('courses/',views.courseList,name='courseList'),
    path('courses/<int:id>/',views.viewCourse,name='course'),
    path('courses/<int:id>/register',views.courseRegister,name='courseRegister'),
    path('courses/<int:id>/addVideo',views.courseAddVideo,name='addCourseVideo'),
    path('addCourse/',views.addCourse,name='addCourse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)