# MATH BANK
<br>

## 개발 도구
- PyCharm
<br>

## 개발 환경
- Flask 1.1.1
- SQLITE 3
- Jinja2 2.10.1
- Bootstrap 4.3
<br>

## 하드웨어 환경
- MAC OS
<br>

## 실행 방법
(실 코드에서는 정보 유출 위험이 있어 호스팅된 DB의 접속경로를 표시하지 않아 DB 부분은 표시되지 않습니다.(database.py))
1. main.py를 실행시킵니다.(이 때, 실행이 안될 경우, app.debug=True를 주석처리하고 재실행합니다.)

2. 로그인 화면이 표시됩니다. 로그인은 (ID : admin, PW: 1234)로 해줍니다.(미리 설정한 값)

![로그인](https://user-images.githubusercontent.com/52739724/68653370-f26d1d00-056e-11ea-8bd1-4e51cf4e4b70.jpg)

3. 메인 화면이 표시됩니다.(허전하지만 뭘 넣을지 고민 중입니다.)

![메인](https://user-images.githubusercontent.com/52739724/68653769-c8682a80-056f-11ea-8e1a-cccbcc91acf5.jpg)

4. 회원 목록 탭을 클릭하면 회원 목록과 각 회원의 채팅 보기를 클릭하면 그 회원의 채팅을 볼 수 있습니다.(다른 프로젝트(챗봇)에 협업 중인 DB를 가져옵니다.)

![회원 목록](https://user-images.githubusercontent.com/52739724/68653779-cc944800-056f-11ea-9865-ef257d320836.jpg)


![회원 목록-채팅 보기](https://user-images.githubusercontent.com/52739724/68653782-cdc57500-056f-11ea-8751-dc400acfa4e0.jpg)

5. 의도 탭을 클릭하면 그에 따른 통계가 그래프로 표시됩니다.

![의도](https://user-images.githubusercontent.com/52739724/68653785-cf8f3880-056f-11ea-91e0-4b3ba5a0bec6.jpg)

6. 개체명 탭을 클릭하면 개체명에 따른 통계가 표시됩니다.

![개체명](https://user-images.githubusercontent.com/52739724/68653788-d0c06580-056f-11ea-98cb-7c3bf2024b3a.jpg)

7. 로그아웃을 누르면 세션이 끊기면서 로그아웃되고 다시 로그인 페이지로 돌아갑니다.
