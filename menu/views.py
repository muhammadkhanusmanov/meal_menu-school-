
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import MealType
from .serializers import MealTypeSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MealTypeListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="MealType ro'yxati",
        responses={200: MealTypeSerializer(many=True)}
    )
    def get(self, request):
        meal_types = MealType.objects.all().order_by('display_order')
        serializer = MealTypeSerializer(meal_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Yangi MealType qo'shish",
        request_body=MealTypeSerializer,
        responses={201: MealTypeSerializer}
    )
    def post(self, request):
        serializer = MealTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealTypeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Bitta MealType ko'rish",
        responses={200: MealTypeSerializer()}
    )
    def get(self, request, pk):
        meal_type = get_object_or_404(MealType, pk=pk)
        serializer = MealTypeSerializer(meal_type)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="MealType yangilash",
        request_body=MealTypeSerializer,
        responses={200: MealTypeSerializer}
    )
    def put(self, request, pk):
        meal_type = get_object_or_404(MealType, pk=pk)
        serializer = MealTypeSerializer(meal_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="MealType o'chirish",
        responses={204: 'Deleted'}
    )
    def delete(self, request, pk):
        meal_type = get_object_or_404(MealType, pk=pk)
        meal_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
