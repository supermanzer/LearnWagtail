# -*- coding: utf-8 -*-
"""
Blog Listing and Detail Page Definitions.

This models.py file defines the data models for our Blog app.
"""

from django.db import models
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, RichTextFieldPanel
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks

# Create your models here.


class BlogListingPage(RoutablePageMixin, Page):
    """Return list of all blog detail pages."""

    template = 'blog/blog_listing_page.html'

    custom_title = models.CharField(
        max_length=100, blank=False, null=False,
        help_text='Overwrite default title'
    )

    def get_context(self, request, *args, **kwargs):
        """Adding blog pages."""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public().order_by('last_published_at')
        return context

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    class Meta:
        verbose_name = "Blog Listing"
        verbose_name_plural = "Blog Listings"

    @route(r'^latest/$')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['latest_posts'] = context['posts'][:2]
        context['n'] = context['latest_posts'].count()
        return render(request, 'blog/latest_posts.html', context)

    def get_sitemap_urls(self, request=None):
        # return [] <- Do this to avoid sitemaps for this page
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_blog_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9
            }
        )
        return sitemap


class BlogDetailPage(Page):
    """Create a blog page model."""

    custom_title = models.CharField(
        max_length=100, null=False, blank=False
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    blog_summary = RichTextField(
        blank=False, null=True,
        help_text='Provide a short summary of what this blog post is about.'
    )
    content = StreamField([
        ("title_and_text", blocks.TitleAndTextBlock()),
        ('full_richtext', blocks.RichtextBlock()),
        ('simple_richtext', blocks.SimpleRichtextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        RichTextFieldPanel('blog_summary'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content')
    ]
