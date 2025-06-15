FROM mysql:8.0

# 환경 변수 설정
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=category_note
ENV MYSQL_USER=category_user
ENV MYSQL_PASSWORD=category_password

# MySQL 설정 파일 복사
COPY ./database/my.cnf /etc/mysql/conf.d/my.cnf

# 초기 스크립트 디렉토리 설정
VOLUME /var/lib/mysql

# MySQL 포트 노출
EXPOSE 3306

# 한국어 환경 설정
RUN apt-get update && apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR:ko
ENV LC_ALL ko_KR.UTF-8

CMD ["mysqld"] 