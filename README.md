# Cost Anomaly Pipeline
<img width="581" alt="Screen Shot 2022-09-13 at 10 00 03 PM" src="https://user-images.githubusercontent.com/57607047/189907707-55d0f2f0-fe7c-45cb-8d9f-4d80c38fe9f9.png">

## ver1. Simple State Machine
- Each step waits 10 minutes inside the lambda function, and retry 6 times by state machine.
<img width="864" alt="state_machime_람다구성" src="https://user-images.githubusercontent.com/57607047/180954828-289f9b6c-7cec-474d-acc0-c88e44a3b64e.png">

## ver2. SNS, error handling machine
- Not waiting inside lambda, but retry every 5 mins up to 12 times (1 hour) by state machine if ResourcePending error.
- If else error, call SNS and send email with error message.
<img width="916" alt="Screen Shot 2022-08-02 at 11 51 11 AM" src="https://user-images.githubusercontent.com/57607047/182282293-b13a49d4-24c9-473d-a289-a435677aa6cd.png">
