from django.db import models
from django.core.urlresolvers import reverse

def get_absolute_url(self):
        return reverse('detail', args=[str(self.slug)])

# Create your models here.
