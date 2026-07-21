import os
import shutil

from schema_validator import validate_payload

INBOX_DIR = "./Inbox"
PROCESSED_DIR = "./Processed"
QUARANTINE_DIR = "./Quarantine"


def process_inbox():
    for filename in os.listdir(INBOX_DIR):
        src_path = os.path.join(INBOX_DIR, filename)
        if not os.path.isfile(src_path):
            continue

        with open(src_path, "r") as f:
            content = f.read()

        result = validate_payload(content)

        if result["status"] == "success" and not result["data"].get("escalate"):
            dest_dir = PROCESSED_DIR
        else:
            dest_dir = QUARANTINE_DIR

        shutil.move(src_path, os.path.join(dest_dir, filename))
