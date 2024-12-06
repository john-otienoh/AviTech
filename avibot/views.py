from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Common headers for requests
HEADERS = {
    'Authorization': settings.WHATSAPP_API_TOKEN,
    'Content-Type': 'application/json'
}
phone_number_id = settings.PHONE_NUMBER_ID
# Function to send a message
def send_msg(msg, wa_id):
    json_data = {
        'messaging_product': 'whatsapp',
        'to': wa_id,
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post(f'https://graph.facebook.com/v20.0/{phone_number_id}/messages', headers=HEADERS, json=json_data)
    print(response.text)

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        # Validation logic for Facebook webhook subscription
        if request.GET.get("hub.mode") == "subscribe" and request.GET.get("hub.challenge"):
            if request.GET.get("hub.verify_token") != settings.VERIFY_TOKEN:
                return HttpResponse("Verification token mismatch", status=403)
            return HttpResponse(request.GET['hub.challenge'], status=200)

    elif request.method == 'POST':
        try:
            # Process incoming POST request (webhook)
            res = json.loads(request.body)
            print(res)

            if 'entry' in res and 'changes' in res['entry'][0] and 'value' in res['entry'][0]['changes'][0] and 'messages' in res['entry'][0]['changes'][0]['value']:
                message = res['entry'][0]['changes'][0]['value']['messages'][0]
                wa_id = message['from']
                message_type = message.get('type')

                if message_type == 'text':
                    user_query = message['text']['body']
                    if user_query.lower() == "hi":
                        send_msg("Hello, welcome to AviTech Bot! How can I assist you today?", wa_id)
                    else:
                        send_msg("Please start by saying 'Hi'.", wa_id)

        except Exception as e:
            print(f"Error: {str(e)}")

        return JsonResponse({"status": "OK"}, status=200)
