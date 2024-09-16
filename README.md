# hackathon2024
東京池袋で行なわれた24時間hackathonに参加し、作成したものです。  
今回のテーマは「超」、私たちの作物のタイトは「超感情リンク」です。

解決したい課題は離れている相手へ言葉を使わずに気持ちを伝えることです。
忙しい人、うまく気持ちを伝えられない人でも、常に相手の気持ちを感じて、自分の気持ちを使える。


## 作成したもの
1. 感情分析モデル（８クラス）  
    　例：anger: 0.00, contempt: 0.00, disgust: 0.00, fear: 0.14, happy: 0.07, neutral: 0.00, sad: 0.00, surprise: 0.79）  
    　データセット：KaggleにあるAffectNetから各クラス２００枚顔写真を選択、独自訓練

2. WebUI  
    　WebCamerでリアルタイムに映像撮り、画面上に感情分析スコアを表示する。  
    　送信するとクラウドへ分析結果を送信する  

3. クラウドでのAgent処理（AWS）  
    　感情スコアを受け取り、LLM処理用プロンプトを生成し、chartGPTへ文章生成依頼。
    　chartGPTから生成した文書をLineNotifyで登録した相手のLineへ通知する  
      また、感情パラメータをIoTHub経由でIoTデバイスへ送信する　　
    ApiGateway->lambda->chatGPT
    lineApi->line
    IotHub->IotDevice  

    Agentのロール設定：  
    * 心理分析プロ：感情判定結果から精神状態を判定して、結論だけ簡潔に述べる。
    * 親切な大阪人：大阪弁で感情状態から世話話をする  

4. Lineアカウンで表示する文書 
    相手のLineでchatGPTで生成した文書が表示される

5. IoTデバイスの処理（未完成）  
    IoTHubからMQTTで受信した感情分析スコアから処理コマンドを合成し、顔刺激装置を制御
    IoTデバイスはESP32と刺激電極で構成され、コマンドによって顔の異なる表情筋を刺激する

#
