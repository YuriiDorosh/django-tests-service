from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.tests.services.parser.test_service import parse_and_click_button
from apps.tests.utils.json_settings import get_button_and_url, set_button_and_url


class GetSettingsAPIView(APIView):
    def get(self, request):
        settings = get_button_and_url()
        return Response(settings)

class SetSettingsAPIView(APIView):
    def post(self, request):
        url = request.data.get('url')
        button = request.data.get('button')
        if not url or not button:
            return Response({"error": "Both 'url' and 'button' are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        set_button_and_url(url, button)
        return Response({"message": "Settings updated successfully."})


class TestParseAPIView(APIView):
    def get(self, request):
        settings = get_button_and_url()
        
        url = settings['url']

        button = settings['button']
        
        result, errors = parse_and_click_button(url, button=button)

        if errors:
            return Response({"message": "Failed to parse data", "errors": errors})
        return Response({"message": "Data parsed successfully", "data": result})
