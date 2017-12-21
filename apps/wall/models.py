from __future__ import unicode_literals
from django.db import models
from ..login.models import User



class Message(models.Model):
    content = models.TextField(max_length=400)
    user = models.ForeignKey(User, related_name="messages")

    # objects = UserManager()
    def __unicode__(self):
        return 'content: {}, user: {}, id: {}'.format(self.content, self.user, self.id)

