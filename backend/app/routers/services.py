from fastapi import APIRouter
from typing import List
from ..models import ServiceCard

router = APIRouter()

SERVICES = [
    ServiceCard(
        id="indian-standards",
        name="Indian Standards",
        description="Browse and understand what an Indian Standard (IS) covers, how it's structured, and why it matters for your product.",
        icon="book",
    ),
    ServiceCard(
        id="product-certification",
        name="Product Certification",
        description="Learn about the ISI Mark scheme — the process to get your product certified and licensed to carry the Standard Mark.",
        icon="badge-check",
    ),
    ServiceCard(
        id="bis-schemes",
        name="BIS Schemes",
        description="Understand which BIS scheme applies to your product category — Product Certification, CRS, Hallmarking, or Management Systems.",
        icon="layers",
    ),
    ServiceCard(
        id="testing",
        name="Testing",
        description="Get guidance on how BIS product testing works and how to find a recognised testing laboratory.",
        icon="flask",
    ),
    ServiceCard(
        id="hallmarking",
        name="Hallmarking",
        description="Understand the hallmarking process for gold and silver jewellery, HUID, and Assaying & Hallmarking Centres.",
        icon="gem",
    ),
    ServiceCard(
        id="consumer-services",
        name="Consumer Services",
        description="Learn how consumers can verify a licence/HUID and register grievances about substandard certified products.",
        icon="users",
    ),
]


@router.get("/api/services", response_model=List[ServiceCard])
def get_services():
    return SERVICES
