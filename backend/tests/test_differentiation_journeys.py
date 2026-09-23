import pytest
from app.decision import generate_compliance_response
from app.models import ChatMessageIn

def test_differentiation_journeys():
    # 1. Pressure cooker standard
    res = generate_compliance_response('What is the standard for pressure cooker?')
    assert res.intent == 'STANDARD_DISCOVERY'
    assert 'Pressure Cooker' in res.product

    # 2. Pressure cooker certification
    res = generate_compliance_response('How do I get certification for pressure cooker?')
    assert res.intent == 'CERTIFICATION'

    # 3. Pressure cooker testing
    res = generate_compliance_response('Where is pressure cooker tested?')
    assert res.intent == 'TESTING'

    # 12. Flying car rejection
    res = generate_compliance_response('Flying car certification')
    assert res.match_found == False
    assert res.confidence == 'none'

    # 14. Hindi journey
    res = generate_compliance_response('प्रेशर कुकर का मानक क्या है?', language='hi')
    assert res.intent == 'STANDARD_DISCOVERY'

    # 15. Marathi journey
    res = generate_compliance_response('प्रेशर कुकरसाठी मानक काय आहे?', language='mr')
    assert res.intent == 'STANDARD_DISCOVERY'

    print('All basic journey paths successfully verified.')
