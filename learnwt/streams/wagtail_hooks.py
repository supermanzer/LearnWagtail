# -*- coding: utf-8 -*-
"""
Using wagtail hooks to extend richtext editor

<code> - an inline element style
<center> - a block style
"""
from wagtail.core import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler
)


@hooks.register('register_rich_text_features')
def register_code_styling(features):
    """Add <code> to rich text editor"""
    # Initial variables
    feature_name = "code"
    type_ = "CODE"
    tag = "code"  # <code>
    # Navbar configuration
    control = {
        'type': type_,
        'label': '</>',
        'description': 'Code',
    }
    # Register this feature with draftail
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )
    # Define how data is stored in DB and retrieved
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {"element": tag}}}
    }
    # Register the DB handling parameters
    features.register_converter_rule('contentstate', feature_name, db_conversion)
    # Register with all Richtext editors by default
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_center_text_feature(features):
    """Create centered text in our richtext."""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"  # Creates <div> element
    # This defines how Draftail will represent this block, NOT how it will be
    # output to the page.
    control = {
        "type": type_,
        "label": "Center",
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center",
        },
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {
            'style_map': {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "center-align ZZZZZTESTZZZZZZ",
                        # "style": "text-align: center;"
                    }
                }
            }
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)
