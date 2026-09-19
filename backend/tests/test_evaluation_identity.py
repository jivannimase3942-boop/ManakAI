import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.identity_helper import matches_expected_identity, normalize_standard

def test_normalization():
    assert normalize_standard("IS 269") == "IS 269"
    assert normalize_standard("IS 269:2015") == "IS 269"
    assert normalize_standard("  IS   269  ") == "IS 269"
    assert normalize_standard("is 269") == "IS 269"

def test_is_269_overlap():
    case = {
        'category': 'exact_id',
        'expected_identity': {
            'standard_numbers': ['IS 269'],
            'record_ids': ['kb-011', 'kb-017']
        }
    }

    assert matches_expected_identity(case, {'id': 'kb-011', 'standard_number': 'IS 269:2015', 'verification_status': 'VERIFIED'})
    assert matches_expected_identity(case, {'id': 'kb-017', 'standard_number': 'IS 269'}) # missing status is treated as VERIFIED for legacy
    assert not matches_expected_identity(case, {'id': 'kb-010', 'standard_number': 'IS 9873'})

def test_strict_standard_matching():
    case = {
        'category': 'exact_id',
        'expected_identity': {
            'standard_numbers': ['IS 269'],
        }
    }
    assert matches_expected_identity(case, {'id': 'kb-999', 'standard_number': 'IS 269:2015'})
    assert not matches_expected_identity(case, {'id': 'kb-999', 'standard_number': 'IS 2690'})
    assert not matches_expected_identity(case, {'id': 'kb-999', 'standard_number': 'IS 9873'})

def test_verification_status():
    case = {
        'category': 'exact_id',
        'expected_identity': {
            'standard_numbers': ['IS 269'],
            'record_ids': ['kb-011']
        }
    }

    assert matches_expected_identity(case, {'id': 'kb-011', 'standard_number': 'IS 269', 'verification_status': 'VERIFIED'})
    assert not matches_expected_identity(case, {'id': 'kb-011', 'standard_number': 'IS 269', 'verification_status': 'PENDING'})
    assert not matches_expected_identity(case, {'id': 'kb-011', 'standard_number': 'IS 269', 'verification_status': 'REJECTED'})
    assert not matches_expected_identity(case, {'id': 'kb-011', 'standard_number': 'IS 269', 'verification_status': 'SUPERSEDED'})

def test_is_13252_product_subclass():
    case_laptop = {
        'category': 'valid',
        'expected_identity': {
            'record_ids': ['kb-012', 'kb-018'],
            'standard_numbers': ['IS 13252']
        }
    }

    assert matches_expected_identity(case_laptop, {'id': 'kb-012', 'standard_number': 'IS 13252'})
    assert matches_expected_identity(case_laptop, {'id': 'kb-018', 'standard_number': 'IS 13252'})
    assert not matches_expected_identity(case_laptop, {'id': 'kb-019', 'standard_number': 'IS 13252'})
