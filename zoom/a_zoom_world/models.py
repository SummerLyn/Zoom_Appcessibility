from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class DomicileType(models.Model):
    """ This table distinguishes the type of housing it is"""
    type = models.CharField(max_length=500, default=None)
    square_feet = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.type


class Address(models.Model):
    """ This table holds the location of the a_zoom_world listing"""
    street = models.CharField(max_length=200, default=None)
    street_two = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.street


class Photo(models.Model):
    """ This table holds all the photos for the a_zoom_world """
    photo = models.ImageField(upload_to='images/')
    featured = models.BooleanField(default=False)

    def image_object(self):
        return u'<img src="' + self.photo.url + '" width=200 />'

    image_object.short_description = "Image"
    image_object.allow_tags = True

    def __str__(self):
        return self.photo.url


class Amenity(models.Model):
    """ This table holds all the amenities a a_zoom_world has """
    type = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.type


class PotentialAllergen(models.Model):
    """ This table stores information on potential allergens"""

    description = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.description


class AccessibilityNeed(models.Model):
    """ This table holds the list of accessibility needs for the user/traveller"""

    name = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=1000, default=None)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    """ This table holds a list of possible vehicle availability """

    year = models.IntegerField(default=None)
    make_and_model = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=500, default=None)
    access_needs = models.ManyToManyField(AccessibilityNeed)

    def __str__(self):
        return self.make_and_model


class Property(models.Model):
    """ This table holds information about each a_zoom_world """

    type_id = models.ForeignKey(DomicileType)
    address = models.ForeignKey(Address)
    title = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=2000, default=None)
    num_bedroom = models.CharField(max_length=20, default=None)
    num_bathroom = models.CharField(max_length=20, default=None)
    access_num_bedroom = models.CharField(max_length=20, default=None)
    access_num_bathroom = models.CharField(max_length=20, default=None)
    photo_property = models.ManyToManyField(Photo, related_name='property_photos', verbose_name='photo_property')
    property_amenity = models.ManyToManyField(Amenity)
    property_allergens = models.ManyToManyField(PotentialAllergen)
    property_vehicle = models.ManyToManyField(Vehicle)
    property_access = models.ManyToManyField(AccessibilityNeed)

    def __str__(self):
        return self.title


class NeedException(models.Model):
    """ This tables holds exceptions to access needs"""
    need = models.CharField(max_length=200, default=None)
    room_location = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.need


class PropertyNeed(models.Model):
    """ This table holds specific needs to a listed property  """

    property_id = models.ForeignKey(Property)
    accessibility_need = models.ForeignKey(AccessibilityNeed)
    property_need = models.ManyToManyField(NeedException)

    def __index__(self):
        return self.property_id


class ZoomUser(models.Model):
    """ This table holds the user information using django default"""

    user = models.OneToOneField(User)
    accessibility_need = models.ManyToManyField(AccessibilityNeed)

    def __index__(self):
        return self.user
