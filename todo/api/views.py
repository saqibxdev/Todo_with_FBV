from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .serializers import UserSerializer
from django.http import Http404, HttpResponse, JsonResponse
@csrf_exempt
def users_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
                
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({"status":"400","message":f"{e}"})


@csrf_exempt
def users_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Http404
    try:
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = UserSerializer(instance=user,data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
            
        elif request.method == 'DELETE':
            user.delete()
            return HttpResponse(status=204)

    except Exception as e:
        return JsonResponse({"status":"400","message":f"{e}"})
