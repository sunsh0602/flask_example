brew install mysql
brew services start mysql
mysql_secure_installation

mysql -u root -p 
password

create database toy_project;
create user 'admin'@'localhost' identified by 'password';
grant all privileges on toy_project.* to 'admin'@'localhost';
flush privileges;



flask 설정
PIP 패키지 설치
# mysql 연결
pip install mysqlclient
# orm 사용
pip install -U Flask-SQLAlchemy
# flask migrate 기능 사용
pip install Flask-Migrate
# dotenv 보안을 위해 사용
pip install python-dotenv



python -c 'import secrets; print(secrets.token_hex())' 
# 터미널에 입력하면 다음과 같이 secret key에 사용할 토큰이 생성됩니다



.env 파일 생성
# normal
SECRET_KEY='02640a6a320bd20a02aaefa29329acddb70b7144e0d75d5c6348d0daf5e12ba5'

# database develop
DB_USER='admin'
DB_PWD='password'
DB_HOST='127.0.0.1'
DB_PORT='3306'
DB_NAME='toy_project'

# database product
DB_PRODUCT_USER='admin'
DB_PRODUCT_PWD='password'
DB_PRODUCT_HOST='127.0.0.1'
DB_PRODUCT_HOST='127.0.0.1'
DB_PRODUCT_PORT='3306'
DB_PRODUCT_NAME='toy_project'



생성한 모델 db 생성 및 migrate
터미널에서 다음 순서대로 입력합니다

flask db init
flask db migrate
flask db upgrade