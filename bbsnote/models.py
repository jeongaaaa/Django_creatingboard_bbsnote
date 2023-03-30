from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.id}] {self.subject}' 

#models.Model을 상속하는 새로운 클래스인 Comment를 정의. 이 클래스는 데이터베이스 테이블
class Comment(models.Model):
    #외래키 필드인 Board를 정의. 이 필드는 Board 모델과 관계있음
    #on_delete 옵션은 Board 객체가 삭제될 때 관련된 Comment 객체도 함께 삭제되도록 지정
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    #Comment 클래스의 속성으로 텍스트 필드 content를 정의
    content = models.TextField()
    #ForeignKey로 User 모델과 연결하고 on_delete=models.CASCADE는 User 객체가 삭제될 때 이 객체도 함께 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #blank=True=>DB에서는 not null 조건으로 되어있지만, blank=True 조건을 써주면 값을 비워놔도 오류x(null허용)=>like가 필수조건이 아니게 되는 것
    ##like = models.IntegerField(blank=True, default=0)
    #객체가 처음 생성될 때 자동으로 현재 날짜/시간으로 설정
    create_date = models.DateTimeField(auto_now_add=True)
    #객체가 저장될 때마다 자동으로 현재 날짜/시간으로 갱신
    update_date = models.DateTimeField(auto_now=True)

    #댓글 순서 최신순 정렬
    class Meta:
        ordering = ['-create_date']


    def __str__(self):
        return f'[{self.board.id}] {self.content}'