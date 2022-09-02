from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer

def index(request):
    """
    pybo 목록출력
    """
    # 입력인자
    page=request.GET.get('page', '1')
    kw=request.GET.get('kw', '')
    # 조회
    question_list=Question.objects.filter(top_fixed=False).order_by('-create_date')
    if kw:
        question_list=question_list.filter(
            Q(subject__icontains=kw) |                     # 제목 검색
            Q(content__icontains=kw) |                     # 내용 검색
            Q(author__username__icontains=kw) |            # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)      # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처링
    paginator = Paginator(question_list,10)    #페이지당 10개씩 보여주기
    page_obj=paginator.get_page(page)
    max_page=len(paginator.page_range)

    #공지사항 리스트
    notice_fixed = Question.objects.filter(top_fixed=True).order_by('create_date')

    context={'question_list': page_obj, 'page': page, 'kw': kw, 'max_page':max_page, 'notice_fixed':notice_fixed}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question=get_object_or_404(Question, pk=question_id)
    question.update_counter
    sort=request.GET.get('sort', '최신순')
    if sort =='최신순':
        answer_list = Answer.objects.all().order_by('-create_date')
    else:
        answer_list = Answer.objects.annotate(like_count=Count('voter')).order_by('-like_count', '-create_date')

    context={'question':question, 'answer_list':answer_list}
    return render(request, 'pybo/question_detail.html', context)