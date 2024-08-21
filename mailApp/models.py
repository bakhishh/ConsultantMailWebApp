from django.db import models


class Data(models.Model):
    type = models.CharField(max_length=255)
    student_id = models.CharField(max_length=255)
    consultant_name = models.CharField(max_length=255)
    assistant_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.consultant_name


class Consultant(models.Model):
    name = models.CharField(max_length=255 , default="none")
    mail = models.EmailField(max_length=255 , default="none")

    def __str__(self):
        return self.name
