# Cost Anomaly Pipeline
with step function, lambda, batch

## ver1. Simple State Machine
- Each step waits 10 minutes inside the lambda function, and retry 6 times by state machine.
<img width="864" alt="state_machime_람다구성" src="https://user-images.githubusercontent.com/57607047/180954828-289f9b6c-7cec-474d-acc0-c88e44a3b64e.png">

## ver2. SNS, error handling machine
- Not waiting inside lambda, but retry every 5 mins up to 12 times (1 hour) by state machine if ResourcePending error.
- If else error, call SNS and send email with error message.
<img width="892" alt="Screen Shot 2022-07-28 at 9 49 50 AM" src="https://user-images.githubusercontent.com/57607047/181397236-d73e6062-bedc-483d-8eec-662cb1576728.png">
