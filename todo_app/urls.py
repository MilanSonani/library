from django.urls import path
from .views import UserRegisterView, UserLoginView, ChangePasswordView, DeleteAccountView, \
            AddBookView, UpdateBookView, DeleteBookView, DetailBookView, ListBookView,\
            BorrowedBookView, BorrowedBookListView, ReturnBookView

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('delete-account/<int:pk>', DeleteAccountView.as_view()),
    path('add-book/', AddBookView.as_view()),
    path('book-list/', ListBookView.as_view()),
    path('book-detail/<int:pk>/', DetailBookView.as_view()),
    path('update-book/<int:pk>/', UpdateBookView.as_view()),
    path('delete-book/<int:pk>/', DeleteBookView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view()),
    path('borrow-book/', BorrowedBookView.as_view()),
    path('return-book/<int:user_id>/<int:book_id>/', ReturnBookView.as_view()),
    path('list-borrow-book/', BorrowedBookListView.as_view()),

]