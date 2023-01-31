from .serializers import CreateBookSerializer, UpdateBookSerializer, UserRegisterSerializer,\
     LoginResponseSerializer, LoginRequestSerializer, ChangePasswordSerializer,\
         BookResponseSerializer, UpdateBookSerializer, BorrowUserBookSerializer
from .models import User, Book, BorrowUserBook
from .permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permisssion_classes = (AllowAny,)
    parser_classes = [MultiPartParser]  

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.role == "LIBRARIAN":
            user.is_staff = True
        user.save()
        response = LoginResponseSerializer(user, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginRequestSerializer
    permisssion_classes = (AllowAny,)
    parser_classes = [MultiPartParser]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        response = LoginResponseSerializer(user, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)


class DeleteAccountView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):
        user_obj = get_object_or_404(User, pk=pk)
        if user_obj:
            user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddBookView(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CreateBookSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        response = BookResponseSerializer(book, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class UpdateBookView(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def put(self, request, pk, format=None):
        book_obj = get_object_or_404(Book, pk=pk)
        serializer = UpdateBookSerializer(book_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBookView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, format=None):
        book_obj = get_object_or_404(Book, pk=pk)
        book_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailBookView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Book.objects.all()
    serializer_class = BookResponseSerializer


class ListBookView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Book.objects.all()
    serializer_class = BookResponseSerializer


class BorrowedBookView(generics.CreateAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BorrowUserBookSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args,  **kwargs):
        check_availibility_of_book = Book.objects.filter(id=request.data['book']).first()
        if check_availibility_of_book.status == 'BORROWED':
            return Response(
                {"detail": f"This book is borrowed"}, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            borrow_book = serializer.save()
            borrow_book.book.status = "BORROWED"
            borrow_book.book.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class BorrowedBookListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BorrowUserBookSerializer
    queryset = BorrowUserBook.objects.all()


class ReturnBookView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    parser_classes = [MultiPartParser]

    def put(self, request, user_id, book_id, format=None):
        book_obj = get_object_or_404(BorrowUserBook, user=user_id, book=book_id)
        if book_obj:
            book_obj.delete()
        Book.objects.filter(id=book_id).update(status='AVAILABLE')
        return Response({"status": f"Book {book_id} is available for users"}, status=status.HTTP_202_ACCEPTED)
