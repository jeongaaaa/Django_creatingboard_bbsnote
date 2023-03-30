#Django의 템플릿 모듈을 가져옴
from django import template

#템플릿 라이브러리의 인스턴스를 생성하고 register 변수에 할당
register = template.Library()

#@=annotation=>template함수로 쓸 수 있게 template engine으로 등록시켜주라는 뜻 -> backend에서 보는 주석 
#register.filter 데코레이터를 사용하여 다음에 정의되는 함수를 템플릿 필터로 등록
@register.filter
#sub라는 이름의 필터 함수를 정의 (사용자정의함수)
def sub(value, arg):
    #두 인수의 차를 return
    return value - arg 


#템플릿 필터란 템플릿 태그에서 | 문자 뒤에 사용하는 필터를 말한다. 
#다음 예처럼 default_if_none과 같은 것들을 템플릿 필터라고 한다.
#{{ form.subject.value|default_if_none:'' }}

#만약 첫번째 게시물 전체 건수가 12개라면 첫번째 페이지는 번호가 12~3 까지의 역순으로 보여지고 두번째 페이지에는 2~1까지 보여져야 한다. 이렇게 페이지별로 게시물의 번호를 역순으로 정렬하려면 다음과 같은 공식을 적용해야 한다. 

#번호 = 전체건수 - 시작인덱스 - 현재인덱스 + 1
#시작인덱스는 페이지당 시작되는 게시물의 시작 번호를 의미한다. 
#예를 들어 페이지당 게시물을 10건씩 보여준다면 1페이지의 시작 인덱스는 1, 2페이지의 시작 인덱스는 11이 된다. 현재 인덱스는 페이지에 보여지는 게시물 개수만큼 0부터 1씩 증가되는 번호이다. 따라서 전체 게시물 개수가 12개이고 페이지당 10건씩 게시물을 보여준다면 공식에 의해 1페이지의 번호는 12 - 1 - (0~9 반복) + 1 이 되어 12~3까지 표시되고 2페이지의 경우에는 12 - 11 - (0~1 반복) + 1 이 되어 2~1이 표시될 것이다.

#템플릿에서 이 공식을 적용하려면 빼기 기능이 필요하다. 앞에서 더하기 필터(|add:5)를 사용한 것처럼 빼기 필터(|sub:3)가 있으면 좋을 것 같다. 하지만 장고에는 빼기 필터가 없다. 그래서 우리는 빼기 필터를 직접 만들 것이다.

# |add:-3와 같이 숫자를 직접 입력하면 더하기 필터를 이용하여 원하는 값을 뺀 결과를 화면에 보여줄 수는 있다. 하지만 이 방법은 이곳에는 사용할 수 없다. 왜냐하면 add 필터에는 변수를 적용할 수 없기 때문이다.

#add 필터는 인수로 숫자만 가능하다.