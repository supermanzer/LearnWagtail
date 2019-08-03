from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
)
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm, AbstractFormField
)
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ContactPage(WagtailCaptchaEmailForm):

    template = 'contact/contact_page.html'
    landing_page_template = 'contact/contact_page_landing.html'

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', heading='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col s6'),
                FieldPanel('to_address', classname='col s6'),
            ]),
            FieldPanel('subject')
        ], heading='Email Settings'),
    ]
