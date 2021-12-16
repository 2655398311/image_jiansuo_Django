from django.db import models


# Create your models here.


class UploadImages(models.Model):
    uname = models.CharField(max_length=64)
    raw_name = models.CharField(max_length=256, null=True)

class Student(models.Model):

    sno = models.AutoField(primary_key = True)
    sname = models.CharField(max_length=30,unique=True)
    spwd = models.CharField(max_length=30)

    def __str__(self):
        return u'Student:%s'%self.sname