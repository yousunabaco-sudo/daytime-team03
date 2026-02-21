from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db}


# Gunicorn で起動するときはここは実行されない（import 時は __name__ != '__main__'）
# ローカルで python wsgi.py したときだけ開発サーバーが起動する
if __name__ == '__main__':
    app.run(debug=True)
