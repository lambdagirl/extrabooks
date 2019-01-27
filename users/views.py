
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from django.views.generic import DetailView

from books.models import Book,Category
from .forms import CustomUserCreationForm
from .models import CustomUser,Contact

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
         user = self.request.user
         form.instance.user = user
         return super(SignUpView, self).form_valid(form)



class EditProfileView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = CustomUser
    fields = ['username', 'zip_code', 'first_name','last_name', 'avatar', ]
    template_name = 'settings.html'
    login_url = 'login'


    def test_func(self):
        obj = self.get_object()
        print(obj)
        return  obj == self.request.user

class ProfieView(DetailView):
    model = CustomUser
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        username = kwargs["object"]
        context['book_list'] = Book.objects.filter(seller__username = username)
        context['follows'] = Contact.objects.filter(
            from_user__isnull=False,
            from_user__username__iexact=self.kwargs.get('username'))
        context['followers'] = Contact.objects.filter(
            to_user__isnull=False,
            to_user__username__iexact=self.kwargs.get('username'))
        return context

@require_POST
@ajax_required
def user_follow(request):
    object_id = request.POST.get('id')
    action = request.POST.get('action')
    if object_id and action:
        try:
            user = CustomUser.objects.get(id = object_id)
            if action =='follow':
                Contact.objects.get_or_create(from_user=request.user,
                                                to_user = user)
            else:
                Contact.objects.filter(from_user=request.user,
                                        to_user = user).delete()
            return JsonResponse({'status':'ok'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status':'ko'})
        return JsonResponse({'status':'ko'})
