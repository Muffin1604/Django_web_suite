from rest_framework import serializers 
from .. models import Carlist,Showroomlist,Review
        
def alphanumeric(value):
    if not str(value).isalnum():
        raise serializers.ValidationError("only alphanumeric characters are allowed")

'''class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField(read_only=True)
    chassisnumber = serializers.CharField(validators = [alphanumeric])
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    def create(self, validated_data):
        return Carlist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.chassisnumber = validated_data.get('chassisnumber', instance.chassisnumber)
        instance.price = validated_data.get('price', instance.price)

        instance.save()
        return instance'''
class ReviewSerializer(serializers.ModelSerializer):
    apiuser= serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('car',)
        #fields = "__all__"

class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    Reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Carlist
        fields = '__all__'
        #exclude = ['name']
    def get_discounted_price(self, object):
        discountprice = object.price - 5000
        return discountprice
    
    def validate_price(self,value):
        if value <= 20000.00:
            raise serializers.ValidationError("price must be greater than 20000.")
        return value
    def validate(self, data):
        if data['name'] == data ['description']:
            raise serializers.ValidationError("name and description must be different")
        return data

class ShowroomSerializer(serializers.ModelSerializer):
    #Showrooms = CarSerializer(many=True, read_only=True)
    Showrooms = serializers.StringRelatedField(many=True)
    '''Showrooms = serializers.HyperlinkedRelatedField(
        many = True,
        read_only =True,
        view_name='car_detail'
    )'''
    class Meta:
        model = Showroomlist
        fields = "__all__"

