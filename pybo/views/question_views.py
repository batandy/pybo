from logging.handlers import QueueListener
from unicodedata import category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question, Category


@login_required(login_url='common:login')
def question_create(request,category_name):
    """
    pybo 질문등록
    """
    category = Category.objects.get(name=category_name)
    if request.method == 'POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.author=request.user
            question.create_date=timezone.now()
            if len(request.POST.getlist('top_fixed'))!=0:
                question.top_fixed=True
            else: question.top_fixed=False
            question.category = category
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form,'category':category}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form=QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            if len(request.POST.getlist('top_fixed'))!=0:
                question.top_fixed=True
            else: question.top_fixed=False
            question.save()
            return redirect('pybo:detail', question_id=question.id, category_name=question.category)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'category':question.category}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')