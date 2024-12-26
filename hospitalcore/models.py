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
    doctor = models.ManyToManyField(DoctorModel)
    image = models.CharField(max_length=1500)

    def __str__(self):
        return self.headline

class Appointment(models.Model):
    ap_id = models.CharField(max_length=20)
    doctor = models.OneToOneField(DoctorModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    disease = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mid_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.ap_id

class MedRecord(models.Model):
    ap_id = models.OneToOneField(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return self.ap_id

class Prescription(models.Model):
    ap_id = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id



class MedicalCondition(models.Model):
    CONDITION_SEVERITY = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]

    STATUS_CHOICES = [
        ('Under Treatment', 'Under Treatment'),
        ('Ongoing', 'Ongoing'),
        ('Stable', 'Stable'),
        ('Resolved', 'Resolved'),
    ]

    condition = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=CONDITION_SEVERITY)
    medication = models.CharField(max_length=100)
    doctor = models.ForeignKey(DoctorModel, on_delete=models.CASCADE, related_name="conditions")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return self.condition

class TreatmentHistory(models.Model):
    medical_condition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE, related_name="history")
    date = models.DateField()
    remarks = models.TextField()
    outcome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medical_condition.condition} - {self.date}"
