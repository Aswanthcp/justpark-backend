from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator


def paginate_queryset(queryset, serializer_class, page_number, items_per_page):
    paginator = Paginator(queryset, items_per_page)

    try:
        paginated_queryset = paginator.page(page_number)
    except Exception as e:
        return None, {"message": str(e)}, status.HTTP_400_BAD_REQUEST

    serializer = serializer_class(paginated_queryset, many=True)

    pagination_data = {
        "hasNextPage": paginated_queryset.has_next(),
        "hasPrevPage": paginated_queryset.has_previous(),
        "currentPage": paginated_queryset.number,
        "totalPages": paginator.num_pages,
        "results": serializer.data,
    }

    return pagination_data, None, status.HTTP_200_OK
