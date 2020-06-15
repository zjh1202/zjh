from django.db import models

# Create your models here.


class User(models.Model):

    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=128)
    object = models.CharField(max_length=128)
    num = models.IntegerField(unique=True)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class TeacherUser(models.Model):

    Teacher_number = models.IntegerField(unique=True)
    Teacher_name = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    school = models.CharField(max_length=128)
    object = models.CharField(max_length=128)
    num = models.IntegerField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Teacher_number

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Teacher(models.Model):

    text_order = models.IntegerField()
    name = models.CharField(max_length=128)
    number = models.IntegerField()
    text = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    keyword = models.CharField(max_length=1000)
    test_number = models.IntegerField()
    num = models.IntegerField()
    subject = models.CharField(max_length=128)


    def __str__(self):
        return self.number

    class Meta1:
        ordering = ["name"]
        verbose_name = "教师"
        verbose_name_plural = "教师"


class Student(models.Model):

    name = models.CharField(max_length=128)
    answer = models.CharField(max_length=1000)
    text_order = models.IntegerField()
    test_number = models.IntegerField()
    grade = models.FloatField()
    num = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta2:
        ordering = ["name", "text_order"]
        verbose_name = "学生"
        verbose_name_plural = "学生"


class WordAdmin(models.Model):
    test_number = models.IntegerField(unique=True)
    subject = models.CharField(max_length=125)
    text_number = models.CharField(max_length=20, default='1')

    def __str__(self):
        return self.test_number
