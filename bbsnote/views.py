from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

#첫번째 뷰 함수 index를 정의. HTTP 요청 객체인 request를 인자로 받음
def index(request):
    # 입력인자
    page = request.GET.get('page', 1)
    # 조회
    #데이터베이스에서 Board 객체 목록을 가져옴. 이 목록은 생성 날짜의 역순으로 정렬
    #order_by에서 -를 붙이면 내림차순. 안 붙이면 오름차순.
    board_list = Board.objects.order_by('-create_date')
    # 페이징처리
    #board_list는 페이지로 나눌 데이터 목록이고 3은 한 페이지에 표시할 항목 수
    paginator = Paginator(board_list, 3)
    #get_page 메소드는 페이지 번호를 받아 해당 페이지를 리턴
    page_obj = paginator.get_page(page)
    #컨텍스트 변수. 템플릿에 전달되어 렌더링에 사용
    #page_obj 데이터를 context에 담음
    context = {'board_list': page_obj}
    ## return HttpResponse("bbsnote에 오신 것을 환영합니다")
    #템플릿 파일 'bbsnote/board_list.html'을 렌더링하여 HTTP 응답 객체를 반환
    return render(request, 'bbsnote/board_list.html', context)

def detail(request, board_id):
    board = Board.objects.get(id=board_id)    
    context = {'board': board}
    return render(request, 'bbsnote/board_detail.html', context)

#사용자가 로그인하지 않은 상태에서 이 뷰 함수에 접근하려고 할 때 common:login으로 지정된 URL로 리다이렉트
@login_required(login_url='common:login')
#request와 board_id라는 두개의 인자를 받음
def comment_create(request, board_id):
    #'Not NULL constraint failed' 오류 해결
    #POST인 경우에만 다음 코드 실행
    if request.method == 'POST':
        #Board 모델에서 id가 board_id와 일치하는 객체를 가져와서 board 변수에 저장
        board = Board.objects.get(id=board_id)
        ## comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
        ## comment.save()
        #content=request.POST.get('content'); content 필드를 요청의 POST 데이터에서 'content' 키의 값을 가져와서 설정
        #create_date=timezone.now(); create_date 필드를 현재 시간으로 설정
        #author=request.user; 현재 로그인한 사용자의 인스턴스를 가져와서 author 필드에 설정
        board.comment_set.create(content=request.POST.get('content'), create_date=timezone.now(), author=request.user)
        ## return redirect('bbsnote:detail', board_id=board.id)
    #'bbsnote:detail'으로 지정된 URL으로 리다이렉트. 인자로 board_id가 전달
    return redirect('bbsnote:detail', board_id=board_id)


@login_required(login_url='common:login')
def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            # board.create_date = timezone.now()
            board.author = request.user
            board.save()
            return redirect('bbsnote:index')
    else:
        form = BoardForm()
    return render(request, 'bbsnote/board_form.html', {'form':form})

@login_required(login_url='common:login')
def board_modify(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user 
            board.save()
            return redirect('bbsnote:detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)
    context = {'form': form}
    return render(request, 'bbsnote/board_form.html', context)


@login_required(login_url='common:login')
def board_delete(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    board.delete()
    return redirect('bbsnote:index')

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "수정 권한이 없습니다!")
        return redirect('bbsnote:detail', board_id=comment.board.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  
            comment.save()
            return redirect('bbsnote:detail', board_id=comment.board.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment':comment, 'form':form}
    return render(request, 'bbsnote/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제 권한이 없습니다!")
        return redirect('bbsnote:detail', board_id=comment.board.id)
    comment.delete()
    return redirect('bbsnote:detail', board_id=comment.board.id)
