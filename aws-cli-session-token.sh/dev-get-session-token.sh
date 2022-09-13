echo "Usage : source ./dev-get-session-token.sh 123456"
export | grep AWS
unset AWS_DEFAULT_REGION
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
#unset AWS_CA_BUNDLE
export | grep AWS

if [[ -z $1 ]]
then
        echo "Read from json file."
else
        echo "MFA Code : "$1
	aws sts get-session-token --serial-number arn:aws:iam::000000000000:mfa/<aws-iam-account-name> --token-code $1 --duration-seconds 36000 > dev-session-token.json
fi

export AWS_DEFAULT_REGION="ap-northeast-2"
export AWS_ACCESS_KEY_ID=`jq --raw-output '.Credentials.AccessKeyId' dev-session-token.json`
export AWS_SECRET_ACCESS_KEY=`jq --raw-output '.Credentials.SecretAccessKey' dev-session-token.json`
export AWS_SESSION_TOKEN=`jq --raw-output '.Credentials.SessionToken' dev-session-token.json`
export | grep AWS

#aws s3 --no-verify-ssl ls
aws s3 ls

