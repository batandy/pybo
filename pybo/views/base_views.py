from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer, Category

def index(request, category_name='qna'):
    """
    pybo 목록출력
    """
    # 입력인자
    page=request.GET.get('page', '1')
    kw=request.GET.get('kw', '')

    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    # 조회
    question_list=Question.objects.filter(top_fixed=False).order_by('-create_date')
    if kw:
        question_list=question_list.filter(
            Q(subject__icontains=kw) |                     # 제목 검색
            Q(content__icontains=kw) |                     # 내용 검색
            Q(author__username__icontains=kw) |            # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)      # 답변 글쓴이 검색
        ).distinct()
    
    question_list=question_list.filter(category=category)
    
    # 페이징 처링
    paginator = Paginator(question_list,10)    #페이지당 10개씩 보여주기
    page_obj=paginator.get_page(page)
    max_page=len(paginator.page_range)

    #공지사항 리스트
    if kw:
        notice_fixed = None
    else:
        notice_fixed=Question.objects.filter(top_fixed=True).order_by('create_date')
    notice_fixed=notice_fixed.filter(category=category)

    context={'question_list': page_obj, 'page': page, 'kw': kw, 'max_page':max_page, 'notice_fixed':notice_fixed, 'category_list': category_list, 'category': category}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id, category_name):
    """
    pybo 내용 출력
    """
    question=get_object_or_404(Question, pk=question_id)
    category = get_object_or_404(Category, name=category_name)
    question.update_counter
    sort=request.GET.get('sort', '최신순')
    if sort =='최신순':
        answer_list = Answer.objects.all().order_by('-create_date')
    else:
        answer_list = Answer.objects.annotate(like_count=Count('voter')).order_by('-like_count', '-create_date')

    context={'question':question, 'answer_list':answer_list, 'category':category}
    return render(request, 'pybo/question_detail.html', context)