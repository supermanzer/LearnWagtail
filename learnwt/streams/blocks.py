# -*- coding: utf-8 -*-
"""
Content Block Definitions

This file defines custom stream field blocks.
"""
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, help_text='Add your title', max_length=100)
    text = blocks.TextBlock(required=True, help_text='Add additional text.')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class CardBlock(blocks.StructBlock):
    """Cards with image, text, and buttons"""

    title = blocks.CharBlock(required=True, help_text='Add your title', max_length=100)
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("image", ImageChooserBlock(required=True)),
            ("title", blocks.CharBlock(required=True, max_length=40)),
            ("text", blocks.TextBlock(required=True, max_length=200)),
            ("button_page", blocks.PageChooserBlock(required=False)),
            ("button_url", blocks.URLBlock(required=False, help_text="If the button page above is selected, that is rendered preferentially.")),
        ])
    )
    class Meta:
        template = 'streams/card_block.html'
        icon = 'user'
        label = 'Scientist Card'


class RichtextBlock(blocks.RichTextBlock):
    """Fully featured Rich Text."""

    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'doc-full'
        label = 'Full RichText'


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Limited featured Rich Text."""

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link'
        ]
        # super().__init__(**kwargs)


    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'edit'
        label = 'Simple RichText'


class CTABlock(blocks.StructBlock):
    """A simple Call to Action component."""

    title = blocks.CharBlock(required=True, max_length=50)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)  # Internal link
    button_url = blocks.URLBlock(required=False)  # External link
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=20)

    class Meta:
        template = 'streams/cta_block.html'
        icon = "doc-full"
        label = 'Call To Action'
