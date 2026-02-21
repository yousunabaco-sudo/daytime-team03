# 新潟心理療法同好会 Webサイト

臨床心理士の同好会において、会員管理、知見の共有（エッセー、書評）、イベント告知、および会員間の交流を促進するためのプラットフォームです。

## 技術スタック

- **Backend**: Python 3.9+ / Flask
- **Database**: SQLite
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Frontend**: HTML (Jinja2) + Tailwind CSS
- **認証**: Flask-Login
- **本番サーバー**: Gunicorn 想定

## ファイル構造

```text
.
├── app/
│   ├── __init__.py          # アプリ生成・初期設定
│   ├── models.py            # データベースモデル（User, Category, Post, Comment）
│   ├── commands.py         # Flask CLI（seed-db 等）
│   ├── static/             # 静的ファイル（CSS, JS, 画像, TinyMCE）
│   ├── blueprints/
│   │   ├── main/           # 公開ページ（トップ、ブログ一覧・詳細等）
│   │   ├── auth/           # ログイン・ログアウト
│   │   └── admin/          # 管理画面（記事・会員管理）
│   └── templates/          # 共通テンプレートは blueprints 内に分散
├── config.py               # アプリケーション設定
├── wsgi.py                 # 実行用エントリーポイント
├── init_db.py              # データベース初期化（schema.sql 適用）
├── requirements.txt       # 依存ライブラリ
├── docs/
│   └── schema.sql          # DB スキーマ・初期データ
├── .env.sample             # 環境変数サンプル
└── README.md
```

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate     # Windows
```

### 3. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env` を用意し、必要に応じて設定します。

```bash
cp .env.sample .env
# .env を編集: SECRET_KEY などを設定
```

例:

```env
SECRET_KEY=your-secret-key
```

### 5. データベースの初期化

`init_db.py` で SQLite の `app.db` を作成し、スキーマと初期データ（管理者ユーザー・カテゴリ）を投入します。

```bash
python init_db.py
```

- 既に `app.db` がある場合は上書き確認が表示されます。
- 初期データとして管理者ユーザーとカテゴリが挿入されます。

### 6. アプリケーションの起動

```bash
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
flask run
```

または:

```bash
python wsgi.py
```

ブラウザで **http://127.0.0.1:5000** にアクセスするとトップページが表示されます。

---

## 管理画面へのアクセス方法

### URL

- **管理画面トップ**: http://127.0.0.1:5000/admin  
  - 未ログインの場合はログインページにリダイレクトされます。
- **ログイン画面**: http://127.0.0.1:5000/auth/login  

### 初期ユーザー（管理者）

`init_db.py` で `docs/schema.sql` を適用した場合、次の管理者アカウントが作成されています。

| 項目     | 値                 |
|----------|---------------------|
| メール   | `admin@example.com` |
| パスワード | `password`        |

※ `schema.sql` のコメントに「admin ユーザー (パスワード: password)」とあるものに合わせています。

ログイン後は **記事一覧** が表示され、以下が利用できます。

- **記事管理**: 投稿一覧・新規投稿・編集・削除
- **会員管理**: ユーザー一覧・新規登録・編集

---

## Render でのデプロイ

本アプリは Flask のアプリケーション工場パターン（`create_app()`）を使っているため、Gunicorn の起動時は **`wsgi:app`** を指定してください。

- ❌ `gunicorn app:app` → `app` パッケージには `app` 属性がないためエラーになります。
- ✅ `gunicorn wsgi:app` → `wsgi.py` 内の `app = create_app()` が使われます。

リポジトリに `render.yaml` を用意している場合は、Render が自動で上記の start command を利用します。ダッシュボードで Start Command を手動設定する場合は次のように指定してください。

```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

---

## その他

- **ブログ一覧**: http://127.0.0.1:5000/blog  
- **マイグレーション**: Flask-Migrate を利用する場合は `flask db upgrade` でスキーマを反映できます（`init_db.py` と併用する場合は運用方針に応じてどちらかで統一してください）。
