from rest_framework import serializers

from courses.serializers import OrderCourseSerializer
from orders.models import Order


class CompletedOrderSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "courses",
        ]

    def get_courses(self, obj):
        courses = obj.cart.courses
        return OrderCourseSerializer(many=True, instance=courses).data
