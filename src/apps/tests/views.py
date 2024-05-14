from rest_framework.views import APIView
from rest_framework.response import Response
from apps.tests.services.parser.test_service import parse_and_click_button

class TestParseAPIView(APIView):
    def get(self, request):
        # Assuming the request data is in JSON format
        # data = request.data
        
        url = "https://mebelsale.com.ua/"
        button_text = "Матраци"

        result = parse_and_click_button(url, button_text=button_text)

        if result:
            return Response({"message": "Data parsed successfully", "data": result})
        else:
            return Response({"message": "Failed to parse data"})