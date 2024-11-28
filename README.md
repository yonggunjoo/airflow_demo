# Airflow 기술 확보 프로젝트 계획

## 1. Airflow 핵심 기능 설명

### 1.1 기본 구성 요소
Airflow의 핵심인 DAG(Directed Acyclic Graph)는 워크플로우를 정의하는 기본 단위입니다. DAG는 다음과 같은 주요 구성요소를 포함합니다:

- Operators: 개별 작업을 정의하며, BashOperator, PythonOperator 등이 있습니다
- Tasks: DAG 내에서 Operator가 수행하는 구체적인 작업입니다
- Task Dependencies: `>>`, `<<` 연산자를 사용하여 작업 간 의존성을 정의합니다

### 1.2 스케줄링 시스템
Airflow는 두 가지 방식으로 실행 일정을 관리합니다:

- Cron 표현식: `0 12 * * *`와 같은 형식으로 정확한 실행 시간을 지정합니다
- 시간 간격: `@daily`, `@hourly`와 같은 미리 정의된 간격을 사용합니다

### 1.3 실행 관리
워크플로우 실행은 다음과 같은 방식으로 관리됩니다:

- Trigger: 수동 또는 예약된 실행이 가능합니다
- Backfill: 과거 날짜의 작업을 실행할 수 있습니다
- Catchup: 누락된 DAG 실행을 자동으로 보완합니다

### 1.4 오류 관리
시스템은 다음과 같은 오류 처리 메커니즘을 제공합니다:

- Retries: 작업 실패 시 자동으로 재시도합니다
- Alerts: 이메일이나 Slack을 통해 오류 알림을 전송합니다

## 2. 프로젝트 정의

### 2.1 프로젝트 목표
이 프로젝트는 다음과 같은 목표를 달성하고자 합니다:

- Apache Airflow를 활용한 데이터 파이프라인 자동화 기술 확보
- 실무에 즉시 적용 가능한 데모 시스템 구축
- 팀 내 기술 역량 강화 및 지식 공유 체계 확립

### 2.2 프로젝트 범위
프로젝트는 다음 영역을 포함합니다:

- Airflow 핵심 기능의 분석 및 문서화
- 로컬 환경 기반의 데모 시스템 구현
- Gmail 기반 알림 시스템 구축

### 2.3 기대 효과
프로젝트 완료 시 다음과 같은 효과를 기대할 수 있습니다:

- 데이터 파이프라인 자동화를 통한 업무 효율성 향상
- 안정적인 워크플로우 관리 체계 확립
- 신속한 장애 대응 능력 확보

## 3. 구현 세부사항

### 3.1 기술 문서 작성
문서화는 다음 세 가지 영역을 중점적으로 다룹니다:

1. 아키텍처 분석
   - 핵심 컴포넌트 구조 설명
   - DAG 실행 프로세스 문서화
   - 스케줄러 동작 방식 정리

2. 주요 기능
   - DAG 설계 및 구현 방법론
   - Operator 종류별 활용 가이드
   - 태스크 의존성 관리 방안
   - 오류 처리 및 재시도 메커니즘

3. 환경 설정
   - Docker 기반 설치 절차

### 3.2 데모 시스템 구현
시스템 구현은 다음과 같은 단계로 진행됩니다:

1. 환경 구성
- 사전 설치
  - vscode
  - python
  - docker
  - airflow:2.9.3

1. 워크플로우 구현
   - Dags
     - [api_data_pipeline](dags/api_data_pipeline.py) : 하나의 API 호출하고 성공 메시지 발송
     - [parallel_api_pipeline](dags/parallel_api_pipeline.py)
       - 1건의 API 병렬처리로 발송 
       - 1건 성공 메일, 1건 실패 메일 발송
       - 실패시 1번의 retry 시도하고, 실패 시 실패 메일 발송
   - API 데이터 수집 ([Json_Fake_Data](https://jsonplaceholder.typicode.com/) 활용)
   - 데이터 파일 저장 (PythonOperator 활용)
   - 로컬 저장소 관리 (docker container 내부 디렉토리)
   - 이메일 알림 시스템 (EmailOperator 활용)

## 4. 검증 및 테스트

docker-compose.yaml 설정 필요

- smtp 설정 : docker-compose.yaml 77~81 라인  주석 해제 및 정보 입력
   ```yaml
   x-airflow-common:
   environment:
      # smtp settings
      # AIRFLOW__SMTP__SMTP_HOST: 'smtp.gmail.com'             # 구글
      # AIRFLOW__SMTP__SMTP_USER: ''        # 사용자 계정 
      # AIRFLOW__SMTP__SMTP_PASSWORD: ''       # 구글에서 발급받은 mail 토큰
      # AIRFLOW__SMTP__SMTP_PORT: 587                          # 587 고정
      # AIRFLOW__SMTP__SMTP_MAIL_FROM: ''   # 보내는 사람 계정

### 4.2 구성 요소 검증
다음 항목들에 대한 세부적인 검증을 수행합니다:

- 외부 API 연동 검증
- 데이터 처리 정확성 확인
- 알림 시스템 동작 검증

### 4.3 테스트
시스템 전반에 대한 테스트를 진행합니다:

- DAG 실행 검증
- 오류 처리 및 복구 기능 테스트 (retry 1회)
- 전체 워크플로우 통합 테스트
```
# 저장소 clone
$ git clone https://github.com/yonggunjoo/airflow_demo.git

# clone path 이동
$ cd ${path}/airflow_demo

# vscode open
$ code .

# terminal > python venv 설정
$ python -m venv ./demo-env
$ demo-env\Scripts\activate

# 플러그인설치
python.exe -m pip install --upgrade pip
$ pip install -r requirements.txt

# docker 컨테이너 백그라운드 실행
docker-compose -f docker-compose.yaml up -d
```
- localhost:8080 접속
- 접속 default 계정 : airflow/airflow 
- parallel_api_pipeline
   - 1건의 API 병렬처리로 발송
   - 1건 성공 메일, 1건 실패 메일 발송
   - 실패시 1번의 retry 시도하고, 실패 시 실패 메일 발송
 - 테스트 결과
 - 성공메일 : 1건, retry : 2건, 실패 메일 : 1건
  ![테스트 결과](테스트결과.png)

## 5. 결론
이 프로젝트를 통해 Airflow 기반의 데이터 파이프라인 자동화를 실현하고, 업무 효율성을 크게 향상시킬 수 있습니다. 지속적인 모니터링과 개선을 통해 시스템의 안정성을 확보할 것입니다.
