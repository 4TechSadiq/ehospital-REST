from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserModel(models.Model):
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=450)
    profile = models.CharField(max_length=1500)

    def __str__(self):
        return self.user_id

class DoctorModel(models.Model):
    doc_id = models.CharField(max_length=20)
    doc_name = models.CharField(max_length=250)
    doc_email = models.EmailField()
    profile = models.CharField(max_length=1500)
    experiance = models.CharField(max_length=250)
    hospital = models.CharField(max_length=250)
    password = models.CharField(max_length=100)
    category = models.CharField(max_length=250)
    phone = models.CharField(max_length=13)
    price = models.FloatField()

    def __str__(self):
        return self.doc_id

class MedicalHistory(models.Model):
    user_id = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    condition = models.CharField(max_length=1500)
    severity = models.CharField(max_length=1500)
    medication = models.CharField(max_length=1500)
    date = models.DateField(auto_now=True)
    doctor = models.ManyToManyField(DoctorModel)
    status = models.CharField(max_length=150)
    remark = models.CharField(max_length=200)
    outcome = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id

class HeathStatus(models.Model):
    user_id = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    pressure = models.CharField(max_length=100)
    sugar = models.CharField(max_length=100)
    cholestrol = models.CharField(max_length=100)
    pre_expl = models.CharField(max_length=300)
    sug_expl = models.CharField(max_length=300)
    chol_expl = models.CharField(max_length=300)

    def __str__(self):
        return self.user_id

class MedNews(models.Model):
    headline = models.CharField(max_length=1500)
    news = models.CharField(max_length=1500)
    date = models.DateField(auto_now=True)
    doctor = models.CharField(max_length=150)
    image = models.CharField(max_length=1500)

    def __str__(self):
        return self.headline

class Appointment(models.Model):
    ap_id = models.CharField(max_length=20)
    user_id = models.CharField(max_length=50, null=True)
    doc_id = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now=True)
    email = models.EmailField(null=True)
    disease = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mid_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    payment_intent_id = models.CharField(max_length=100, null=True)
    payment_status = models.CharField(max_length=50, null=True)

    def save(self, *args, **kwargs):
        if not self.ap_id:
            last_appointment = Appointment.objects.order_by('-id').first()
            new_id = f"AP-{(last_appointment.id if last_appointment else 0) + 1:04}"
            self.ap_id = new_id
        super().save(*args, **kwargs)


    def __str__(self):
        return self.ap_id

class MedRecord(models.Model):
    ap_id = models.OneToOneField(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return self.ap_id


class MedicalCondition(models.Model):
    user = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    severity = models.CharField(max_length=520)
    medication = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    status = models.CharField(max_length=500)

    def __str__(self):
        return self.condition


class TreatmentHistory(models.Model):
    user = models.CharField(max_length=100)
    medical_condition = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)
    remarks = models.TextField()
    outcome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medical_condition.condition} - {self.date}"


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    dosage_options = models.CharField(max_length=200)  # Example: "50mg, 100mg, 200mg"
    description = models.TextField(null=True, blank=True)
    side_effects = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine)  # Allows multiple medicines
    dosage = models.CharField(max_length=100)
    times_per_day = models.IntegerField()
    routine = models.CharField(max_length=10)  # Before or After

    def __str__(self):
        return f"Prescription for {self.patient}"


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    services = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    contact = models.CharField(max_length=25)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class ApprovedAppointments(models.Model):
    ap_id = models.CharField(max_length=20)
    user_id = models.CharField(max_length=50, null=True)
    doc_id = models.CharField(max_length=50, null=True)
    date = models.DateField(auto_now=True)
    email = models.EmailField(null=True)
    disease = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mid_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    payment_intent_id = models.CharField(max_length=100, null=True)
    payment_status = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.ap_id
    

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

class Notification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ]

    prescription = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, null=True, blank=True)

    def calculate_price(self):
        # Base price for each medicine (random 2-3 digit number)
        medicine_count = self.prescription.medicines.count()
        base_price = random.randint(50, 999)  # Random base price between $50 and $999
        
        # Price calculation based on number of medicines and times per day
        total_price = (base_price * medicine_count * self.prescription.times_per_day) / 2
        return round(total_price, 2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification for {self.prescription.patient} - ${self.price}"

    class Meta:
        ordering = ['-created_at']

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='hospitalcore.Prescription')  # Include the app label
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(prescription=instance)