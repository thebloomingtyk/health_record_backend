# from rest_framework import serializers
# from .models import Room, Consultation

# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__'

# class ConsultationSerializer(serializers.ModelSerializer):
#     room = RoomSerializer()

#     class Meta:
#         model = Consultation
#         fields = '__all__'

#     def create(self, validated_data):
#         room_data = validated_data.pop('room')
#         room, created = Room.objects.get_or_create(**room_data)
#         consultation = Consultation.objects.create(room=room, **validated_data)
#         return consultation

#     def update(self, instance, validated_data):
#         room_data = validated_data.pop('room')
#         room, created = Room.objects.update_or_create(id=instance.room.id, defaults=room_data)

#         instance.doctor_name = validated_data.get('doctor_name', instance.doctor_name)
#         instance.patient_name = validated_data.get('patient_name', instance.patient_name)
#         instance.patient_age = validated_data.get('patient_age', instance.patient_age)
#         instance.recommended_treatment = validated_data.get('recommended_treatment', instance.recommended_treatment)
#         instance.room = room
#         instance.save()
#         return instance


from rest_framework import serializers
from .models import Room, Consultation

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Consultation
        fields = '__all__'

    def create(self, validated_data):
        room_data = validated_data.pop('room')
        room, created = Room.objects.get_or_create(**room_data)
        consultation = Consultation.objects.create(room=room, **validated_data)
        return consultation

    def update(self, instance, validated_data):
        room_data = validated_data.pop('room')
        room, created = Room.objects.update_or_create(id=instance.room.id, defaults=room_data)

        instance.patient_name = validated_data.get('patient_name', instance.patient_name)
        instance.patient_age = validated_data.get('patient_age', instance.patient_age)
        instance.recommended_treatment = validated_data.get('recommended_treatment', instance.recommended_treatment)
        instance.room = room
        instance.save()
        return instance
