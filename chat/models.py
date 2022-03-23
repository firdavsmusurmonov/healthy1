from django.db import models
from account.models import Customuser
from doctor.utils import generate_unique_slug
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def get_avatar(instance, filename):
    return "threads/%s" % (filename)


class Thread(models.Model):
    subject = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to=get_avatar, default='threads/default.png')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            if len(self.subject) > 0:
                self.slug = generate_unique_slug(self, 'subject')
        super(Thread, self).save(*args, **kwargs)

    def send_message(self, message, user):
        Message.objects.create(
            thread=self,
            text=message,
            user=user
        ).save()

        particpaints = Particpaint.objects.filter(thread=self).all()
        for par in particpaints:
            room_name = 'chat_' + str(par.user.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                room_name, {
                    "type": "chat_message",
                    "message": str(message)
                })

    def __str__(self):
        return str(self.slug)


class Particpaint(models.Model):
    user = models.ForeignKey(Customuser, null=True, on_delete=models.SET_NULL, related_name="particpaint")
    thread = models.ForeignKey(Thread, null=True, on_delete=models.SET_NULL, related_name="particpaintThread")
    last_read = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.thread)


class Message(models.Model):
    thread = models.ForeignKey(Thread, null=True, on_delete=models.SET_NULL, related_name="message1")
    user = models.ForeignKey(Customuser, null=True, on_delete=models.SET_NULL, related_name="message")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.thread)
