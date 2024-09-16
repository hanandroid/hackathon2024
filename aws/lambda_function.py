import json
import boto3
import base64
import urllib.request
import os
from datetime import datetime, timezone

# OpenAI APIキー
api_key = os.environ["OPENAI_API_KEY"]

def lambda_handler(event, context):
    # API Gatewayから送信されたデータを受け取る
    body = event.get('body')
    
    try:
        data = json.loads(body)
        message = data.get('message', 'No message found')
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
    
    print(f"Received message: {message}")
    
    # gptと会話
    answer = gptTalk(message)
    
    # line通知
    lineNotify(answer)

    # IoT通信
    iot_pub(message)
        
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Message received successfully', 'data': message})
    }


# chartGPT解析
def gptTalk(inputMsg):
    # APIエンドポイントURL
    url = "https://api.openai.com/v1/chat/completions"
    
    # リクエストヘッダー
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # APIに送信するデータ（プロンプト）
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "あなたは心理分析プロです。"},
            {"role": "user", "content": f"以下の感情判定結果から相手の精神状態を判定して、結論だけ簡潔に述べて。{inputMsg}"}
            # {"role": "user", "content": "以下の感情判定結果から相手の精神状態を判定して、結論だけ簡潔に述べて。anger: 0.00, contempt: 0.00, disgust: 0.00, fear: 0.14, happy: 0.07, neutral: 0.00, sad: 0.00, surprise: 0.79, nomal: 0.0"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    # リクエストデータをJSONに変換
    json_data = json.dumps(data).encode('utf-8')
    
    # リクエストの作成
    req = urllib.request.Request(url, data=json_data, headers=headers)
    generated_text = "No data"
    
    # リクエストを送信し、レスポンスを取得
    try:
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            response_json = json.loads(response_text)
            
            # 応答テキストを抽出
            generated_text = response_json['choices'][0]['message']['content']
            print(f"{generated_text}")
    
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        print(f"Error: {e.code}, {error_message}")
    
    return generated_text
    
# line 通知
def lineNotify(contents):
    # LINE Notify
    TOKEN = 'SLjcnDO0jt5cbhgHHAQMWhgT8Y0ozIuOw6BkYXq4Clb'
    api_url = 'https://notify-api.line.me/api/notify'
    
    # ''の間に送りたいメッセージを入力
    # contents = 'Hello World!!'
    
    request_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer' + ' ' + TOKEN
    }
    params = {'message': contents}

    data = urllib.parse.urlencode(params).encode('ascii')
    req = urllib.request.Request(api_url, headers=request_headers, data=data, method='POST')
    conn = urllib.request.urlopen(req)
    
    
    
# WS IoT Dataオブジェクトを取得
iot = boto3.client('iot-data')
 
# IotHub通信
def iot_pub(inputMsg):
    # トピックを指定
    topic = 'test/pub'
    
    # メッセージの内容
    payload = {
        "message": inputMsg
    }
    
    try:
        # メッセージをPublish
        iot.publish(
            topic=topic,
            qos=0,
            payload=json.dumps(payload, ensure_ascii=False)
        )
    except Exception as e:
        print(e)
        return "Failed."
    
    return "Succeeeded."




def convert_b64_string_to_bynary(s):
    """base64をデコードする"""

def same_img():
    #画像保存場所の設定
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('aikey')

    # バイナリがBase64にエンコードされているので、ここでデコード
    imageBody = base64.b64decode(event['body-json'])
    TextTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') #アップロードした画像ファイル名をその時の時間にする
    images = imageBody.split(b'\r\n',4)#必要な部分だけをsplitで切り取る

    key = TextTime +".png"
    bucket.put_object(
        Body = images[4],
        Key = key
    )
    #画像名を Web側で取得するための戻り値
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin' : '*' ,
        'Content-Type' :'application/json'},
        'body': '{"message":"'+ key + '"}'
    }
