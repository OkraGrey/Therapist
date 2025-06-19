from django.contrib import admin
from .models import Form, Question, ChoiceOption, Submission, Answer


class ChoiceOptionInline(admin.TabularInline):
    model = ChoiceOption
    extra = 1
    ordering = ["order"]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    ordering = ["order"]
    inlines = [ChoiceOptionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "text_answer", "choice_answer", "range_answer")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("form", "email", "submitted_at", "answer_count")
    list_filter = ("submitted_at", "form")
    search_fields = ("form__name", "email")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)
    inlines = [AnswerInline]

    def answer_count(self, obj):
        return obj.answers.count()

    answer_count.short_description = "Answers"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "answer_display")
    list_filter = ("question__type", "submission__form")
    search_fields = ("submission__form__name", "question__text")
    readonly_fields = (
        "submission",
        "question",
        "text_answer",
        "choice_answer",
        "range_answer",
    )

    def answer_display(self, obj):
        if obj.text_answer:
            return f"Text: {obj.text_answer[:50]}..."
        elif obj.choice_answer:
            return f"Choice: {obj.choice_answer.text}"
        elif obj.range_answer:
            return f"Range: {obj.range_answer}/5"
        return "No answer"

    answer_display.short_description = "Answer"
