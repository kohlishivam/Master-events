from django.shortcuts import render
from django.http import HttpResponse
import requests

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# Create your views here.

VERIFY_TOKEN = '7thseptember2016'
PAGE_ACCESS_TOKEN = 'EAAJz4ZB0zviUBAEitDLi38TVFoRJWXZBDu9Vnn5bBP9M2leOAH024own6CrgBMWC7IZBCqjOT8lyzQPLNMDFV8hn44tTBzbGteoeSejqMKy6hPH5iWhBMdZCSoVr8nTTgIVsP8P7PFi0faSqNkVZAUXQZAUfWRkBVBF6eNuJ0gOgZDZD'

def post_facebook_message(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()


class MyChatBotView(generic.View):
	def get (self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message= json.loads(self.request.body.decode('utf-8'))
		print incoming_message

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				print message
				sender_id = message['sender']['id']
				message_text = message['message']['text']
				post_facebook_message(sender_id,message_text) 

		return HttpResponse()	

def index(request):
	return HttpResponse('Hello world')