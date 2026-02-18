# 心理療法士同好会 Webサイト

心理療法士の同好会において、会員管理、知見の共有（エッセー、書評）、イベント告知、および会員間の交流を促進するためのプラットフォームです。

## 技術スタック

- **Backend**: Python 3.x + Flask
- **Database**: SQLite
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Frontend**: HTML (Jinja2) + TailwindCSS
- **Server**: Gunicorn (本番環境想定)

## ファイル構造

```text
.
├── app/                # アプリケーションのメインパッケージ
│   ├── __init__.py     # アプリ生成・初期設定
│   ├── models.py       # データベースモデル定義
│   ├── static/         # 静的ファイル（CSS, JS, 画像）
│   ├── templates/      # Jinja2 テンプレート
│   └── blueprints/     # ブループリント（ルーティング）
├── config.py           # アプリケーション設定
├── wsgi.py             # 実行用エントリーポイント
├── requirements.txt    # 依存ライブラリ一覧
├── .env                # 環境変数設定
├── ANTIGRAVITY.md      # プロジェクト憲法（設計指針）
└── README.md           # 本ファイル
```

## セットアップ手順

以下の手順でローカル環境での動作確認が可能です。

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd 106_AI
```

### 2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 3. 依存ライブラリのインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
`.env` ファイルを作成し、必要な設定を記述します。
```bash
cp .env.example .env  # .env.example がある場合
# もしくは直接作成
echo "SECRET_KEY=your-secret-key" > .env
```

### 5. アプリケーションの実行
```bash
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
flask run
```

実行後、ブラウザで `http://127.0.0.1:5000` にアクセスしてください。
"Hello, World! (Project Reset)" と表示されれば成功です。
