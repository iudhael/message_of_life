from django.contrib.auth import authenticate, login


class RememberMeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        username = request.COOKIES.get('username')
        password = request.COOKIES.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)


        response = self.get_response(request)
        return response
