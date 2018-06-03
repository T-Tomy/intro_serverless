import csv
import os
import json
import boto3
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from contextlib import contextmanager

def csvToDict(csv_str):
    '''
      Description: CSV形式の文字列を「key:1列目, val:2列目」の辞書形式に変換する
    '''

    d = {}
    reader = csv.reader(csv_str.strip().splitlines())
    header = next(reader)
    for row in reader:
        d[row[0]] = row[1]

    return d

@contextmanager
def fetchCsvWithError(url):
    '''
      Description: CSVファイルをダウンロードしてついでにエラーハンドリングもしてくれるやつ
    '''
    try:
        res = urlopen(url)
    except URLError as err:
        yield None, err
    else:
        try:
            yield res, None
        finally:
            res.close()

def runner(event, context):
    '''
    Description メイン
    '''
    # AWSリソース
    s3 = boto3.resource('s3')

    # 環境変数
    holidays_csv_url = os.environ['HOLIDAYS_CSV_URL']
    s3_target_bucket = os.environ['S3_TARGET_BUCKET']
    s3_object_key = os.environ['S3_OBJECT_KEY']

    # ファイルのダウンロード
    # 内閣府の祝日休日データを落とす
    with fetchCsvWithError(holidays_csv_url) as (response, e):
        if e:
            if hasattr(e, 'reason'):
                notify('syncHolidaysList', 'danger'
                       '休祝日情報の取得に失敗. Reason: {} {}'.format(
                           e.code, e.reason))
            elif hasattr(e, 'code'):
                notify(
                    'syncHolidaysList', 'danger'
                    '休祝日情報の取得に失敗. The server couldn\'t fulfill the request. Error code: {}'.
                    format(e.code))
            return ('abnormal end')
        else:
            csv_str = response.read().decode('shift_jis')

    # 変換
    csv_dict = csvToDict(csv_str)
    json_str = json.dumps(csv_dict, ensure_ascii=False)

    # S3バケットにあげる
    obj = s3.Object(s3_target_bucket, s3_object_key)
    obj.put(Body=json_str)

    return 'normal end'
