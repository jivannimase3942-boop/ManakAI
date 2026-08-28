from fastapi import APIRouter
from typing import List
from ..models import SourceListItem
from .. import knowledge_base

router = APIRouter()


@router.get("/api/sources", response_model=List[SourceListItem])
def get_sources():
    records = knowledge_base.all_records()
    return [
        SourceListItem(
            title=r["title"],
            standard_number=r["standard_number"],
            source_name=r["source_name"],
            source_url=r["source_url"],
        )
        for r in records
    ]
