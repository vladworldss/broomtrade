from django.core.exceptions import ValidationError


def validate_positive(value):
    if value < 0:
        raise ValidationError('Значение цены должно быть положительным!',
                              code='invalid')


def validate_price(cleaned_data):
    if cleaned_data['price'] == cleaned_data['new_price']:
        raise ValidationError('Цена с учетом скидки должна быть меньше!',
                              code='invalid')
