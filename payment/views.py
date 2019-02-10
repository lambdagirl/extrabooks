from django.shortcuts import render
import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order, Offer
# Create your views here.
def payment_process(request):
    order_id = request.session.get('offer_id')
    order = get_object_or_404(Order, offer = order_id)
    offer = get_object_or_404(Offer, id = order_id)

    if request.method == 'POST':
        #retrieve nonce
        nonce= request.POST.get('payment_method_nonce',None)
        #create and submit transaction
        result = braintree.Transaction.sale({
            'amount':{':.2f'}.format(offer.get_total_cost()),
            'payment_method_nonce':nonce,
            'options':{
            'submit_for_settlement':True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        #generate token
        client_token = braintree.ClientToken.generate()
        return render(request,
                            'payment/process.html',
                            {'order':order,
                            'client_token':client_token})

def payment_done(request):
    return render(request,'payment/done.html')
def payment_canceled(request):
    return render(request,'payment/canceled.html')
