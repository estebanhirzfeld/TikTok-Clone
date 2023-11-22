from rest_framework import permissions

class CanAccessPrivateContent(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, 'retrieve'):
            obj = view.get_object()
        # elif hasattr(view, 'list'):
        #     obj = view.get_queryset().first()
        else:
            return False

        user = obj.user

        is_owner = user == request.user
        is_private = user.profile.is_private
        is_follower = user.profile.check_follower(request.user.profile)

        return is_owner or (is_private and is_follower) or not is_private
