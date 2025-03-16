def lambda_handler(event, context):
    try:
        # Extract bucket name and file key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        # Get the file object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')  # Assuming text-based files

        if not file_content:
            raise Exception("Failed to read the content.")

        # Publish the content to the SNS topic
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=content,
            Subject=f"Content for File: {file_key}"
        )

        print(f"Content for '{file_key}' published to SNS.")
        return {
            'statusCode': 200,
            'body': f"Content for '{file_key}' published to SNS."
        }

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {str(e)}"
        }
