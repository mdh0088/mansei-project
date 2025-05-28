# mansei-project



### 개발 환경 실행
###### 1. 개발용 docker 환경 시작
```shell
docker-compose -f docker-compose.dev.yml up -d
```
###### 2. 데이터베이스 마이그레이션 (백엔드 컨테이너가 실행된 후)
```shell
docker-compose -f docker-compose.dev.yml exec backend uv run alembic upgrade head
```
###### 3. 로그 확인
```shell
docker-compose -f docker-compose.dev.yml logs -f
```

### 프로덕션 환경 실행
###### 1. 환경변수 설정

- `.env` 파일을 실제 프로덕션 값으로 편집
```shell
cp .env.example .env
```
###### 2. 프로덕션 환경 시작
```shell
docker-compose up -d
```
###### 3. 데이터베이스 마이그레이션
```shell
docker-compose exec backend uv run alembic upgrade head
```

### 빠른 수정 방법

###### 1. 현재 docker 컨테이너들 중지
```shell
docker-compose -f docker-compose.dev.yml down
```

###### 2. docker 이미지 재빌드
```shell
docker-compose -f docker-compose.dev.yml build --no-cache
```

###### 3. 서비스 재시작
```shell
docker-compose -f docker-compose.dev.yml up -d
```

###### 4. 로그 확인
```shell
docker-compose -f docker-compose.dev.yml logs -f
```

### 특정 서비스만 재시작 (예 : backend)
###### 1. backend만 내리기
```shell
docker-compose -f docker-compose.dev.yml stop backend
```

혹은 컨테이너 완전 히제거
```shell
docker-compose -f docker-compose.dev.yml rm -f backend
```
###### 2. backend만 빌드
```shell
docker-compose -f docker-compose.dev.yml build backend
```
###### 3. backend만 실행
```shell
docker-compose -f docker-compose.dev.yml up -d backend
```
###### backend 로그만 보기
```shell
docker-compose -f docker-compose.dev.yml logs -f backend
```
### docker-compose로 관리 중인 컨테이너 리스트 보기
```shell
docker-compose -f docker-compose.dev.yml ps
```

### alembic 을 사용한 테이블 생성

###### 1. migration 파일 재생성
```shell
docker-compose -f docker-compose.dev.yml exec backend uv run alembic revision --autogenerate -m "init"
```
###### 2, migration 적용
```shell
docker-compose -f docker-compose.dev.yml exec backend uv run alembic upgrade head
```
###### 3. 테이블 재확인
```shell
docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d mansei_dev -c "\dt"
```

