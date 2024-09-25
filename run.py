# run.py
import os
from app import create_app

app = create_app("development")

# PORT = os.environ.get("PORT", 5151)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5151, debug=True)
