from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Order
from .serializers import OrderSerializer, OrderUpdateSerializer

class OrderFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    
    class Meta:
        model = Order
        fields = ['status', 'start_date', 'end_date']

class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    filterset_class = OrderFilter
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        order = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "No tienes permiso para realizar esta acción"},
                status=status.HTTP_403_FORBIDDEN
            )
        if order.status != 'pending':
            return Response(
                {"detail": "Solo se pueden aceptar órdenes pendientes"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'accepted'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        order = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "No tienes permiso para realizar esta acción"},
                status=status.HTTP_403_FORBIDDEN
            )
        if order.status != 'pending':
            return Response(
                {"detail": "Solo se pueden rechazar órdenes pendientes"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'rejected'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "No tienes permiso para realizar esta acción"},
                status=status.HTTP_403_FORBIDDEN
            )
        if order.status != 'accepted':
            return Response(
                {"detail": "Solo se pueden completar órdenes aceptadas"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'completed'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data) 