from functools import wraps
from django.shortcuts import redirect, reverse


def login_dec(status=True):
    def login_judge(func):
        @wraps(func)
        def warps_func(self, request, *args, **kwargs):
            if request.user.is_authenticated == status:
                return redirect(reverse('index'))

            return func(self, request, *args, **kwargs)

        return warps_func

    return login_judge
