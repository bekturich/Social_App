from .models import Post
from modeltranslation.translator import TranslationOptions, register

@register(Post)
class PostTranslationOp(TranslationOptions):
    fields = ['description']

