import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from schema_validator import validate_payload


def test_validate_payload_valid():
    payload = json.dumps({"id": "1", "content_type": "text", "payload": "hello"})

    result = validate_payload(payload)

    assert result["status"] == "success"
    assert result["data"] == {"id": "1", "content_type": "text", "payload": "hello"}


def test_validate_payload_allows_extra_keys():
    payload = json.dumps(
        {"id": "1", "content_type": "text", "payload": "hello", "escalate": True}
    )

    result = validate_payload(payload)

    assert result["status"] == "success"
    assert result["data"]["escalate"] is True


def test_validate_payload_missing_single_key():
    payload = json.dumps({"id": "1", "content_type": "text"})

    result = validate_payload(payload)

    assert result["status"] == "missing_keys"
    assert result["missing_keys"] == ["payload"]


def test_validate_payload_missing_multiple_keys():
    payload = json.dumps({"content_type": "text"})

    result = validate_payload(payload)

    assert result["status"] == "missing_keys"
    assert result["missing_keys"] == ["id", "payload"]


def test_validate_payload_empty_object_missing_all_keys():
    payload = json.dumps({})

    result = validate_payload(payload)

    assert result["status"] == "missing_keys"
    assert result["missing_keys"] == ["id", "content_type", "payload"]


def test_validate_payload_malformed_json():
    payload = "{id: 1, content_type: 'text', payload: 'hello'"

    result = validate_payload(payload)

    assert result["status"] == "invalid_json_format"


def test_validate_payload_empty_string():
    result = validate_payload("")

    assert result["status"] == "invalid_json_format"


def test_validate_payload_non_dict_list_containing_required_keys():
    payload = json.dumps(["id", "content_type", "payload"])

    result = validate_payload(payload)

    assert result["status"] == "success"
    assert result["data"] == ["id", "content_type", "payload"]


def test_validate_payload_non_dict_list_missing_required_keys():
    payload = json.dumps(["unrelated"])

    result = validate_payload(payload)

    assert result["status"] == "missing_keys"
    assert result["missing_keys"] == ["id", "content_type", "payload"]


def test_validate_payload_non_dict_string():
    payload = json.dumps("hello world")

    result = validate_payload(payload)

    assert result["status"] == "missing_keys"
    assert result["missing_keys"] == ["id", "content_type", "payload"]


@pytest.mark.parametrize("scalar_json", ["null", "5", "true", "3.14"])
def test_validate_payload_non_iterable_scalar_raises(scalar_json):
    with pytest.raises(TypeError):
        validate_payload(scalar_json)
