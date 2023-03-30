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

#로그인이 되어 있지 않으면 'common:login' URL로 리디렉션
@login_required(login_url='common:login')
#board_modify라는 함수 정의. request와 board_id 두개의 인수를 받고
def board_modify(request, board_id):
    #Board 모델에서 pk가 board_id인 객체를 가져오고 해당 객체가 업스면 404에러 페이지 표시
    board = get_object_or_404(Board, pk=board_id)
    #만약 요청이 게시물의 작성자가 아니면 아래 코드 실행
    if request.user != board.author:
        #에러메세지
        messages.error(request, '수정권한이 없습니다')
        #'bbsnote:detail' URL로 리디렉션
        return redirect('bbsnote:detail', board_id=board.id)
    #만약 요청이 POST이면 아래 코드 실행(GET방식일때와 POST방식일때를 구분해줘야 함)
    if request.method == "POST":
        #BoardForm이라는 폼 클래스의 인스턴스를 생성하고 request.POST와 board 객체를 사용하여 초기화
        form = BoardForm(request.POST, instance=board)
        #만약 폼이 유효하면 아래 코드 실행
        if form.is_valid():
            #폼 데이터로 board 객체를 업데이트. commit=False로 데이터베이스에 변경 사항을 저장하지 않도록 함
            board = form.save(commit=False)
            #board 객체의 author 속성을 요청을 보낸 사용자로 설정
            board.author = request.user 
            #변경 사항을 데이터베이스에 저장
            board.save()
            #'bbsnote:detail' URL로 리디렉션되고 board_id라는 인수 필요
            return redirect('bbsnote:detail', board_id=board.id)
    else:
        #BoardForm이라는 폼 클래스의 인스턴스 생성
        form = BoardForm(instance=board)
    #템플릿에서 사용할 수 있는 데이터를 포함하는 딕셔너리
    context = {'form': form}
    #'bbsnote/board_form.html' 템플릿을 렌더링하고 HTTP 응답 반환. 컨텍스트 변수를 사용하여 렌더링
    return render(request, 'bbsnote/board_form.html', context)


#로그인이 되어있지 않으면 'common:login' URL로 리디렉션
@login_required(login_url='common:login')
#board_delete라는 함수 request와 board_id 인수 받음
def board_delete(request, board_id):
    #객체 없으면 404에러 페이지 표시
    board = get_object_or_404(Board, pk=board_id)
    #요청을 보낸 사용자가 게시물 작성자가 아니면 아래 코드 실행
    if request.user != board.author:
        #에러메세지
        messages.error(request, '삭제 권한이 없습니다')
        #'bbsnote:detail'로 리디렉션
        return redirect('bbsnote:detail', board_id=board.id)
    #데이터베이스에서 삭제
    board.delete()
    #'bbsnote:index'로 리디렉션
    return redirect('bbsnote:index')

#로그인이 되어있지 않으면 'common:login' URL로 리디렉션
@login_required(login_url='common:login')
#comment_modify라는 함수 request와 board_id 인수 받음
def comment_modify(request, comment_id):
    #해당 객체 없으면 404에러 페이지 표시
    comment = get_object_or_404(Comment, pk=comment_id)
    #만약 요청의 사용자가 댓글의 작성자가 아니면 아래 코드 실행
    if request.user != comment.author:
        #에러메세지
        messages.error(request, "수정 권한이 없습니다!")
        #'bbsnote:detail' URL로 리디렉션
        return redirect('bbsnote:detail', board_id=comment.board.id)
    #만약 요청이 'POST'이면 아래 코드 실행
    if request.method == "POST":
        #CommentForm이라는 폼 인스턴스를 생성. request.POST와 comment 객체로 초기화
        form = CommentForm(request.POST, instance=comment)
        #만약 폼이 유효하면 아래 코드 실행
        if form.is_valid():
            #폼 데이터를 사용하여 comment 객체를 업데이트. 데이터베이스에 변경 사항 저장 안함
            comment = form.save(commit=False)
            #comment 객체의 author 속성을 요청을 보낸 사용자로 설정
            comment.author = request.user  
            #변경 사항을 데이터베이스에 저장
            comment.save()
            #'bbsnote:detail' URL로 리디렉션
            return redirect('bbsnote:detail', board_id=comment.board.id)
    else:
        #CommentForm이라는 폼 클래스의 인스턴스 생성
        form = CommentForm(instance=comment)
    #템플릿에서 사용할 수 있는 데이터를 포함하는 딕셔너리
    context = {'comment':comment, 'form':form}
    #'bbsnote/comment_form.html' 템플릿을 렌더링하고 HTTP 응답을 반환. 컨텍스트 변수를 사용하여 렌더링
    return render(request, 'bbsnote/comment_form.html', context)

#로그인이 되어있지 않으면 'common:login' URL로 리디렉션
@login_required(login_url='common:login')
#comment_delete라는 함수 request와 comment_id 인수 받음
def comment_delete(request, comment_id):
    #해당 객체 없으면 404에러 페이지 표시
    comment = get_object_or_404(Comment, pk=comment_id)
    #만약 요청의 사용자가 댓글의 작성자가 아니면 아래 코드 실행
    if request.user != comment.author:
        #에러메세지
        messages.error(request, "삭제 권한이 없습니다!")
        #'bbsnote:detail' URL로 리디렉션
        return redirect('bbsnote:detail', board_id=comment.board.id)
    #객체를 데이터베이스에서 삭제
    comment.delete()
    #'bbsnote:detail' URL로 리디렉션
    return redirect('bbsnote:detail', board_id=comment.board.id)
