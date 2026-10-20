"""Create local configuration without overwriting an existing environment."""

from pathlib import Path
import secrets

root = Path(__file__).resolve().parent.parent
target = root / ".env.local"
if not target.exists():
    content = (root / ".env.example").read_text()
    content = content.replace(
        "JWT_SECRET=generate-on-setup", f"JWT_SECRET={secrets.token_hex(32)}"
    )
    content = content.replace(
        "SECRET_KEY=generate-on-setup", f"SECRET_KEY={secrets.token_hex(32)}"
    )
    with target.open("x") as output:
        output.write(content)
    target.chmod(0o600)
    print("Created .env.local with unique development signing keys.")
else:
    print("Using existing .env.local.")
