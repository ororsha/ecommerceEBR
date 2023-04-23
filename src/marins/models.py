import random
import os
from django.db.models import Q
from django.shortcuts import reverse

from django.db import models

# Create your models here.


LOCATIONS_CHOICES = (
    ('Haifa', 'Haifa'),
    ('Herzliya', 'Herzliya'),
    ('Tel-Aviv', 'Tel-Aviv'),
    ('Ashdod', 'Ashdod'),
    ('Ashkelon', 'Ashkelon'),
    ('Eilat', 'Eilat')
)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "boats/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )


class MarinQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    # def featured(self):
    #     return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(name__icontains=query) |
                  Q(description__icontains=query) |
                  Q(location__icontains=query))
        return self.filter(lookups).distinct()


class MarinManager(models.Manager):
    def get_queryset(self):
        return MarinQuerySet(self.model, using=self._db)

    # def all(self):
    #     return self.get_queryset().active()

    def active(self):  # Product.objects.featured()
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Marin(models.Model):
    title        = models.CharField(max_length=64)
    description = models.TextField()
    is_open     = models.BooleanField(default=True)
    location    = models.CharField(choices=LOCATIONS_CHOICES, max_length=100)
    image_1       = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    max_vessels = models.IntegerField(default=1)
    slug        = models.SlugField(default="", null=False)
    active          = models.BooleanField(default=False)

    objects = MarinManager()

    def get_absolute_url(self):
        return reverse("marins:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title