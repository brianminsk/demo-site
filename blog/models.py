from django.db import models
from django.shortcuts import render
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get blog entries
        blog_entries = BlogPage.objects.child_of(self).live()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blog_entries = blog_entries.filter(tags__name=tag)

        context['blog_entries'] = blog_entries
        return context

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('tags'),
    ]

    promote_panels = Page.promote_panels + [
        # moved to content_panels
        # FieldPanel('tags'),
    ]