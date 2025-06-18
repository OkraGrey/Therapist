from django.contrib import admin
from .models import Form, Question, ChoiceOption


class ChoiceOptionInline(admin.TabularInline):
    model = ChoiceOption
    extra = 1
    ordering = ["order"]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    ordering = ["order"]
    inlines = [ChoiceOptionInline]


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "form", "type", "is_mandatory", "order")
    list_filter = ("type", "is_mandatory", "form")
    search_fields = ("text", "form__name")
    ordering = ("form", "order")
    inlines = [ChoiceOptionInline]


@admin.register(ChoiceOption)
class ChoiceOptionAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "order")
    list_filter = ("question__form", "question__type")
    search_fields = ("text", "question__text")
    ordering = ("question", "order")
