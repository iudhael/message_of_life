from django.db import models

# Create your models here.


class Subscribers(models.Model):
    email_subscriber = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Subscriber"

    def __str__(self):
        return self.email_subscriber


class MailMessage(models.Model):
    title = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)
    status = models.BooleanField(default=False)
    date_de_publication_email = models.DateField('date de publication du mail ', auto_now_add=True)

    class Meta:
        verbose_name = "Message mail envoyé"

    def __str__(self):
        return self.title
