import os
from pathlib import Path
from tempfile import gettempdir

preview_db_path = (Path(gettempdir()) / "bkjh-preview.sqlite3").as_posix()
os.environ.setdefault("DATABASE_URL", f"sqlite:///{preview_db_path}")

from django.core.management import call_command  # noqa: E402

from config.wsgi import application  # noqa: E402


flag_path = Path("/tmp/bkjh-preview-ready")
if not flag_path.exists():
    call_command("migrate", interactive=False, verbosity=0)
    call_command("seed_bkjh_content", verbosity=0)
    call_command("bootstrap_admin", verbosity=0)
    flag_path.write_text("ready", encoding="utf-8")


app = application
