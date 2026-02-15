from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.shortcuts import get_object_or_404

from django.views.generic import TemplateView, ListView
from .models import FamilyLibrary
from house_hold.forms import BookForm


class HomeView(TemplateView):
    template_name = 'home.html'  # главная страница

class LibraryListView(ListView):
    model = FamilyLibrary
    context_object_name = 'books'
    template_name = 'list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort')
        year = self.request.GET.get('year')
        rating = self.request.GET.get('rating')
        
        if sort_by:
            queryset = queryset.order_by(sort_by)
        
        if year:
            queryset = queryset.filter(publ_year=year)
        
        if rating:
            queryset = queryset.filter(rating=rating)
        
        return queryset


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


def edit_book(request, pk):
    book = get_object_or_404(FamilyLibrary, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = BookForm(instance=book)
    # return render(request, 'edit_book.html', {'form': form})
    return render(request, 'edit_book.html', {'form': form})

def search_books(request):
    query = request.GET.get('q')
    if query:
        books = FamilyLibrary.objects.filter(book_name__icontains=query) | FamilyLibrary.objects.filter(author__icontains=query)
    else:
        books = FamilyLibrary.objects.all()
    return render(request, 'search.html', {'books': books})


def delete_book(request, pk):
    book = get_object_or_404(FamilyLibrary, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('library_list')
    return render(request, 'delete_book.html', {'book': book})
