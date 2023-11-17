from django.contrib.auth.decorators import user_passes_test


def drone_owner_required(view_func):
    def check_drone_owner(user):
        return user.is_authenticated and user.profile.drone_owner

    return user_passes_test(check_drone_owner)(view_func)