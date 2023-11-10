from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    def check_admin(user):
        return user.is_authenticated and user.is_staff
    return user_passes_test(check_admin)(view_func)