import sqlite3
import os

def init_db():
    # データベースファイルのパス
    db_path = 'app.db'
    schema_path = 'docs/schema.sql'
    
    if os.path.exists(db_path):
        print(f"警告: {db_path} は既に存在します。上書きしますか？ (y/n)")
        choice = input().lower()
        if choice != 'y':
            print("中断しました。")
            return

    # 接続してスキーマを実行
    try:
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        print(f"成功: {db_path} が正常に初期化されました。")
    except Exception as e:
        print(f"エラー: データベースの初期化に失敗しました。\n{e}")

if __name__ == '__main__':
    init_db()
