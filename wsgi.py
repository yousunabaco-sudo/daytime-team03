from app import create_app, db
from flask import Flask

app = create_app()
app.run(debug=True) # デバッグモードを有効にする

@app.shell_context_processor
def make_shell_context():
    return {'db': db}
