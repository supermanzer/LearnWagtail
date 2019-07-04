# -*- coding: utf-8 -*-
"""
Content Block Definitions

This file defines custom stream field blocks.
"""
from wagtail.core import blocks


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, help_text='Add your title', max_length=100)
    text = blocks.TextBlock(required=True, help_text='Add additional text.')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


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
