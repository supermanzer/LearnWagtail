# -*- coding: utf-8 -*-
"""
Flex Page Model

This file defines our general flexible page.
"""

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from streams import blocks


class FlexPage(Page):
    """Define flexible page class."""

    template = "flex/flex_page.html"

    content = StreamField([
        ("title_and_text", blocks.TitleAndTextBlock()),
        ('full_richtext', blocks.RichtextBlock()),
        ('simple_richtext', blocks.SimpleRichtextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock()),
        ("button_block", blocks.ButtonBlock()),
    ], null=True, blank=True)

    subtitle = models.CharField(max_length=100, null=True, blank=True, help_text='Appears in the Navbar')

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel('content')
    ]

    class Meta:  # noqa
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
