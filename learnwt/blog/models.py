# -*- coding: utf-8 -*-
"""
Blog Listing and Detail Page Definitions.

This models.py file defines the data models for our Blog app.
"""

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, RichTextFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks

# Create your models here.


class BlogListingPage(Page):
    """Return list of all blog detail pages."""

    template = 'blog/blog_listing_page.html'

    custom_title = models.CharField(
        max_length=100, blank=False, null=False,
        help_text='Overwrite default title'
    )

    def get_context(self, request, *args, **kwargs):
        """Adding blog pages."""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        return context

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]


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
