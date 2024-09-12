from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        search_fields = []
        if request.query_params.get("phone_only"):
            search_fields.append("phone")
        if request.query_params.get("username_only"):
            search_fields.append("username")
        if request.query_params.get("email_only"):
            search_fields.append("email")
        if search_fields:
            return search_fields

        return super().get_search_fields(view, request)
