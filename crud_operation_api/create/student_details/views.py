from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import student
from .serializers import studentSerializer
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authtoken.models import Token
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class studenttokenauthentication(APIView):
    
    def post(self,request):
        try:
            data = {}
            username = request.data.get('username')
            password = request.data.get('password')
            data['username'] = username
            data['password'] = password
            auth_user = User.objects.filter(username=username).first()
            success = check_password(password,auth_user.password)
            if success:
                students_data = student.objects.all()
                serializer = studentSerializer(students_data, many=True) 
                return Response(serializer.data,status=status.HTTP_200_OK) 
            else:
                return Response({'success': False, 'message': "details entered incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(str(e))



# class create_user(APIView):
#     def post(self,request):
#         data = {'user_id': request.data.get('user_id'),
#                 'password':request.data.get('password')
#         }
#         serializer = studentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#         data = {
#             # "data": serializer.data,
#             "msg":"Data Added Succefully"
#         }
#         return Response(data=data, status=status.HTTP_200_OK)


# User.objects.filter(username=username)

             
class StudentDetailsApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
            students_data = student.objects.all()
            serializer = studentSerializer(students_data, many=True) 
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)


## Registration Api 
class registeredview(APIView):

    def post(self, request):
        data = {}
        username = request.data.get('username')
        password = request.data.get('password')
        data['username'] = username
        data['password'] = password 
        auth_user = User.objects.filter(username=username).first()

        if auth_user:
            success = check_password(password, auth_user.password)
            if success:
                return Response({"message": 'You are already registered User. Please try log in.'}, status=status.HTTP_412_PRECONDITION_FAILED)
            else:
                return Response({"message":"Incorrect password"},status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            # create user
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            return Response({"message": "Registration done."}, status=status.HTTP_200_OK)


class login(APIView):
    def post(self,request):
        response = {}
        username = request.data.get('username')
        password = request.data.get('password')
        auth_user = User.objects.filter(username=username).first()
        if auth_user:
            password_check = check_password(password,auth_user.password)
            if password_check:
                try:
                    Token_object = Token.objects.get(user=auth_user)
                    response['message'] = 'You are successfully logged in - Token Already Exists'
                    response['token'] = Token_object.key
                    return Response(response,status=status.HTTP_200_OK)
                except Token.DoesNotExist:
                    Token_object = Token.objects.create(user=auth_user)
                    response["message"]="You are successfully logged in - Token is created'"
                    Token_object = Token.objects.get(user=auth_user)
                    response['token']= Token_object.key
                    return Response(response,status=status.HTTP_200_OK)
            else:
                    return Response({"message": 'Invalid Password.'}, status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            return Response({"message": "You are not registered"}, status=status.HTTP_412_PRECONDITION_FAILED)
        

class StudentDetailstoken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            "msg": "Data Added Succefully",
            "authenticated": request.user.is_authenticated
        }
        return Response(data=data, status=status.HTTP_200_OK)

# inserting the records

class InsertRecordsApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permision_classes = [IsAdminUser]

    def post(self,request):
        data = {'firstname': request.data.get('firstname'),
                'lastname':request.data.get('lastname'),
                'city': request.data.get('city'),
                'phonenumber': request.data.get('phonenumber')
        }
        serializer = studentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        data = {
            # "data": serializer.data,
            "msg":"Data Added Succefully"
        }
        return Response(data=data, status=status.HTTP_200_OK)
        
# Deleting Records        
class DeleteRecordsApiView(APIView):

     def delete(self,request,id):
        delete_records = student.objects.filter(id=id)
        delete_records.delete()
        return Response({"Messsage":"Record deleted sucesssfulyy"})
     
# updating records
class UpdateRecordsApiView(APIView):

     def put(self,request,id):
        oldrecord = student.objects.get(id=id)
        serializer = studentSerializer(instance=oldrecord,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


#retrive specific records
class RetriveSpecificRecords(APIView):
    
    def get(self, request,id):  
        retrive_records = student.objects.get(id=id)
        serializer = studentSerializer(retrive_records)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'message':'Data Fetched Succesfully'})
        return Response(serializer.data,status=status.HTTP_200_OK)


#retriverecords using post
class RetriveSpecificRecordsUsingPost(APIView):

    def post(self,request):
        data = {"id":request.data.get('id')}
        retrive_records = student.objects.get(id=data['id'])
        serializer = studentSerializer(retrive_records)
        return Response(serializer.data,status=status.HTTP_200_OK)


class DeleteRecordsUsingPost(APIView):    
    def post(self,request):
        permission_name = 'DELETE_POST'
        data = {"id":request.data.get('id')}
        delete_records = student.objects.get(id=data['id'])
        x = studentSerializer(delete_records)
        print(x)
        abc = x.data
        delete_records.delete()
        deleted_data = {"data":abc,
            'message':'Date Deleted Sucessfully'
        }
        return Response(deleted_data)
 

class UpdaterecordsiUsingPost(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self,request):
        permission_name = 'UPDATE_POSTS'
        
        if request.user:
            if PermissionModel.objects.filter(
                permission_name=permission_name, 
                is_active=True, 
                user_id=request.user_id).exists():
                data = {
                    'id':request.data.get('id')}
                old_records = student.objects.get(id=data['id'])
                serializer = studentSerializer(instance=old_records,data=request.data,partial=True)
                if serializer.is_valid():
                serializer.save()
                print(serializer.data)   
                data = {
                    "Data" : serializer.data,
                    "Message": "Data Updated Sucessfully"
                    }
                return Response(data)
        else:
            data = {"Message": "Please Login"}
            return Response(data)

## Permission    

class retrivepermission(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,id=None):
        if id is not None:
            retrive_data = student.objects.get(id=id)
            serializer = studentSerializer(retrive_data)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            retrive_data = student.objects.all()
            serializer = studentSerializer(retrive_data,many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        

class updatepermission(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def put(self,request,id):
        oldrecord = student.objects.get(id=id)
        serializer = studentSerializer(instance=oldrecord,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


        
# inserting the records

class InsertRecordsApiView(APIView):
    authentication_classes = [BasicAuthentication]
    permision_classes = [IsAdminUser]

    def post(self,request):
        data = {'firstname': request.data.get('firstname'),
                'lastname':request.data.get('lastname'),
                'city': request.data.get('city'),
                'phonenumber': request.data.get('phonenumber')
        }
        serializer = studentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        data = {
            # "data": serializer.data,
            "msg":"Data Added Succefully"
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CustomePermissionView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # user = authenticate(request,username=username,password=password)
        try:
            auth_user = User.objects.get(username=username)
        except Exception as ex:
            print(ex)
            return
        
        # If not a super user
        if not auth_user.is_superuser:
            print(auth_user)
            if request.method == 'POST':
                data = {
                    'firstname': request.data.get('firstname'),
                    'lastname':request.data.get('lastname'),
                    'city': request.data.get('city'),
                    'phonenumber': request.data.get('phonenumber')
                }
                serializer = studentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        "data": serializer.data,
                        "msg":"Data Added Succefully"
                        }
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    pass
            elif request.method =="GET":
                data = {"id":request.data.get('id')}
                retrive_data = student.objects.get(id=data['id'])
                serializer = studentSerializer(retrive_data)
                return Response(data=serializer.data,status=status.HTTP_200_OK)
        
        return Response({'msg': 'you can do all operations'})
            # try:
            #     request_method = request.method.lower()
            #     if request_method == "post":

            #         print("post")
            #     else:
            #         print('not eligible')
            # except Exception as e:
            #     return Response({"msg":"you are not eligible"})

            # # return Response({'msg':'you can do only post and get crud operations'})


class ORM(APIView):
    def get(self,request):
        filter_data = student.objects.filter(city="mumbai")|student.objects.filter(city="Mumbai")
        count = filter_data
        serializer = studentSerializer(filter_data,many=True)
        data ={"data":serializer.data,"count":count}
        return Response(data=data,status=status.HTTP_200_OK)
    

class SetPermission(APIView):
    authentication_classes = [TokenAuthentication]
    permision_classes = [IsAdminUser]
    
    def post(self, request):
        to_username = request.data.get('to_username')
        User.objects.filter(username=to_username)
            
        
