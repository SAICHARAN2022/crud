from django.conf.urls import url
from django.urls import path, include
from .views import StudentDetailsApiView
from .views import InsertRecordsApiView
from .views import DeleteRecordsApiView
from .views import UpdateRecordsApiView
from .views import RetriveSpecificRecords
from .views import RetriveSpecificRecordsUsingPost
from .views import DeleteRecordsUsingPost
from .views import UpdaterecordsiUsingPost
from .views import studenttokenauthentication,registeredview,login,StudentDetailstoken,updatepermission,retrivepermission,customepermissions
from .views import ORM
urlpatterns = [
    path('retrive-api',StudentDetailsApiView.as_view()),
    path('delete-api/<int:id>/',DeleteRecordsApiView.as_view()),
    path('update-api/<int:id>/',UpdateRecordsApiView.as_view()),
    path('retrive-records/<int:id>/',RetriveSpecificRecords.as_view()),
    path('retrive-records-post/',RetriveSpecificRecordsUsingPost.as_view()),
    path('delete-api-post/',DeleteRecordsUsingPost.as_view()),
    path('update-api-post/',UpdaterecordsiUsingPost.as_view()),
    path('rerive-api-token-api/',studenttokenauthentication.as_view()),
    path('registration/',registeredview.as_view()),
    path('login/',login.as_view()),
    #path('create-user/',create_user.as_view()),
    path('token/',StudentDetailstoken.as_view()),
    path('update/<int:id>',updatepermission.as_view()),
    path('insert-api',InsertRecordsApiView.as_view()),
    path('retrive/(?P<id>\d+)', retrivepermission.as_view()),
    path('user/permission/', customepermissions.as_view()),
    path('filter/data/', ORM.as_view())
 ]


