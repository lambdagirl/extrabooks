from actions.models import Action
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from django.views.generic import DetailView
from books.models import Book,Category
from .forms import CustomUserCreationForm
from .models import CustomUser,Contact
from actions.utils import create_action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth

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
                create_action(request.user,'is following', user)
            else:
                Contact.objects.filter(from_user=request.user,
                                        to_user = user).delete()
            return JsonResponse({'status':'ok'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status':'ko'})
        return JsonResponse({'status':'ko'})

def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        #if user is following others, retrieve only their action
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user').prefetch_related('target')[:10]
    return render(request,'dashboard.html',{'section':'dashboard','actions':actions})

@login_required
def sosettings(request):
    user = request.user
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    return render(request, 'social/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            #return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'social/password.html', {'form': form})
