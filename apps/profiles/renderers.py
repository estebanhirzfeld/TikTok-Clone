from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler
import json


class ProfileJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data})


class ProfilesJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfilesJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profiles": data})



class FollowRequestsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code

        # Handle ReturnList
        if isinstance(data, list):
            return super(FollowRequestsJSONRenderer, self).render({'status_code': status_code, 'follow_requests': data})

        # Handle regular dictionaries
        errors = data.get('errors', None)
        if errors is not None:
            return super(FollowRequestsJSONRenderer, self).render(data)

        return json.dumps({'status_code': status_code, 'follow_requests': data})