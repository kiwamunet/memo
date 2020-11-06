import pdfkit
import PyPDF2
from pdf import PDFGenerator
from django.conf import settings
import os
import subprocess
import boto3
import json

s3 = boto3.resource('s3')


def lambda_handler(event, context):

    # sqs
    sqs = boto3.resource('sqs', region_name="ap-northeast-1")
    queue = sqs.get_queue_by_name(QueueName='')

    html_contents = ""
    for record in event['Records']:
        payload = record["body"]
        json_dict = json.loads(payload)
        html_contents = json_dict[0]["html_contents"]

    msg_list = queue.receive_messages(MaxNumberOfMessages=1)
    for message in msg_list:
        message.delete()

    # wwkhtmltopdf セット
    subprocess.run("ldd /opt/bin/wkhtmltopdf".split(), check=True)
    subprocess.run("wkhtmltopdf -V".split(), check=True)

    generator = PDFGenerator()
    generator.generate(
        html_contents=html_contents,
        landscape=False,
    )

    docs_file = generator.save(
        name="/tmp/XXXX.pdf"
    )

    # upload to s3
    bucket = ''
    key = 'test' + '.pdf'
    file_name = docs_file

    s3.meta.client.upload_file(file_name, bucket, key)
