from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Define default number of choices for a new question."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Define default fields and values for a new question."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],
                              'classes': ['collapse']}),
        ('End Date information', {'fields': ['end_date'],
                                  'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)

# Solution 1 (inefficient) for adding Choice
# admin.site.register(Choice)
