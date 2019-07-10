from django.db import models

# Create your models here.
class Subscriber(models.Model):
    """Define blog subscribers"""
    email = models.CharField(
        max_length=100, blank=False, null=False, help_text='Enter email address'
    )
    first_name = models.CharField(
        max_length=100, blank=False, null=False, help_text='Enter first name'
    )
    last_name = models.CharField(
        max_length=100, blank=False, null=False, help_text='Enter last name'
    )


    def __str__(self):
        """Define string rep of subscriber."""
        return self.email

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = "Subscribers"
