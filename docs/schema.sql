-- 心理療法士同好会 Webサイト データベーススキーマ (SQLite)

-- 1. `users` (利用者)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('admin', 'member')),
    profile TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. `categories` (カテゴリー)
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. `posts` (投稿内容)
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_date DATETIME,
    eyecatch_img TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 4. `comments` (コメント)
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER, -- 会員の場合は ID が入る。非会員の場合は NULL。
    name TEXT NOT NULL, -- 投稿者名（会員なら users.name、非会員なら入力名）
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- インデックスの作成
CREATE INDEX idx_posts_user_id ON posts (user_id);
CREATE INDEX idx_posts_category_id ON posts (category_id);
CREATE INDEX idx_comments_post_id ON comments (post_id);

-- 初期データ
-- 1. admin ユーザー (パスワード: password)
INSERT INTO users (name, email, password_hash, role)
VALUES (
    '管理者',
    'admin@example.com',
    'scrypt:32768:8:1$3CzU4IjTBdTUDs8r$ddf6c98ae307af19f639a61035ac6bf4f711b6000a9ef6054a2c61f0a70328892ef657546e175a9daf8733ebebaf4961fc485a88b7da86bc7319917b19f03bd6',
    'admin'
);

-- 2. categories
INSERT INTO categories (name, slug)
VALUES 
    ('トピックス', 'topics'),
    ('エッセー・書評', 'essay'),
    ('イベント', 'event'),
    ('研究会', 'study'),
    ('その他', 'other');
