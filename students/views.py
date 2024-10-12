from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from books.models import *
from django.http import JsonResponse
from django.db.models import Q

class Home(generic.TemplateView):
    template_name = 'index.html'
    
class Main(LoginRequiredMixin, generic.TemplateView):
    template_name = 'main.html'
    
@login_required
def profile(request, pk):
    profile = get_object_or_404(User, pk=pk)
    books = profile.borrowed_user.all()
    if request.user.is_superuser or request.user.is_staff or request.user.username == profile.username:
        return render(request, 'students/profile.html', {'profile':profile, 'books':books})
    else:
        return redirect('main')

class EditProfile(LoginRequiredMixin, generic.UpdateView):
    template_name = 'students/edit.html'
    form_class = EditUser
    queryset = User.objects.all()
    pk_url_kwarg = 'pk'
    
    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super(EditProfile, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
    
@login_required
def users(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'admin/users.html', {'users': users})
    return redirect('main')

@login_required
def search_users(request, item):
    item_as_number = 0
    if item == "null":
        users = User.objects.all()
    else:
        if item.isdigit():
            item_as_number = int(item)
            users = User.objects.filter(id=item_as_number)
        else:
            users = User.objects.filter(
                Q(first_name__contains=item) | 
                Q(email__contains=item) | 
                Q(username__contains=item)
            )
    
    users_list = []
    for user in users:
        user_serializer = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'staff': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }
        
        users_list.append(user_serializer)
    
    return JsonResponse({'users':users_list}, safe=False)