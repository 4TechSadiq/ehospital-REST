from django.db import models

# Create your models here.
class UserModel(models.Model):
    user_id = models.CharField(max_length=20)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=450)
    profile = models.CharField(max_length=1500)

    def __str__(self):
        return self.user_id

class DoctorModel(models.Model):
    doc_id = models.CharField(max_length=20)
    doc_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=13)

class MedicalHistory(models.Model):
    user_id = models.OneToOneField(UserModel,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    doctor = models