from django.shortcuts import render,get_object_or_404,redirect
from rest_framework import viewsets
from .serializers import HeroSerializer
from .models import Hero
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status


# Create your views here.
class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer

class HeroApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    #function to get all heroes
    def get(self, request, *args, **kwargs ):
        
     heroes = Hero.objects.all().order_by('id')
     serializer = HeroSerializer(heroes, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)
     

    #function to create a new hero
    def Hero(self, request, *args, **kwargs):
     
        data = {
            'name': request.data.get('name'), 
            'alias': request.data.get('alias'), 
            'id':request.data.get('id')
        }
        serializer = HeroSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class HeroDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, id):
        '''
        Helper method to get the object with given id, 
        '''
        try:
            return Hero.objects.get(id=id)
        except Hero.DoesNotExist:
            return None
    
    def get(self, request, id, *args, **kwargs):
        '''
        Retrieves the hero with given hero_id
        '''
        hero_instance = self.get_object(id)
        if not hero_instance:
            return Response(
                {"res": "Object with hero id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HeroSerializer(hero_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 4. Update
    def put(self, request, id, *args, **kwargs):
        '''
        Updates the hero item with given hero_id if exists
        '''
        hero_instance = self.get_object(id)
        if not hero_instance:
            return Response(
                {"res": "Object with hero id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'alias': request.data.get('alias'), 
            'id':request.data.get('id')
        }
        serializer = HeroSerializer(instance = hero_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 5. Delete
    def delete(self, request, id, *args, **kwargs):
        '''
        Deletes the hero item with given id if exists
        '''
        hero_instance = self.get_object(id)
        if not hero_instance:
            return Response(
                {"res": "Object with hero id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        hero_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
