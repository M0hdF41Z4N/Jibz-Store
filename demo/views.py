from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,View
from demo.models import Product,Category,Address,Payment
from cart.models import Cart,Ord
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm,CheckoutForm
from django.contrib import messages
from django.conf import settings
import stripe

# Create your views here.

# Home View
class home(ListView):
    model = Product
    template_name = 'demo/home.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['cat_list'] = Category.objects.all()
        return context

# Checkout View
class checkoutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        user = self.request.user
        orders = Ord.objects.filter(user=user,ordered=False)
        if orders.exists():
            order = orders[0]
            context = {
            'form' : form ,
            'carts' : Cart.objects.filter(user=user) ,
            'order' : order
            }
            return render(self.request,'demo/checkout-page.html',context)
        else:
            messages.warning(self.request,"You do not have any active order. Continue Shopping !!!")
            return redirect('demo:demo')
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        orders = Ord.objects.filter(user=self.request.user,ordered=False)
        if form.is_valid():
            Name = form.cleaned_data.get('Name')
            House_no = form.cleaned_data.get('House_no')
            Area = form.cleaned_data.get('Area')
            Zip = form.cleaned_data.get('Zip')
            Same_Billing_Address = form.cleaned_data.get('Same_Billing_Address')
            City = form.cleaned_data.get('City')
            State = form.cleaned_data.get('State')
            shippingAddress = Address(
            user = self.request.user ,
            Name = Name ,
            House_no = House_no,
            Area = Area,
            City = City,
            State = State,
            Zip = Zip,
            Same_Billing_Address = Same_Billing_Address,
            )
            shippingAddress.save()
            payment_option = form.cleaned_data.get('Payment_option')
            if payment_option != 'sp':
                messages.warning(self.request,"Under Maintainence.Please Select Stripe Payment option.")
                return redirect("demo:checkout")
        return redirect("/payment/stripe")


# Product View
class ProductView(DetailView):
    model = Product
    template_name = 'demo/product-page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

stripe.api_key = settings.STRIPE_SECRET_KEY


# Payment View Function
class PaymentView(View):
    def get(self,*args,**kwargs):
        return render(self.request,"demo/payment.html")
    def post(self,*args,**kwargs):
        token = self.request.POST.get('stripeToken')
        user = self.request.user
        order = Ord.objects.get(user=user,ordered=False)
        amount = int(order.get_totals())
        try:
            # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
            amount = amount,
            currency = 'usd',
            source=token
            )

            # Updating payment in db
            payment = Payment()
            payment.user = self.request.user
            payment.amount = amount
            payment.order_id = charge['id']
            payment.save()

            # Updating order in db
            order.payment = payment
            order.ordered = True
            order.save()

            #Remove from cart
            order_items = Cart.objects.filter(user=user)[0]
            order_items.delete()


            messages.success(self.request, "Your order is successfully placed.")
            redirect("/")
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error',{})
            messages.warning(self.request, f"{err.get('message')}")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not Authenticated")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
        except stripe.error.StripeError as e:
            messages.warning(self.request, "Something went wrong. You will not charged. Please try again.")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.warning(self.request, "A serious error occurred. We have been notifed.")
        return redirect("/")

# Order View
class OrderView(View):
    model = Ord
    def get(self,*args,**kwargs):
        user = self.request.user
        context = {
        'orders' : Ord.objects.filter(user=user,ordered=True),
        'payment' : Payment.objects.filter(user=user)
        }
        return render(self.request,"demo/order.html",context)
