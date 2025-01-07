from mongoengine.queryset import QuerySet

def paginate(queryset: QuerySet, page: int, per_page: int):
    total = queryset.count()
    items = queryset.skip((page - 1) * per_page).limit(per_page)
    return {
        'total': total,
        'page': page,
        'per_page': per_page,
        'items': items
    }