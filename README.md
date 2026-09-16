# 天気APIアプリ

## 概要

PythonとOpen-Meteo APIを使用して作成した天気情報取得アプリです。

都市を選択すると、現在の天気や最高気温・最低気温などを取得して表示します。
また、取得した天気情報を履歴として保存し、前回の都市の天気や過去の履歴を確認できるようにしています。

## 主な機能

* 都市を選択して天気を取得
* 現在の気温を表示
* 最高気温・最低気温を表示
* 天気情報に応じたアドバイスを表示
* 前回選択した都市の天気を表示
* 天気情報の履歴を保存
* 過去の天気履歴を確認

## 使用技術

* Python
* Open-Meteo API
* JSON
* requests

## 対応都市

* 福岡
* 東京
* 大阪
* 名古屋
* 札幌
* 那覇

## データ保存

取得した天気情報は `weather_history.json` に保存しています。

`weather_history.json` は実行時に生成されるデータのため、GitHubには公開していません。

## アプリの構成

```text
weather/
├── weather.py
├── README.md
├── .gitignore
└── weather_history.json
```

※ `weather_history.json` はローカル環境で生成されるファイルです。
