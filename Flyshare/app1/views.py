from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app1.models import *
from app1.serializer import PostModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.
def indexPage(request):
    return render(request, 'Login/index.html')
def signupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        uemail = request.POST.get('email')
        upass = request.POST.get('password1')
        ucpass = request.POST.get('password2')
        if upass == ucpass:
            my_user = User.objects.create_user(first_name=fname,last_name=lname,email=uemail,password=upass,username=uname)
            my_user.save()
            messages.success(request,"Your account has been successfully created.")
            return redirect('login')
        else:
            return redirect('index')
    return render(request,'Login/signup.html')
def loginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('user_password')
        user = authenticate(request,username=uname,password=upass)
        if user is not None:
            login(request,user)
            return redirect('base')
        else:
            messages.error(request, "Incorrect credentials")
            return redirect('login')
    return render(request,'Login/login.html')
@login_required(login_url='login')
def basePage(request):
    return render(request,'Login/base.html')
def logoutPage(request):
    logout(request)
    return redirect('login')

def PostPage(request):
    return render(request,'Post/post.html')

def Post(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        passenger_name = request.POST.get('PassengerName')
        date_of_journey = request.POST.get('DateOfJourney')
        gender = request.POST.get('gender')
        flight_number = request.POST.get('FlightNumber')
        pnr_number = request.POST.get('PNRNumber')
        source = request.POST.get('source')  # Ensure field name consistency
        destination = request.POST.get('destination')  # Ensure field name consistency
        baggage_space = request.POST.get('BaggageSpace')
        checkbox = request.POST.get('checkbox') == 'on'  # Checkbox handling

        # Create a new instance of PostModel
        new_passenger = PostModel(
            passenger_name=passenger_name,
            date_of_journey=date_of_journey,
            gender=gender,
            flight_number=flight_number,
            pnr_number=pnr_number,
            source=source,
            destination=destination,
            baggage_space=baggage_space,
            is_checked=checkbox,
        )
        
        # Save the new instance to the database
        new_passenger.save()

    return render(request, 'Post/post.html', {})





class PostModelAPIView(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get(self, request):
        qs = PostModel.objects.all()
        serializer = PostModelSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostModelAPIViewID(generics.GenericAPIView):
    serializer_class = PostModelSerializer
    queryset = PostModel.objects.all()
    def get_object(self,id):
        try:
            data = PostModel.objects.get(id=id)
            return data
        except PostModel.DoesNotExist:
            return None
    
    def get(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self,request,id):
        qs = self.get_object(id)
        serializer = PostModelSerializer(qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        qs = self.get_object(id)
        if qs is None:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)        
        

