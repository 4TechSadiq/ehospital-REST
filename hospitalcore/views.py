from django.shortcuts import render
from rest_framework import generics
from .models import UserModel, DoctorModel, HeathStatus, MedNews, Appointment, MedRecord, Prescription, MedicalHistory, TreatmentHistory, MedicalCondition,Medicine, Hospital, ApprovedAppointments, Notification
from .serializers import UserSerializer, DoctorSerializer, HeathStatusSerializer, MedNewsSerializer, AppointmentSerializer, MedRecordSerializer, PrescriptionSerializer, MedHistorySerializer, TreatmentHistorySerializer, MedicalConditionSerializer,MedicineSerializer, HospitalSerializer, ApprovedAppointmentsSerializer, NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .modules.user_id import generate_e_hosp_id
from .modules.image_url import get_url
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import math as Math
from rest_framework.parsers import MultiPartParser, FormParser
from .modules.MedicalInvoice import generate_medical_invoice
from .modules.SendMail import send_invoice_email

# Make sure to set your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request):
        print("Received data:", request.data)
        try:
            amount = request.data.get('amount')
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                automatic_payment_methods={'enabled': True},
            )
            return Response({
                'clientSecret': intent.client_secret
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=400)

class CreateAppointmentView(APIView):
    def post(self, request):
        try:
            # Verify payment with Stripe
            print("Received data:", request.data)
            payment_intent_id = request.data.get('payment_intent_id')
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if payment_intent.status != 'succeeded':
                return Response({
                    'error': 'Payment not completed'
                }, status=400)

            # Create appointment
            appointment = Appointment.objects.create(
                first_name=request.data.get('first_name'),
                mid_name=request.data.get('mid_name'),
                last_name=request.data.get('last_name'),
                phone=request.data.get('phone'),
                email=request.data.get('email'),
                disease=request.data.get('disease'),
                description=request.data.get('description'),
                doc_id=request.data.get('doc_id'),
                user_id=request.data.get('user_id'),
                payment_intent_id=payment_intent_id,
                payment_status='completed'
            )

            return Response({
                'message': 'Appointment created successfully',
                'ap_id': appointment.ap_id
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=400)

class AppointmentView(APIView):
    def post(self, request):
        print("Received data:", request.data)
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            # Verify payment with Stripe
            try:
                payment_intent = stripe.PaymentIntent.retrieve(
                    request.data['payment_intent_id']
                )
                if payment_intent.status == 'succeeded':
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'error': 'Payment not completed'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except stripe.error.StripeError as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateAppointment(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class DeleteAppointment(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


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
            print(profile_file)
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

class ListUsers(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

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

class UserDetail(generics.UpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class CreateUser(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

class DeleteUser(generics.DestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


from rest_framework.exceptions import NotFound
class ListSingleUser(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Get 'user_id' from URL
        queryset = UserModel.objects.filter(id=user_id)
        if not queryset.exists():
            raise NotFound({"error": "User not found."})
        return queryset

# Doctor Views
class DoctorList(generics.ListCreateAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

    def post(self, request, *args, **kwargs):
        print("Incoming request data:", request.data)

        # Safely copy request data
        try:
            data = request.data.copy()
            #data['doc_id'] = generate_e_hosp_id()
        except Exception as e:
            return Response({'error': f'Failed to generate doctor ID: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Validate profile image
        image = request.FILES.get('profile')
        if not image:
            return Response({'error': 'Profile image is required'}, status=status.HTTP_400_BAD_REQUEST)
        elif not image.name.lower().endswith(('png', 'jpg', 'jpeg')):
            return Response({'error': 'Invalid image format. Only PNG, JPG, and JPEG are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
        elif image.size > 5 * 1024 * 1024:  # Limit to 5MB
            return Response({'error': 'Profile image size exceeds 5MB limit.'}, status=status.HTTP_400_BAD_REQUEST)

        # Process and upload the profile image
        try:
            image_url = get_url(image)
            data['profile'] = image_url
        except Exception as e:
            return Response({'error': f'Image processing failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save the data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Debug serializer errors
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDoctor(generics.ListAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

import logging

logger = logging.getLogger(__name__)

class UpdateDoctor(generics.UpdateAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Log incoming data for debugging
        logger.debug(f"Update request data: {request.data}")
        
        # Create a mutable copy of the data
        mutable_data = request.data.copy()
        
        # Handle password separately if needed
        password = mutable_data.pop('password', None)
        if password:
            logger.debug("Password field found in request")
        
        # Handle file upload
        if 'profile' in request.FILES:
            mutable_data['profile'] = request.FILES['profile']
            url = get_url(mutable_data['profile'])
            mutable_data['profile'] = url
        elif 'profile' in mutable_data and not mutable_data['profile']:
            # If profile field is empty string, remove it to prevent validation error
            mutable_data.pop('profile')
        
        # Convert price to float if present
        if 'price' in mutable_data:
            try:
                if mutable_data['price']:
                    mutable_data['price'] = float(mutable_data['price'])
            except (ValueError, TypeError):
                return Response(
                    {'detail': 'Invalid price format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(
            instance, 
            data=mutable_data, 
            partial=True  # Always use partial=True for updates
        )
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            # Update password if provided
            if password:
                instance.password = password  # Assuming you have proper password handling
                instance.save()
            
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Update error: {str(e)}")
            logger.error(f"Serializer errors: {serializer.errors if hasattr(serializer, 'errors') else 'No serializer errors'}")
            
            return Response(
                {
                    'detail': str(e),
                    'fields': serializer.errors if hasattr(serializer, 'errors') else {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Error in perform_update: {str(e)}")
            raise
       
class DeleteDoctor(generics.DestroyAPIView):
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
from collections import defaultdict

class MedNewsList(generics.ListCreateAPIView):
    queryset = MedNews.objects.all()
    serializer_class = MedNewsSerializer
    
    def post(self, request, *args, **kwargs):
        data = {key: value for key, value in request.data.items() if key != 'image'}
        
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            image_url = get_url(image)
            data['image'] = image_url
        except Exception as e:
            return Response({'error': f'Image processing failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MedNewsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMedNews(generics.ListAPIView):
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

    def post(self, request, *args, **kwargs):
        print("Incoming request data:", request.data)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class CreateMedicine(generics.CreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class ListMedicine(generics.ListAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class CreatePrescription(generics.CreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("Incoming request data:", request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListPrescription(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class CreateHospital(generics.CreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class ListHospital(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class UpdateHospital(generics.UpdateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class DeleteHospital(generics.DestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class ApprovedAppointment(generics.CreateAPIView):
    queryset = ApprovedAppointments.objects.all()
    serializer_class = AppointmentSerializer

class ListApprovedAppointment(generics.ListAPIView):
    queryset = ApprovedAppointments.objects.all()
    serializer_class = ApprovedAppointmentsSerializer

class CreateNotification(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        print("Incoming request data:", data)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListNotification(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class UpdateNotification(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class RecieveData(APIView):
    def post(self, request):
        print("Received data:", request.data)
        invoice = generate_medical_invoice(request.data)
        print("Generated invoice:", invoice)
        mail = send_invoice_email(pdf_buffer=invoice[1], recipient_email=request.data['userData']['email'], subject='Medical Invoice', body='Please find the attached medical invoice.',sender_email="", sender_password="")
        return Response(request.data)
