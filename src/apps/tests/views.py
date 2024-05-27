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
        
        settings_ua = get_button_and_url()
        url_ua = settings_ua['url']
        button_ua = settings_ua['button']

        result_ua, errors_ua = parse_and_click_button(url_ua, button=button_ua)

        url_ru = 'https://mebelsale.com.ua/ru/'
        button_ru = 'Матрасы'

        result_ru, errors_ru = parse_and_click_button(url_ru, button=button_ru)

        response_data = {
            "ua": {
                "message": "Data parsed successfully" if not errors_ua else "Failed to parse data",
                "data": result_ua if not errors_ua else None,
                "errors": errors_ua if errors_ua else None
            },
            "ru": {
                "message": "Data parsed successfully" if not errors_ru else "Failed to parse data",
                "data": result_ru if not errors_ru else None,
                "errors": errors_ru if errors_ru else None
            }
        }

        return Response(response_data)
