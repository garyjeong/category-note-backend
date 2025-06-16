FROM mysql:8.0

# 환경 변수 설정
ENV MYSQL_ROOT_PASSWORD=wjdwhdans
ENV MYSQL_DATABASE=category_note
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=wjdwhdans

# MySQL 설정 파일 복사
COPY ./database/my.cnf /etc/mysql/conf.d/my.cnf

# 초기 스크립트 디렉토리 설정
VOLUME /var/lib/mysql

# MySQL 포트 노출
EXPOSE 3306

# MySQL 문자셋 설정 (한국어 지원)
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

CMD ["mysqld"] 