from django.db import models
from user.models import User
# Create your models here.
class Note(models.Model):
    title = models.CharField('标题', max_length=100)
    content = models.TextField('内容')
    created_time = models.DateField('创建时间', auto_now_add=True)
    update_time = models.DateField('更新时间', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)