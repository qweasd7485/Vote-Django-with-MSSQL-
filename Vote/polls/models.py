from django.db import models
from django.core.validators import MaxValueValidator
import django.utils.timezone as timezone
from datetime import datetime
import pytz

# Create your models here.

#status_timezone = pytz.timezone('Etc/UTC')
#tz = timezone(timedelta(hours=+8))


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    revoteable = models.BooleanField(default=False)
    ballot = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(3)]) #每次可投票數
    
    def __unicode__(self):
        return self.question_text
    
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.question + self.choice_text
    
    def __str__(self):
        return self.question.question_text + '：' + self.choice_text
    
class Voted(models.Model):    #使用者議題投過次數記錄
    question = models.IntegerField(default=0)
    account = models.IntegerField(default=0)
    votetimes = models.IntegerField(default=0)
    create_date = models.DateTimeField('date voted', default=datetime.now())
    
    def __unicode__(self):
        return self.account + self.question + '(' + self.create_date +')'
    
    def __str__(self):
        return '會員編號：' + str(self.account) + ' 題目編號：' + str(self.question) + '(第一次投票時間：' + self.create_date.strftime("%m/%d/%Y, %H:%M:%S") + ')'
        
class VoteHistory(models.Model):             #使用者議題選項紀錄 代表該時間使用者於該議題投過某選項一票
    question = models.IntegerField(default=0)
    account = models.IntegerField(default=0)
    choice = models.IntegerField(default=0)
    content = models.CharField(max_length=50, default="")  
    create_date = models.DateTimeField('date voted', default=datetime.now())
    
    def __unicode__(self):
        return self.account + '投過' + self.question + ' 候選項目' + self.content + '1票   (時間：' + self.create_date + ')' 
    
    def __str__(self):
        return '會員編號：' + str(self.account) + '投過' + str(self.question) + ' 候選項目總編號' + str(self.choice) + '1票   (時間：' + self.create_date.strftime("%m/%d/%Y, %H:%M:%S") + ')' + str(self.content) 
    