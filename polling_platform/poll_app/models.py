from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

	
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    poll_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True)

    def __str__(self):
        return self.poll_text



class EmailId(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='poll')
    email_id = models.EmailField()
    username= models.CharField(max_length=200)
    is_partone_complete = models.BooleanField(default=False)
    is_parttwo_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.email_id



class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name = 'answers_poll')
    email = models.ForeignKey(EmailId, on_delete=models.CASCADE, related_name = 'answers_email')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


