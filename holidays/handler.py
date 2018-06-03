import os
import json
import boto3

def runner(event, context):
    '''
    Description メイン
    '''
    # AWSリソース
    s3 = boto3.resource('s3')

    # 環境変数
    s3_target_bucket = os.environ['S3_TARGET_BUCKET']
    s3_object_key = os.environ['S3_OBJECT_KEY']

    # データを読み込む
    obj = s3.Object(s3_target_bucket, s3_object_key)
    res = obj.get()

    # JSONテキストとして返す
    return (res['Body'].read().decode('utf-8'))
