import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer
from rest_framework.permissions import IsAuthenticated


class TodosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        todos = Todo.objects.filter(author=request.user.pk, complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['author'] = request.user.pk
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        todo = Todo.objects.filter(author=request.user.pk, id=pk).first()
        print(todo)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        todo = Todo.objects.filter(author=request.user.pk, id=pk).first()
        serializer = TodoCreateSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoneTodoAPIView(APIView):
    def get(self, request, pk):
        todo = Todo.objects.filter(author=request.user.pk, id=pk).first()
        print(todo)
        if todo.complete:
            todo.complete = False
            todo.completed_at = None
        else:
            todo.complete = True
            todo.completed_at = datetime.datetime.today()

        todo.save()
        serializer = TodoDetailSerializer(todo)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        todo = Todo.objects.filter(author=request.user.pk, id=pk).first().delete()
        print(todo)
        return Response("TEST", status=status.HTTP_200_OK)

