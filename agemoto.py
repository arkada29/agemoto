from app import create_app, db
from app.models import Users

app = create_app()
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'user':Users}
