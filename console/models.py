from django.db import models

# Create your models here.
class Power(models.Model):
    level = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.level, self.description)