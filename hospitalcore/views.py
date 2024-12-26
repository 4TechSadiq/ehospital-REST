from django.shortcuts import render
from rest_framework import generics
from .models import UserModel, DoctorModel, HeathStatus, MedNews, Appointment, MedRecord, Prescription, MedicalHistory, TreatmentHistory, MedicalCondition
from .serializers import UserSerializer, DoctorSerializer, HeathStatusSerializer, MedNewsSerializer, AppointmentSerializer, MedRecordSerializer, PrescriptionSerializer, MedHistorySerializer, TreatmentHistorySerializer, MedicalConditionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .modules.user_id import generate_e_hosp_id
from .modules.image_url import get_url
# Create your views here.


# User Views
class UserList(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print("Incoming request data:", request.data)  # Log request payload for debugging
        data = request.data.dict()  # Convert QueryDict to a mutable dictionary
        data['user_id'] = generate_e_hosp_id()
        print("Generated user_id:", data['user_id'])
        
        # Handle profile upload
        if 'profile' in request.FILES:
            profile_file = request.FILES['profile']
            data['profile'] = get_url(profile_file)  # Upload the file and get its URL
        else:
            print("No profile file found in request.FILES")
            data['profile'] = None  # Or handle this case as required
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            print("Serializer validated data:", serializer.validated_data)  # Log validated data
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)  # Log errors if validation fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CreateUser(APIView):
#     def post(self, request, *args, **kwargs):
#         print(request.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class LoginUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if user exists with provided email and password
        user = UserModel.objects.filter(email=email, password=password).first()
        
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid email or password"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class CreateUser(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class DeleteUser(generics.DestroyAPIView):
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

class CreateTreatment(generics.CreateAPIView):
    queryset = TreatmentHistory.objects.all()
    serializer_class = TreatmentHistorySerializer

class ListTreatment(generics.ListCreateAPIView):
    queryset = TreatmentHistory.objects.all()
    serializer_class = TreatmentHistorySerializer

class CreateMedicalCondition(generics.CreateAPIView):
    queryset = MedicalCondition.objects.all()
    serializer_class = MedicalConditionSerializer

class ListMedicalCondition(generics.ListAPIView):
    queryset = MedicalCondition.objects.all()
    serializer_class = MedicalConditionSerializer