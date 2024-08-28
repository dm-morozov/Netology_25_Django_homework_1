from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self) -> None:
        main_tags_count = sum(1 for form in self.forms if form.cleaned_data.get('is_main'))
        if main_tags_count > 1:
            raise ValidationError('Основной тег может быть только один')
        elif main_tags_count == 0:
            raise ValidationError('У статьи должен быть один основной тег')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)