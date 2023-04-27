from .models import News, Order, Attachment
from rest_framework import serializers
import random


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M')

    class Meta:
        model = News
        fields = ('slug', 'title', 'text', 'image', 'created_at', )


class OrderSerializer(serializers.ModelSerializer):
    identification_number = serializers.CharField(read_only=True)
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    files = serializers.ListField(child=serializers.FileField(), required=False)

    class Meta:
        model = Order
        fields = ('id', 'identification_number', 'description', 'sender', 'files', )

    def validate_sender(self, sender):
        if not sender.is_authenticated:
            sender = None
        return sender

    def create(self, validated_data):
        # Add identification_number to order
        number = str(random.randint(1, 999999))
        zeros = (6 - len(number)) * '0'  # add leading zeros
        validated_data['identification_number'] = f"{zeros}{number}"

        files = validated_data.pop('files', None)
        order = super().create(validated_data)  # create order

        # Handle incoming files
        if files:
            files_to_create = [Attachment(file=file, order=order) for file in files]
            Attachment.objects.bulk_create(files_to_create)

        return order


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = ('id', 'file', )


class OrderInfoSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'identification_number', 'description', 'files', )

    def get_files(self, obj):
        attachments = obj.attachments.all()
        serializer = AttachmentSerializer(attachments, many=True)
        return serializer.data
