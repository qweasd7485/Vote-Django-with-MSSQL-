from django import template
from polls.models import Question, Choice, Voted

register = template.Library()

@register.simple_tag
def voted_query(question_id, account_id):
    try:
        voted_list = Voted.objects.get(question=question_id, account=account_id)
        if voted_list.votetimes > 0:
            return "1"
    except (KeyError, Voted.DoesNotExist):
        return "0"    
    return "0" 