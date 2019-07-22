# -*- coding: utf-8 -*-
"""
Menu Models

These models define how we will construction our menus.
"""
from django.db import models

from django_extensions.db.fields import AutoSlugField

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
)
from wagtail.snippets.models import register_snippet


class MenuItem(Orderable):
    """Define a single menu item."""
    
    link_title = models.CharField(max_length=100, blank=True, null=True)
    # URL field uses too strict validation criteria, we use CharField for more
    # flexibility
    link_url = models.CharField(
        max_length=250, blank=True, null=True
    )
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='+'
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)
    
    page = ParentalKey('Menu', related_name="menu_items")
    
    panels = [
        FieldPanel('link_title'),
        FieldPanel('link_url'),
        PageChooserPanel('link_page'),
        FieldPanel('open_in_new_tab')
    ]
    
    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        else:
            return '#'

    @property
    def title(self):
        if self.link_page and not self.link_url:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        else:
            return 'Missing Title'

@register_snippet
class Menu(ClusterableModel):
    """Define main menu object."""

    title = models.CharField(max_length=100, null=True, blank=False)
    # A custom
    slug = AutoSlugField(populate_from="title", editable=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug')
        ], heading="Menu"),
        InlinePanel("menu_items", label='Menu Item')
    ]

    def __str__(self):
        return self.title
