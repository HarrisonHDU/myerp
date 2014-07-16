from django.db import models

# Create your models here.

MALE = 'M'
FEMALE = 'F'
sex_enum = (
    (MALE, 'Male'),
    (FEMALE, 'Female')
)


class Student(models.Model):
    code = models.CharField(max_length=50, blank=False, verbose_name='学号', unique=True)
    name = models.CharField(max_length=50, blank=False, verbose_name='姓名')
    sex = models.CharField(max_length=1, choices=sex_enum, default=MALE, verbose_name='性别')
    age = models.IntegerField(max_length=3, verbose_name='年龄')
    political = models.CharField(max_length=50, verbose_name='政治面貌')
    origin = models.CharField(max_length=50, verbose_name='籍贯')
    professional = models.CharField(max_length=50, verbose_name='院系')

    def __str__(self):
        return '{}({})'.format(self.name, self.code)


