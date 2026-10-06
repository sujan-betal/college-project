def build_pagination(page: int, page_size: int, total: int) -> dict:
    total_pages = (total + page_size - 1) // page_size if page_size else 0

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }


def percentage(part: int, whole: int) -> float:
    if not whole:
        return 0.0

    return round((part / whole) * 100, 2)


def build_audit_dict(log) -> dict:
    return {
        "id": str(log.id),
        "userid": str(log.userid) if log.userid else None,
        "action": log.action,
        "target_type": log.target_type,
        "target_id": str(log.target_id) if log.target_id else None,
        "meta": log.meta,
        "created_at": log.created_at.isoformat() if log.created_at else None
    }