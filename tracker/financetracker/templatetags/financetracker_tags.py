from django import template
from financetracker.models import Review

register = template.Library()


@register.inclusion_tag('financetracker/stars.html')
def show_stars(review_id):
    review = Review.objects.get(pk=review_id)
    stars_count = 5
    active_stars = [''] * int(review.grade)
    deactive_stars = [''] * (stars_count - int(review.grade))

    return {'active_stars': active_stars, 'deactive_stars': deactive_stars}
