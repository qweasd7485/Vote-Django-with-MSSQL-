from django.contrib import admin
from polls.models import Question, Choice, Voted, VoteHistory
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None                  , {'fields': ['question_text']}),
        ('Revoteable(可否重複投票)', {'fields': ['revoteable']}),
        ('Ballots(最高3票)'      , {'fields': ['ballot'] }),
        ('Date information'    , {'fields': ['pub_date'], 'classes': ['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'revoteable', 'ballot', 'pub_date') 
    
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Voted)
admin.site.register(VoteHistory)