import re

def normalize_standard(std_num):
    if not std_num:
        return ""
    # Remove version suffix like :2015
    std = std_num.split(':')[0]
    # Remove extra spaces, make uppercase
    std = re.sub(r'\s+', ' ', std).strip().upper()
    return std

def matches_expected_identity(case, actual_record):
    if not actual_record:
        return False

    actual_record_id = actual_record.get('id')
    actual_std_num = actual_record.get('standard_number') or ''
    actual_status = actual_record.get('verification_status')

    # 1. Reject invalid status
    if actual_status in ['PENDING', 'REJECTED', 'SUPERSEDED']:
        return False

    expected_identity = case.get('expected_identity', {})

    # 2. Exact ID match check
    if actual_record_id in expected_identity.get('record_ids', []):
        return True

    # 3. Standard match for EXACT ID queries
    if case.get('category') == 'exact_id':
        exp_stds = expected_identity.get('standard_numbers', [])
        if exp_stds:
            actual_norm = normalize_standard(actual_std_num)
            for exp_std in exp_stds:
                if normalize_standard(exp_std) == actual_norm:
                    return True

    return False
