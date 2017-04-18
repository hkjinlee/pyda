# 프로젝트 개요
- python을 이용한 데이터분석 실습용 프로젝트
- IDE로는 [Spyder](https://github.com/spyder-ide/spyder)를 사용

# 프로젝트 이용 환경
## Mac OS/X
- (anaconda)[https://www.continuum.io/downloads] 환경을 이용

# Spyder 이용하기
## 주요 개념
### Code cell
![spyder_codecell.png]
- 한꺼번에 실행되어야 하는 코드의 묶음(block)
  - 위 스크린샷에는 총 4개의 code cell이 존재. 노란 셀이 현재 active상태
- #%%로 시작하여 다음 #%%가 나올때까지가 하나로 묶임
- Shift+Enter로 한꺼번에 실행

## 패키지 설치
- IPython 콘솔에서 !pip install [패키지이름]

## 핫키(shortcut)
### 창 이동
- cmd+shift+E: 에디터
- cmd+shift+I: IPython 콘솔
- cmd+shift+C: Python 콘솔
- cmd+shift+V: 변수 탐색기
- cmd+shift+H: 도움말

### 코드 실행
- 블럭설정 뒤 cmd+Enter: 
현재 선택된 블럭 실행
- shift+Enter: 현재 code cell 실행
