from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from user_payment.models import UserPayment
import stripe
import time


@login_required(login_url='login')
def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	is_paid= UserPayment.objects.filter(app_user = request.user,stripe_checkout_id__isnull=False)
	if is_paid.exists():
		return redirect("/")

	# if request.method == 'POST':
	checkout_session = stripe.checkout.Session.create(
		payment_method_types = ['card'],
		line_items = [
			{
				'price': settings.PRODUCT_PRICE,
				'quantity': 1,
			},
		],
		mode = 'payment',
		customer_creation = 'always',
		success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
		cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
	)
	return redirect(checkout_session.url, code=303)
	# return render(request, 'user_payment/product_page.html')


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	try:
		stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
		checkout_session_id = request.GET.get('session_id', None)
		session = stripe.checkout.Session.retrieve(checkout_session_id)
		customer = stripe.Customer.retrieve(session.customer)	
		user = request.user
		user_payment = UserPayment.objects.get(app_user=user.id)
		user_payment.stripe_checkout_id = checkout_session_id
		user_payment.save()
		print(user_payment)
	except Exception as e:
		print(e)
	return render(request, 'user_payment/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'user_payment/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)

