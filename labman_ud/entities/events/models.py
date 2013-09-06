# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.


def event_logo_path(self, filename):
    return '%s/%s%s' % ('events', self.event.slug, os.path.splitext(filename)[-1])


def viva_photo_path(self, filename):
    return "%s/%s%s" % ("vivas", self.slug, os.path.splitext(filename)[-1])


VIVA_RESULTS = (
    ('Apt', 'Apt'),
    ('Cum Laude', 'Cum Laude'),
    ('Cum Laude by unanimity', 'Cum Laude by unanimity'),
)


#########################
# Model: EventType
#########################

class EventType(models.Model):
    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(EventType, self).save(*args, **kwargs)


#########################
# Model: Event
#########################

class Event(models.Model):
    event_type = models.ForeignKey('EventType')

    full_name = models.CharField(
        max_length=250,
    )

    short_name = models.CharField(
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        verbose_name=u'Location',
        blank=True,
    )

    start_date = models.DateField(
        blank=True,
    )

    end_date = models.DateField(
        blank=True,
    )

    year = models.PositiveIntegerField(
        blank=True,
    )

    homepage = models.URLField(
        verbose_name='Homepage',
        blank=True,
        null=True,
    )

    observations = models.TextField(
        max_length=1500,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s %s' % (self.short_name, self.year)

    def save(self, *args, **kwargs):
        if (not self.year) and (self.start_date):
            self.year = self.start_date.year

        event_name = u'%s %s' % (self.short_name, self.year)
        self.slug = slugify(event_name)

        super(Event, self).save(*args, **kwargs)


#########################
# Model: EventLogo
#########################

class EventLogo(models.Model):
    event = models.ForeignKey('Event')

    logo = models.ImageField(
        upload_to=event_logo_path,
        verbose_name='Logo',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'Logo for event: %s' % (self.event.short_name)


#########################
# Model: Viva
#########################

class Viva(models.Model):
    date = models.DateField()

    result = models.CharField(
        max_length=250,
        choices=VIVA_RESULTS,
        default='Apt',
        blank=True,
    )

    held_at_university = models.ForeignKey('organizations.Organization')

    panel = models.ForeignKey('VivaPanel')


#########################
# Model: VivaPanel
#########################

class VivaPanel(models.Model):
    chair = models.ForeignKey(
        'persons.Person',
        related_name='is_chair',
    )

    chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_chairs_organization',
    )

    first_co_chair = models.ForeignKey(
        'persons.Person',
        related_name='is_first_co_chair',
    )

    first_co_chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_first_co_chairs_organization',
    )

    second_co_chair = models.ForeignKey(
        'persons.Person',
        related_name='is_second_co_chair',
    )

    second_co_chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_second_co_chairs_organization',
    )

    third_co_chair = models.ForeignKey(
        'persons.Person',
        related_name='is_third_co_chair',
    )

    third_co_chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_third_co_chairs_organization',
    )

    secretary = models.ForeignKey(
        'persons.Person',
        related_name='is_secretary',
    )

    secretarys_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_secretarys_organization',
    )