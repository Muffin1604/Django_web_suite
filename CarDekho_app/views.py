from django.shortcuts import render
from . models import Carlist,Showroomlist,Review
from . api_file.serializers import CarSerializer,ShowroomSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status,mixins,generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from . api_file.permissions import AdminOrReadOnlyPermission,ReviewUserorReadonlypermission

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()
    

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        cars = Carlist.objects.get(pk=pk)
        useredit = self.request.user
        Review_queryset = Review.objects.filter(car= cars, apiuser= useredit)
        if Review_queryset.exists():
            raise ValidationError("You have already reviewed this car")
        serializer.save(car=cars,apiuser=useredit)
    

class ReviewDetails(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = [ReviewUserorReadonlypermission]
    permission_classes = [AdminOrReadOnlyPermission]

class ReviewList(generics.RetrieveUpdateDestroyAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = [ReviewUserorReadonlypermission]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)

# class ReviewDetails(mixins.RetrieveModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    

# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [DjangoModelPermissions]
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
class Showroom_Viewset(viewsets.ModelViewSet):
    queryset = Showroomlist.objects.all()
    serializer_class = ShowroomSerializer


# class Showroom_View(APIView):
#     #authentication_classes = [BasicAuthentication]
#     #permission_classes= [IsAuthenticated]#allowany,isadminuser
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         showroom = Showroomlist.objects.all()
#         serializer = ShowroomSerializer(showroom, many=True,context={'request':request})
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = ShowroomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
        
# class Showroom_Details(APIView):
#     def get(self,request,pk):
#         try:
#             showroom = Showroomlist.objects.get(pk=pk)
#         except Showroomlist.DoesNotExist:
#             return Response({'Error':'car not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = ShowroomSerializer(showroom)
#         return Response(serializer.data)
    
#     def put(self, request,pk):
#         showroom = Showroomlist.objects.get(pk=pk)
#         serializer = ShowroomSerializer(showroom,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk):
#         showroom = Showroomlist.objects.get(pk=pk)
#         showroom.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) 


# def car_list_view(request):
#     cars = Carlist.objects.all()
#     data = {
#         'cars':list(cars.values()),

#     }
#     return JsonResponse(data)
#     # data_json = json.dumps(data)
#     # return HttpResponse(data_json, content_type = 'applicaton/json')

# def car_detail_view(request,pk):
#     car = Carlist.objects.get(pk=pk) 
#     data = {
#         'name':car.name,
#         'description':car.description,
#         'active':car.active
#     }  
#     return JsonResponse(data) 
# Create your views here.
@api_view(['GET','POST'])
def car_list_view(request):
    if request.method == 'GET':
        car = Carlist.objects.all()
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
@api_view(['GET','PUT','DELETE'])
def car_detail_view(request,pk):
    if request.method == 'GET':
        try:
            car = Carlist.objects.get(pk=pk)
        except:
            return Response({'Error':'car not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        car = Carlist.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
