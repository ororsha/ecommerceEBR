import random
import os
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.shortcuts import reverse
from .utils import unique_slug_generator

# Create your models here.
LOCATIONS_CHOICES = (
    ('HF', 'Haifa'),
    ('HZ', 'Herzliya'),
    ('TV', 'Tel-Aviv'),
    ('As', 'Ashdod'),
    ('EL', 'Eilat')
)

LABEL_CHOICES = (
    ('M', 'Motor yacht'),
    ('S', 'Sailboat'),
    ('T', 'Tender Boat')
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


class BoatQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    # def featured(self):
    #     return self.filter(featured=True, active=True)


class BoatManager(models.Manager):
    def get_queryset(self):
        return BoatQuerySet(self.model, using=self._db)

    # def all(self):
    #     return self.get_queryset().active()

    def active(self):  # Product.objects.featured()
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None


class Boat(models.Model):
    title = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(decimal_places=2, max_digits=20, default=100.00)
    discount_price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    marine_location = models.CharField(choices=LOCATIONS_CHOICES, max_length=2)
    boat_category = models.CharField(choices=LABEL_CHOICES, max_length=1)
    builder = models.CharField(max_length=100)
    year = models.DecimalField(decimal_places=0, max_digits=4)
    length = models.DecimalField(decimal_places=2, max_digits=5)
    max_guests = models.DecimalField(decimal_places=0, max_digits=3)
    max_speed = models.DecimalField(decimal_places=2, max_digits=4)
    active = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False)
    description = models.TextField()
    image_1 = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    image_4 = models.ImageField(upload_to=upload_image_path, blank=True, null=True)

    objects = BoatManager()

    def get_absolute_url(self):
        return "/boats/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def product_pre_save_receiver(sender, instance , **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Boat)


    # def get_absolute_url(self):
    #     return reverse("core:product", kwargs={
    #         'slug': self.slug
    #     })
    #
    # def get_add_to_cart_url(self):
    #     return reverse("core:add-to-cart", kwargs={
    #         'slug': self.slug
    #     })
    #
    # def get_remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart", kwargs={
    #         'slug': self.slug
    #     })
    #
    # def get_check_date_and_update_url(self):
    #     return reverse("core:check-date-and-update", kwargs={
    #         'slug': self.slug
    #     })