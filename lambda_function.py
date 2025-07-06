import boto3
import gzip
import json
import base64

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:904119424362:security-alerts'
SECURITY_GROUP_ID = 'sg-0b8253aa712e296d5'  

def lambda_handler(event, context):
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    log_events = json.loads(uncompressed_payload)

    blocked_ips = []

    for e in log_events['logEvents']:
        message = json.loads(e['message'])
        
        if message.get('eventName') == 'ConsoleLogin':
            if message.get('errorMessage') == 'Failed authentication':
                source_ip = message.get('sourceIPAddress')
                if source_ip:
                    try:
                        ec2.authorize_security_group_ingress(
                            GroupId=SECURITY_GROUP_ID,
                            IpProtocol='-1',
                            CidrIp=f"{source_ip}/32"
                        )
                        blocked_ips.append(source_ip)
                    except Exception as ex:
                        print(f"Error blocking {source_ip}: {str(ex)}")
    
    if blocked_ips:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='Security Alert: IPs Blocked',
            Message=f"The following IPs were blocked due to suspicious activity:\n{', '.join(blocked_ips)}"
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Blocked IPs: {blocked_ips}")
    }
