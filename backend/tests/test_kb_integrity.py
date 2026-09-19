import json
import pytest

def test_kb_unique_ids():
    with open('../data/knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    ids = [r['id'] for r in data]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {[id for id in ids if ids.count(id) > 1]}"

def test_kb_verification_metadata():
    with open('../data/knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for r in data:
        if r.get('verified'):
            assert r.get('verification_status') == 'OFFICIAL_EVIDENCE', f"Record {r['id']} has verified=True but lacks OFFICIAL_EVIDENCE"

def test_kb_pending_records():
    with open('../data/knowledge_base.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    kb18 = next((r for r in data if r['id'] == 'kb-018'), None)
    if kb18:
        assert kb18.get('status') in ('PENDING', 'NOT_VERIFIED'), "kb-018 must remain excluded"
        assert not kb18.get('verified'), "kb-018 must not be verified"
