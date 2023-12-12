# TODO: change this in production
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails import (
    send_follow_request_accepted_notification,
    send_profile_follow_request_notification,
    send_profile_following_notification,
)
from .exceptions import CantFollowYourself
from .models import FollowRequest, Profile
from .pagination import FollowRequestsPagination, ProfilePagination
from .permissions import CanAccessPrivateContent
from .renderers import (
    FollowRequestsJSONRenderer,
    ProfileJSONRenderer,
    ProfilesJSONRenderer,
)
from .serializers import (
    FollowRequestSerializer,
    FollowSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)
from .signals import follow_on_request_accept

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = [ProfilesJSONRenderer]


class YourProfileDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, CanAccessPrivateContent]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        profile = get_object_or_404(Profile, user__id=user_id)
        return profile


class YourFollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            following_profiles = profile.following.all()  # 1
            serializer = FollowSerializer(following_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profiles.count(),
                "following": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)


class YourFollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            followers_profiles = profile.followers.all()  # 1
            serializer = FollowSerializer(followers_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": followers_profiles.count(),
                "followers": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        try:
            target_profile = Profile.objects.get(user__id=user_id)

            # Check if the request user is following the target user or if the target user is not private
            if (
                request.user.profile.check_following(target_profile)
                or not target_profile.is_private
                or request.user.profile == target_profile
            ):
                # Show following profiles only if the conditions are met
                following_profiles = target_profile.following.all()
                serializer = FollowSerializer(following_profiles, many=True)
                formatted_response = {
                    "status_code": status.HTTP_200_OK,
                    "following_count": following_profiles.count(),
                    "following": serializer.data,
                }
                return Response(formatted_response, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied(
                    "You are not authorized to view this user's followers."
                )
        except Profile.DoesNotExist:
            raise PermissionDenied(
                "You are not authorized to view this user's followers."
            )

        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        try:
            target_profile = Profile.objects.get(user__id=user_id)

            # Check if the request user is following the target user or if the target user is not private
            if (
                request.user.profile.check_following(target_profile)
                or not target_profile.is_private
                or request.user.profile == target_profile
            ):
                # Show follower profiles only if the conditions are met
                followers_profiles = target_profile.followers.all()
                serializer = FollowSerializer(followers_profiles, many=True)
                formatted_response = {
                    "status_code": status.HTTP_200_OK,
                    "followers_count": followers_profiles.count(),
                    "followers": serializer.data,
                }
                return Response(formatted_response, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied(
                    "You are not authorized to view this user's followers."
                )
        except Profile.DoesNotExist:
            raise PermissionDenied(
                "You are not authorized to view this user's followers."
            )


class FollowAPIView(APIView):
    def post(self, request, user_id, format=None):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if profile == follower:
                raise CantFollowYourself()

            if user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_name}",
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            # Check if the target profile is private
            if profile.is_private:
                follow_request, created = FollowRequest.objects.get_or_create(
                    requester=user_profile, target=profile
                )

                if not created:
                    formatted_response = {
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "message": f"You have already sent a follow request to {profile.user.first_name} {profile.user.last_name}",
                    }
                    return Response(
                        formatted_response, status=status.HTTP_400_BAD_REQUEST
                    )

                send_profile_follow_request_notification(user_profile, profile)
                return Response(
                    {
                        "status_code": status.HTTP_200_OK,
                        "message": f"Follow request sent to {profile.user.first_name} {profile.user.last_name}",
                    },
                )

            # If the target profile is not private, directly follow
            user_profile.follow(profile)

            # Notify following user by email
            send_profile_following_notification(user_profile, profile)

            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": f"You are now following {profile.user.first_name} {profile.user.last_name}",
                },
            )
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        try:
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if not user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You can't unfollow {profile.user.first_name} {profile.user.last_name}, since you were not following them in the first place ",
                }
                return Response(
                    formatted_response,
                    status.HTTP_400_BAD_REQUEST,
                )

            user_profile.unfollow(profile)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}",
            }
            return Response(formatted_response, status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise NotFound("You can't unfollow a profile that does not exist.")


class FollowListView(generics.ListAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FollowRequestsPagination
    renderer_classes = [FollowRequestsJSONRenderer]

    def get_queryset(self):
        return FollowRequest.objects.filter(
            target=self.request.user.profile, accepted=False
        )


class AcceptFollowRequestView(generics.UpdateAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "follow_request_id"

    def get_queryset(self):
        follow_request_id = self.kwargs["follow_request_id"]
        return FollowRequest.objects.filter(
            target=self.request.user.profile, accepted=False, id=follow_request_id
        )

    def perform_update(self, serializer):
        follow_request = self.get_object()
        requester_profile = follow_request.requester
        target_profile = follow_request.target

        if follow_request.target != self.request.user.profile:
            return PermissionDenied(
                {"detail": "You are not allowed to accept this follow request."}
            )

        with transaction.atomic():
            serializer.instance.accepted = True
            serializer.save(partial=True)
            serializer.is_valid(raise_exception=True)
            follow_on_request_accept(sender=FollowRequest, instance=follow_request)
            send_follow_request_accepted_notification(requester_profile, target_profile)

        return Response({"status": "success"})


class RejectFollowRequestView(generics.DestroyAPIView):
    serializer_class = FollowRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "follow_request_id"

    def get_queryset(self):
        follow_request_id = self.kwargs["follow_request_id"]
        return FollowRequest.objects.filter(
            Q(target=self.request.user.profile)
            | Q(requester=self.request.user.profile),
            id=follow_request_id,
        )

    def perform_destroy(self, instance):
        # You can add additional logic here if needed
        instance.delete()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
