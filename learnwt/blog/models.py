# -*- coding: utf-8 -*-
"""
Blog Listing and Detail Page Definitions.

This models.py file defines the data models for our Blog app.
"""

from django.db import models
from django.shortcuts import render
from django.utils.text import slugify
from django import forms
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator
)

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.models import Page, Orderable
from wagtail.search import index
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, RichTextFieldPanel, MultiFieldPanel,
    InlinePanel
)
from wagtail.api import APIField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from streams import blocks
from logging import getLogger


logger = getLogger(__name__)

# Create your models here.
class BlogAuthorsOrderable(Orderable):
    """Provide ability to assign one or more blog authors in a specific order."""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE,
    )
    api_fields = [
        APIField('author'),
        APIField('author_name'),
        APIField('author_website')
    ]
    panels = [
        SnippetChooserPanel('author')
    ]
    # EXPOSING DJANGO MODEL FORMS TO API
    @property
    def author_name(self):
        return self.author.name()

    @property
    def author_website(self):
        return self.author.website

@register_snippet
class BlogAuthor(models.Model):
    """Define a reusable data model for assigning blog authors."""
    # Snippets are a great way to store and make use of reusable data.
    # This includes things like categories, menus, etc.
    # Here we use it to associate blogs with authors.
    # FIELDS
    first_name = models.CharField(
        max_length=100, null=True, blank=False,
        help_text="Author's first name"
    )
    last_name = models.CharField(
        max_length=120, null=True, blank=False,
        help_text="Author's last name"
    )
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True, blank=False,
        related_name='+'
    )

    def name(self, name_format='f l'):
        names = {
            'f l': f'{self.first_name} {self.last_name}',
            'l f': f'{self.last_name}, {self.first_name}'
        }
        return names.get(name_format)
    # API FIELDS
    api_fields = [
        APIField('first_name'),
        APIField('last_name'),
        APIField('website'),
        APIField('image')
    ]
    # SEARCH FIELDS
    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('website')
    ]
    # ADMIN INTERFACE CONFIGURATION
    panels = [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
            ImageChooserPanel('image'),
        ], heading='Name and Image'),
        MultiFieldPanel([
            FieldPanel('website')
        ], heading="Links")
    ]

    def __str__(self):
        """String representative of this class."""
        return self.name()

    class Meta:
        verbose_name = "Blog Author"


@register_snippet
class BlogCategory(models.Model):
    """Define categories for our blog posts."""
    # FIELDS
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    slug = models.SlugField(
        verbose_name="slug", allow_unicode=True, max_length=100,
        default=""
    )
    # API FIELDS
    api_fields = [
        APIField('name'),
        APIField('slug')
    ]
    # SEARCH FIELDS
    search_fields = [
        index.SearchField('name'),
        index.SearchField('slug')
    ]
    # ADMIN INTERFACE CONFIGURATION
    panels = [
        FieldPanel('name'),
    ]

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = "Blog Categories"
        ordering = ['name', ]


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
        # This will contain plenty of subclassed results so you will need
        # to use post.specific() to access properties of these posts.
        all_posts = BlogDetailPage.objects.live().public().order_by('id')
        # Adding custom pagination to handle errors explicitly
        paginator = Paginator(all_posts, 3)
        page = request.GET.get("page")

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context

    api_fields = [
        APIField('custom_title'),
    ]
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
        context['n'] = len(context['latest_posts'])
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
    """Define parental blog detail class."""

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

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    content = StreamField([
        ("title_and_text", blocks.TitleAndTextBlock()),
        ('full_richtext', blocks.RichtextBlock()),
        ('simple_richtext', blocks.SimpleRichtextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('custom_title'),
        index.SearchField('blog_summary'),
        index.SearchField('blog_image'),
        index.SearchField('content'),
        index.SearchField('blog_authors'),
        index.SearchField('categories')
    ]
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        RichTextFieldPanel('blog_summary'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label="Author",
                        min_num=1, max_num=8)
        ], heading="Blog Authors"),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Categories')
    ]
    # FIELDS RETURNED BY API
    api_fields = [
        APIField('custom_title'),
        APIField('blog_summary'),
        APIField('blog_image'),
        APIField('content'),
        APIField('blog_authors'),
        APIField('categories')
    ]

    class Meta:
        verbose_name = 'Blog Detail'
        verbose_name_plural = 'Blog Details'

    def save(self, *args, **kwargs):
        """Clear the cache for this specific BlogDetail object on save."""
        cache_key = make_template_fragment_key(
            'blog_post_preview',
            [self.id, ]
        )
        logger.info(f'BlogDetail page saved. Deleting cache {cache_key}')
        cache.delete(cache_key)
        return super().save(*args, **kwargs)

# First sub-classed blog detail page
class ArticleBlogPage(BlogDetailPage):
    """Define custom model for articles."""

    template = 'blog/article_blog_page.html'
    subtitle = models.CharField(max_length=150, blank=True, null=True)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        related_name='+',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1200x300'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('custom_title'),
            FieldPanel('subtitle'),
            RichTextFieldPanel('blog_summary'),
        ], heading='Intro text'),
        MultiFieldPanel([
            ImageChooserPanel('intro_image'),
            ImageChooserPanel('blog_image'),
        ], heading='Article Images'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label="Author",
                        min_num=1, max_num=8)
        ], heading="Blog Authors"),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Categories')
    ]


class VideoBlogPage(BlogDetailPage):
    """Define a sub-class of BlogDetailPage explicitly for video."""
    template = 'blog/video_blog_page.html'
    youtube_video_id = models.CharField(max_length=100)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        RichTextFieldPanel('blog_summary'),
        ImageChooserPanel('blog_image'),
        FieldPanel('youtube_video_id'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            InlinePanel('blog_authors', label="Author",
                        min_num=1, max_num=8)
        ], heading="Blog Authors"),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ], heading='Categories')
    ]
