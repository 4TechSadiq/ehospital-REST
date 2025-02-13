from rest_framework import serializers
from .models import UserModel, DoctorModel, HeathStatus, MedNews, Appointment, MedRecord, Prescription, MedicalHistory, TreatmentHistory, MedNews, MedRecord, MedicalCondition, Medicine, Hospital, ApprovedAppointments, Notification

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

class TreatmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentHistory
        fields = "__all__"

class MedicalHistorySerializer(serializers.ModelSerializer):
    history = TreatmentHistorySerializer(many=True, source='history', read_only=True)

    class Meta:
        model = MedicalHistory
        fields = ['condition', 'severity', 'medication', 'status', 'history']

class MedicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCondition
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
    

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class ApprovedAppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedAppointments
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'