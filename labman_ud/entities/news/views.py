# -*- encoding: utf-8 -*-

import threading
import weakref

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.syndication.views import Feed

from .models import News, PersonRelatedToNews, ProjectRelatedToNews, PublicationRelatedToNews

from entities.persons.models import Person
from entities.projects.models import Project
from entities.publications.models import Publication

from labman_setup.models import *


###########################################################################
# View: news_index
###########################################################################

def news_index(request):
    news = News.objects.all().order_by('-created', 'title')

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': 'News',
        'news': news,
    }

    return render(request, 'news/index.html', return_dict)


###########################################################################
# View: view_news
###########################################################################

def view_news(request, news_slug):
    news = get_object_or_404(News, slug=news_slug)
    # tags = news.tags.all()

    related_persons_ids = PersonRelatedToNews.objects.filter(news=news.id).values('person_id')
    related_persons = Person.objects.filter(id__in=related_persons_ids).order_by('slug')

    related_projects_ids = ProjectRelatedToNews.objects.filter(news=news.id).values('project_id')
    related_projects = Project.objects.filter(id__in=related_projects_ids).order_by('slug')

    related_publications_ids = PublicationRelatedToNews.objects.filter(news=news.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('slug')

    if not related_persons and not related_projects and not related_publications:
        related = False
    else:
        related = True

    # dictionary to be returned in render(request, )
    return_dict = {
        # 'tags': tags,
        'web_title': news.title,
        'news': news,
        'related': related,
        'related_persons': related_persons,
        'related_projects': related_projects,
        'related_publications': related_publications,
    }

    return render(request, 'news/info.html', return_dict)


###########################################################################
# Feed: news feeds
###########################################################################

class LatestNewsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestNewsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    try:
        _settings = LabmanDeployGeneralSettings.objects.get()
        research_group_short_name = _settings.research_group_short_name

    except:
        research_group_short_name = u'Our'

    title = u'%s news' % research_group_short_name
    description = u'%s news' % research_group_short_name

    def get_object(self, request):
        self.__request.request = weakref.proxy(request)
        return super(LatestNewsFeed, self).get_object(request)

    def link(self, obj):
        url = reverse('news_index')
        return self.__request.request.build_absolute_uri(url)

    def items(self):
        return News.objects.order_by('-created')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        url = reverse('view_news', args=[item.slug])
        return self.__request.request.build_absolute_uri(url)
