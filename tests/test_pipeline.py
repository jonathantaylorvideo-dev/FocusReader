import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import orchestrator
from schema_validator import validate_payload


def test_validate_payload_valid():
    payload = json.dumps({"id": "1", "content_type": "text", "payload": "hello"})

    result = validate_payload(payload)

    assert result["status"] == "success"


def test_validate_payload_missing_keys():
    payload = json.dumps({"id": "1", "content_type": "text"})

    result = validate_payload(payload)

    assert result["status"] == "missing_keys"
    assert "payload" in result["missing_keys"]


def test_validate_payload_malformed_json():
    payload = "{id: 1, content_type: 'text', payload: 'hello'"

    result = validate_payload(payload)

    assert result["status"] == "invalid_json_format"


def test_process_inbox_routes_valid_and_invalid_files(tmp_path, monkeypatch):
    inbox_dir = tmp_path / "Inbox"
    processed_dir = tmp_path / "Processed"
    quarantine_dir = tmp_path / "Quarantine"
    inbox_dir.mkdir()
    processed_dir.mkdir()
    quarantine_dir.mkdir()

    monkeypatch.setattr(orchestrator, "INBOX_DIR", str(inbox_dir))
    monkeypatch.setattr(orchestrator, "PROCESSED_DIR", str(processed_dir))
    monkeypatch.setattr(orchestrator, "QUARANTINE_DIR", str(quarantine_dir))

    valid_content = json.dumps({"id": "1", "content_type": "text", "payload": "hello"})
    invalid_content = json.dumps({"id": "2"})

    (inbox_dir / "valid.json").write_text(valid_content)
    (inbox_dir / "invalid.json").write_text(invalid_content)

    orchestrator.process_inbox()

    assert (processed_dir / "valid.json").exists()
    assert not (quarantine_dir / "valid.json").exists()

    assert (quarantine_dir / "invalid.json").exists()
    assert not (processed_dir / "invalid.json").exists()

    assert not (inbox_dir / "valid.json").exists()
    assert not (inbox_dir / "invalid.json").exists()
