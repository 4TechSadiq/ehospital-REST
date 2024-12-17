from rest_framework import serializers
from .models import UserModel, DoctorModel, HeathStatus, MedNews, Appointment, MedRecord, Prescription, MedicalHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorModel
        fields = '__all__'

class MedHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class HeathStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeathStatus
        fields = '__all__'

class MedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedNews
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class MedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedRecord
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
    

