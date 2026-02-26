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

## Python + Flask 環境構築

本プロジェクトは **Python 3.9 以上** と **Flask** で動作します。

### 必要な環境

- Python 3.9 以上（推奨: 3.10 以降）
- pip（Python に同梱）

### 環境構築の流れ

1. **Python のバージョン確認**
   ```bash
   python3 --version
   ```

2. **仮想環境の作成**
   ```bash
   python3 -m venv venv
   ```

3. **仮想環境の有効化**
   ```bash
   source venv/bin/activate   # macOS / Linux
   # venv\Scripts\activate    # Windows (PowerShell の場合は .\venv\Scripts\Activate.ps1)
   ```

4. **依存ライブラリのインストール**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **環境変数とデータベース**
   - `.env` に `SECRET_KEY` などを設定
   - `python init_db.py` で SQLite を初期化

6. **起動**
   ```bash
   export FLASK_APP=wsgi.py
   flask run
   # または python wsgi.py
   ```

---

## セットアップ手順（詳細）

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

## ロリポップでの運用

ロリポップ！レンタルサーバーでは、CGI 経由で Flask を動かします。Gunicorn は使えません。

### 前提

- SSH が利用可能なプランであること
- 公開ディレクトリ（例: `www`）にファイルを配置

### 1. SSH 接続と pip の準備

```bash
ssh アカウント@サーバー -p 2222
```

pip が未導入の場合:

```bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
export PATH=$PATH:~/.local/bin
```

### 2. プロジェクトの配置

- FTP/SFTP でアプリのソースをサーバーにアップロード（例: `www` 配下のサブディレクトリ）
- 仮想環境はサーバー上で作成するか、ローカルで `pip install -r requirements.txt` したうえで `app` や `venv/lib` をアップロードする運用も可能（サーバー仕様に合わせて調整）

### 3. CGI エントリポイントの作成

公開ディレクトリに **index.cgi** を置き、Flask アプリを CGI で起動します。

```bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/path/to/your/app')   # プロジェクトのパスに変更
from wsgi import app
from wsgiref.handlers import CGIHandler
CGIHandler().run(app)
```

- 1 行目の `#!/usr/bin/env python3` は、サーバー上の Python のパスに合わせて変更（例: `#!/usr/local/bin/python3`）
- `sys.path.insert` のパスを、本番環境のプロジェクトルートに合わせて変更
- パーミッション: `chmod 755 index.cgi`

### 4. .htaccess で URL を CGI に転送

同じディレクトリに **.htaccess** を配置します。

```apache
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.cgi/$1 [QSA,L]
```

- 静的ファイルや実在するパスはそのまま、それ以外を `index.cgi` に渡します。
- プロジェクトをサブディレクトリに置く場合は `RewriteBase /サブディレクトリ/` に変更。

### 5. データベースとパーミッション

- `python init_db.py` をサーバー上で実行するか、ローカルで作成した `app.db` をアップロード
- `app.db` を置くディレクトリは書き込み可能（707 や 755 など）にし、必要に応じてパスを `config.py` または環境変数で指定

### 注意

- CGI はリクエストごとにプロセスが起動するため、負荷の高い処理は向きません。
- 公式マニュアルで「Python」「CGI」「.htaccess」の仕様を確認してから設定してください。

---

## さくらサーバー（さくらのレンタルサーバ）での運用

さくらのレンタルサーバでは、**スタンダードプラン以上** で SSH が利用でき、Python + Flask を CGI で動かせます。

### 前提

- さくらのレンタルサーバ スタンダードプラン以上（SSH 利用可能）
- 公開ディレクトリは通常 `www`（契約時に案内されたパスに準拠）

### 1. SSH 接続

```bash
ssh ユーザー名@xxx.sakura.ne.jp
```

必要に応じてシェルを bash に変更:

```bash
chsh -s /usr/local/bin/bash
```

### 2. pip のインストール

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user
echo 'export PATH=~/.local/bin:$PATH' >> ~/.bash_profile
source ~/.bash_profile
```

### 3. プロジェクトの配置と依存関係

- FTP または SFTP でアプリのソースを `www` 配下などにアップロード
- SSH でログインし、プロジェクトディレクトリで:
  ```bash
  pip install --user -r requirements.txt
  ```
  または、サーバー推奨の方法に従って仮想環境を利用

### 4. CGI エントリポイント（index.cgi）

公開ディレクトリに **index.cgi** を作成します。

```bash
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/home/アカウント/www')   # 実際のプロジェクトルートに変更
from wsgi import app
from wsgiref.handlers import CGIHandler
CGIHandler().run(app)
```

- 1 行目の Python パスは `which python3` で確認したパスに合わせる
- `sys.path.insert` を本番のプロジェクトルートに変更
- `chmod 755 index.cgi`

### 5. .htaccess の設定

```apache
RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.cgi/$1 [QSA,L]
<Files ~ "\.(py|db)$">
  Require all denied
</Files>
```

- サブディレクトリに設置した場合は `RewriteBase /サブディレクトリ/` に変更
- `.py` や `.db` を直 URL で見られないようにしています（Apache 2.4 の場合は `Require all denied`、2.2 の場合は `deny from all` などサーバー案内に合わせてください）

### 6. データベース

- サーバー上で `python3 init_db.py` を実行するか、ローカルで作成した `app.db` をアップロード
- `app.db` を置くディレクトリのパーミッションを書き込み可能にし、`config.py` の `SQLALCHEMY_DATABASE_URI` でそのパスを指定してもよい

### 7. 動作確認

ブラウザで契約ドメインの URL にアクセスし、トップや `/blog` が表示されるか確認します。エラー時はサーバーのエラーログを確認してください。

---

## その他

- **ブログ一覧**: http://127.0.0.1:5000/blog  
- **マイグレーション**: Flask-Migrate を利用する場合は `flask db upgrade` でスキーマを反映できます（`init_db.py` と併用する場合は運用方針に応じてどちらかで統一してください）。
