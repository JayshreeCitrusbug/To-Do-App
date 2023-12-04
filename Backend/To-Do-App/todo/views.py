from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Todo
from .serializer import TodoSerializer

class TodoView(APIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)

        return Response({
            'status': True,
            'data': serializer.data,
            'message': 'Details fetched successfully'
        })

    def post(self, request):
        try:
            user = request.user        
            data = request.data
            data['user'] = user.id
            serializer = TodoSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'data': serializer.errors,
                    'message': 'Invalid field data'
                })

            serializer.save()
            return Response({
                'status': True,
                'data': serializer.data,
                'message': 'New Todo Task is created'
            })
        
        except Exception as exc:
            print("on create exception", exc)
            return Response({
                'status': False,
                'data': {},
                'message': 'Something went wrong'
            })

    def patch(self, request):
        try:
            data = request.data
            uid = data.get('uid')
            if not uid:
                return Response({
                    'status': False,
                    'data': {},
                    'message': 'uid field is required'
                })

            obj = Todo.objects.filter(uid=uid)
            if not obj.exists():
                return Response({
                    'status': False,
                    'data': {},
                    'message': 'Invalid uid'
                })
            print(obj[0])
            serializer = TodoSerializer(obj[0], data=data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'data': serializer.errors,
                    'message': 'Invalid fields'
                })

            serializer.save()
            return Response({
                'status': True,
                'data': serializer.data,
                'message': f"'{obj[0].name}' task is updated"
            })

        except Exception as exc:
            print("exception", exc)
            return Response({
                'status': False,
                'data': {},
                'message': 'Something went wrong'
            })
