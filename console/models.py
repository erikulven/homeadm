from django.db import models


# Create your models here.
class Power(models.Model):
    level = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    hourly_consume = models.FloatField(default=0.0)

    def __unicode__(self):
        return "%s: %s" % (self.level, self.description)

    def daily_consume(self):
        return self.hourly_consume * 24 * 1.0

    def monthly_consume(self):
        return self.daily_consume() * 31 * 1.0

    def yearly_consume(self):
        return self.daily_consume() * 365 * 1.0
