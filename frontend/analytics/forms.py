from django import forms

class ProductFilterForm(forms.Form):
    min_price = forms.FloatField(min_value=0, required=False, label="Мин. цена")
    max_price = forms.FloatField(min_value=0, required=False, label="Макс. цена")
    min_rating = forms.FloatField(min_value=0, max_value=5, required=False, label="Мин. рейтинг")
    min_reviews = forms.IntegerField(min_value=0, required=False, label="Мин. отзывов")