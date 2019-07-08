# learnwt/home/models.py
"""
Home Application models.

This file defines models for the home application.
"""
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks



class HomePageCarousel(Orderable):
    """Add between 1 and 5 images."""

    page = ParentalKey('home.HomePage', related_name='carousel_images')
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=40, null=True, blank=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    text_orient = models.CharField(
        choices=(
            ('left', "Left"),
            ('right', 'Right'),
            ('center', 'Center')
        ), max_length=20, null=True, blank=True
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('text_orient'),
        ImageChooserPanel("carousel_image"),
    ]

class HomePage(Page):
    """
    Define home page data model.
    """
    template = 'home/home_page.html'
    max_count = 1  # Restrict instances of this page to a single instance.

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=['bold', 'italic'])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    sidenav_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content = StreamField([
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
            ImageChooserPanel('banner_image'),
            ImageChooserPanel('sidenav_image'),
            PageChooserPanel('banner_cta'),
        ], heading="Banner Options"),
        MultiFieldPanel([
            InlinePanel('carousel_images', min_num=1, max_num=5, label='Images'),
        ], heading='Carousel Images'),
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = "Hello World"
        verbose_name_plural = "Hello Worlds"
