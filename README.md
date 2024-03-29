#### 클리앙 앱 (Clien app) 공부
-----------

## 개발 언어
- Python 3.x

## 라이브러리
- Selenium: https://selenium-python.readthedocs.io

## 필수 설치
Python - 다운로드/설치후 재부팅 권장
- https://www.python.org/downloads/

Selenium- Python3 설치후 아래의 명령어 실행 권장
- pip install selenium
- 또는 python -m pip install selenium

## 실행

### URL 수집 - backup.txt 에 저장
```
 url_collect.py --file backup.txt
```
사용자이름/비밀번호 입력창이 나오는건.. 로그인을 해야 사용자 정보 수집이 가능합니다. \
사이트 로그인 할떄만 사용하니, 걱정 하지 않으셔도 되요.\
backup.txt 파일에 url 을 저장 합니다. 다른 능력 있으신분들의 크롤링을 사용 하셔도 됩니다.

### Download url page - 크롤링
- --url_file backup.txt : 위에서 저장한 URL 파일이름
- --save ./save: 저장할 디렉토리
```
download_url.py --url_file backup.txt --save ./save
```
