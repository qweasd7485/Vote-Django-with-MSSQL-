from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from polls.models import Question, Choice, Voted, VoteHistory
import datetime



# Create your views here.
@login_required
def index(request):
    latest_question_list = Question.objects.all()  #取得所有問題
    #voted_list = Voted.objects.filter(account=request.user.id).order_by('account', 'question')
    #print(request.user.fullName)
    #print(datetime.datetime.now())
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id): 
    vote_able = voteable(question_id, request.user.id) #取得該使用者是否確實該議題具有該次投票權
    if vote_able == 1 :  #回傳為1代表具有該次投票權
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})
    elif vote_able == 0 :    #回傳為01代表不具有該次投票權
        messages.error(request, '該議題已經投過!')
        return render(request, 'main/main.html')
    messages.error(request, '獲取「投票權」出現錯誤，煩請回報議題與使用者至系統管理員(code99)。') #0與1以外回傳問題碼
    return render(request, 'main/main.html')

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)    
    
    question_ballot = Question.objects.get(id=question_id).ballot
    
    if question_ballot == 1:
        try:
            selected_choice = p.choice_set.get(pk=request.POST['choice'])
            #print(selected_choice.choice_text)
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html',{
                'question': p,
                'error_message': "~請選擇一個項目以進行投票~",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            votetimes_add(question_id, request.user.id)  #記錄該問題該使用者投票幾次
            votehistory_add(question_id, request.user.id, selected_choice.id, request.user.fullName, selected_choice.choice_text)#直接紀錄該使用者該議題該選項投過1次
            return HttpResponseRedirect(reverse('polls:results', args={p.id,}))
    elif question_ballot > 1: #可投票數>1時
        #print(request.POST.getlist('choice'))    
        selected_choices = request.POST.getlist('choice')       #回傳使用者有選的選項值範例：['6', '7']
        if len(selected_choices) > question_ballot :
            messages.error(request, '實際投票超過該議題單次可投票數！')    #使用者實際投票超過該議題單次可投票數
            return render(request, 'polls/detail.html' , {'question': p})
        elif len(selected_choices) > 0 and len(selected_choices) < question_ballot:
            messages.error(request, '並未投票滿可投票數！')
            return render(request, 'polls/detail.html' , {'question': p})
        elif len(selected_choices) <=  0:
            messages.error(request, '並未投票！')
            return render(request, 'polls/detail.html' , {'question': p})
        
        for choice in selected_choices:                         #迴圈將使用者選取的項目至資料庫將該選項票數+1
            selected_choice = Choice.objects.get(id=choice)
            selected_choice.votes += 1
            selected_choice.save()
            votehistory_add(question_id, request.user.id, choice, request.user.fullName, selected_choice.choice_text) #直接紀錄該使用者該議題該選項投過1次
        votetimes_add(question_id, request.user.id)             #資料庫紀錄該使用使該議題投過次數+1        
        return HttpResponseRedirect(reverse('polls:results', args={p.id,}))
    
    
    
def voteable(question_id, account_id): #取得該使用者是否確實該議題具有投票權
    try:
        revoteable = Question.objects.get(id=question_id).revoteable   #該議題是否可以多次投票
        votetimes = Voted.objects.get(question=question_id, account=account_id).votetimes #該使用者該議題投過幾次    
        if revoteable == False and votetimes >= 1:   #該議題不能多次投票且已經投過
            return 0
        else:
            return 1
    except (KeyError, Voted.DoesNotExist):  #資料庫中不存在代表該議題尚未投過
        return 1


def votetimes_add(question_id, account_id): #記錄使用者該問題投過次數
    #先查已經有沒有投過     
    try:
        voted_list = Voted.objects.get(question=question_id, account=account_id)
        if voted_list.votetimes >= 0:   #資料表已存在該使用者於該議題
            voted = 1
    except (KeyError, Voted.DoesNotExist):
        voted = -1   
    
    #逐一進行次數新增或+1
    if voted == 1:
        voted_list.votetimes += 1
        voted_list.save()
    else:
        Voted.objects.create(question=question_id, account=account_id, votetimes=1)
        
def votehistory_add(question_id, account_id, choice_id, account_name, choice_content):   #直接紀錄該使用者該議題該選項投過1次    
    VoteHistory.objects.create(question=question_id, account=account_id, choice=choice_id, create_date=datetime.datetime.now(), content=account_name + ' ' + choice_content)
        
        
    

    
