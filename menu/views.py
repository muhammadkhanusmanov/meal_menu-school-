# menu/views.py
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import MealType
from .serializers import MealTypeSerializer
from .permission import IsSuperAdmin, IsAdmin
from drf_yasg.utils import swagger_auto_schema

class MealTypeListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # barcha kirgan foydalanuvchilar ko‘ra oladi

    @swagger_auto_schema(
        operation_summary="MealType ro'yxati (rolga qarab filtrlanadi)",
        operation_description="""
        - SuperAdmin: barcha maktablar bo‘yicha guruhlab
        - Admin: o‘z maktabi uchun
        - Parent/Student: farzandi/yoki o‘zi o‘qiyotgan maktab uchun
        """,
        responses={200: MealTypeSerializer(many=True)}
    )
    def get(self, request, id: int = None):
        role_id = getattr(request.user, 'role_id', None)
        school_id = getattr(request.user, 'school_id', None)
        meal_types = MealType.objects.all().order_by('display_order')

        if role_id == 1:  # SuperAdmin
            grouped_data = defaultdict(list)
            for meal in meal_types:
                serialized = MealTypeSerializer(meal).data
                grouped_data[str(meal.school_id)].append(serialized)
            return Response(grouped_data, status=status.HTTP_200_OK)

        elif role_id in [5, 2, 3]:  # Admin, Student, Parent
            if not school_id:
                return Response({'detail': 'school_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            meal_types = meal_types.filter(school_id=school_id)
            serializer = MealTypeSerializer(meal_types, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'Access Denied'}, status=status.HTTP_403_FORBIDDEN)
        
class MealTypeCrud(APIView):
    authentication_classes = [LaravelPassportAuthentication]
    permission_classes = [IsSuperAdmin | IsAdmin | IsParent | IsStudent]
    
    def get(self, request, id: int = None):
        meal_type = MealType.objects.get(id=id)
        serializer = MealTypeSerializer(meal_type)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id: int = None):
        # check if user is SuperAdmin or admin
        if getattr(request.user, 'role_id', None) not in [1, 5]:
            return Response({'detail': 'Access Denied'}, status=status.HTTP_403_FORBIDDEN)
        
        meal_type = MealType.objects.get(id=id)
        serializer = MealTypeSerializer(meal_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id: int = None):
        # check if user is SuperAdmin or admin
        if getattr(request.user, 'role_id', None) not in [1, 5]:
            return Response({'detail': 'Access Denied'}, status=status.HTTP_403_FORBIDDEN)
        meal_type = MealType.objects.get(id=id)
        meal_type.delete()
        return Response({'detail': 'MealType deleted successfully'}, status=status.HTTP_200_OK)


class MenuItemListAPIView(APIView):
    authentication_classes = [LaravelPassportAuthentication]
    permission_classes = [IsSuperAdmin | IsAdmin | IsParent | IsStudent]

    @swagger_auto_schema(
        operation_summary="MenuItem ro'yxati (rolga moslab school_id bo'yicha filtrlanadi)",
        responses={200: MenuItemSerializer(many=True)}
    )
    def get(self, request):
        role_id = getattr(request.user, 'role_id', None)
        school_id = getattr(request.user, 'school_id', None)

        queryset = MenuItem.objects.select_related('meal_type').order_by('name')

        if role_id == 1:  # SuperAdmin
            grouped = defaultdict(list)
            for item in queryset:
                grouped[str(item.school_id)].append(MenuItemSerializer(item).data)
            return Response(grouped, status=status.HTTP_200_OK)

        elif role_id in [2, 3, 5]:  # Admin, Parent, Student
            if not school_id:
                return Response({"detail": "school_id required"}, status=status.HTTP_400_BAD_REQUEST)
            filtered = queryset.filter(school_id=school_id)
            serializer = MenuItemSerializer(filtered, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Unauthorized role"}, status=status.HTTP_403_FORBIDDEN)