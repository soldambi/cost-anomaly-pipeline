# Cost Anomaly Pipeline
<img width="581" alt="Screen Shot 2022-09-13 at 10 00 03 PM" src="https://user-images.githubusercontent.com/57607047/189907707-55d0f2f0-fe7c-45cb-8d9f-4d80c38fe9f9.png">
- 사용된 AWS 서비스
  - Step Function: 워크플로우를 구성하고 관리하는 용도
  - Lambda: 워크플로우의 각 스텝(step)이면서, Batch와 SNS에 요청을 보내는 용도
  - Batch: 파이썬 스크립트를 실행할 컴퓨팅 환경을 구성하고 실제 실행하는 용도
  - SNS: 워크플로우가 성공하거나 실패할 경우 사용자에게 이메일 알림을 보내는 용도
  - ECR: Batch Job을 실행할 컨테이너 이미지를 저장하는 용도
  - SageMaker: 컨테이너 이미지 빌드/푸시 및 개발 용도
  - S3: step function 각 스텝의 중간 결과물들을 csv로 저장하는 용도
  - EventBridge: 스케줄링 및 step function을 트리거하는 용도

## ver1. Simple State Machine
- Each step waits 10 minutes inside the lambda function, and retry 6 times by state machine.
<img width="864" alt="state_machime_람다구성" src="https://user-images.githubusercontent.com/57607047/180954828-289f9b6c-7cec-474d-acc0-c88e44a3b64e.png">

## ver2. SNS, error handling machine
- Not waiting inside lambda, but retry every 5 mins up to 12 times (1 hour) by state machine if ResourcePending error.
- If else error, call SNS and send email with error message.
<img width="916" alt="Screen Shot 2022-08-02 at 11 51 11 AM" src="https://user-images.githubusercontent.com/57607047/182282293-b13a49d4-24c9-473d-a289-a435677aa6cd.png">
