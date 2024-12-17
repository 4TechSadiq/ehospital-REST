from django.shortcuts import render
from rest_framework import generics
from .models import UserModel, DoctorModel, HeathStatus, MedNews, Appointment, MedRecord, Prescription, MedicalHistory
from .serializers import UserSerializer, DoctorSerializer, HeathStatusSerializer, MedNewsSerializer, AppointmentSerializer, MedRecordSerializer, PrescriptionSerializer, MedHistorySerializer
# Create your views here.


# User Views
class UserList(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class ListUser(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer   

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class CreateUser(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

# Doctor Views
class DoctorList(generics.ListCreateAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

class CreateDoctor(generics.CreateAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

# Medical History Views
class MedHistoryList(generics.ListCreateAPIView):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedHistorySerializer

class MedHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedHistorySerializer

class CreateMedHistory(generics.CreateAPIView):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedHistorySerializer

# Heath Status Views
class HeathStatusList(generics.ListCreateAPIView):
    queryset = HeathStatus.objects.all()
    serializer_class = HeathStatusSerializer

class HeathStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeathStatus.objects.all()
    serializer_class = HeathStatusSerializer

class CreateHeathStatus(generics.CreateAPIView):
    queryset = HeathStatus.objects.all()
    serializer_class = HeathStatusSerializer

# Med News Views
class MedNewsList(generics.ListCreateAPIView):
    queryset = MedNews.objects.all()
    serializer_class = MedNewsSerializer

class MedNewsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedNews.objects.all()
    serializer_class = MedNewsSerializer

class CreateMedNews(generics.CreateAPIView):
    queryset = MedNews.objects.all()
    serializer_class = MedNewsSerializer

# Appointment Views
class ListAppointment(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class DetailAppointment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class RemoveAppointment(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class CreateAppointment(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

