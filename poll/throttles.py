from rest_framework.throttling import UserRateThrottle



class CustomOwnerPollThrottle(UserRateThrottle):
    owner_rate = '20/minute'
    non_owner_rate = '5/minute'

    def custom_rate(self, request, view):
        poll = view.get_object()

        if poll.author == request.user:
            return self.owner_rate
        return self.non_owner_rate

    def allow_request(self, request, view):
        self.rate = self.custom_rate(request, view)
        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)
