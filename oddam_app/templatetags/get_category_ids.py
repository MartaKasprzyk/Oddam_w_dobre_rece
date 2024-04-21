from django import template

register = template.Library()


@register.filter
def category_ids(institution):
    ids = []
    for category in institution.categories.all():
        ids.append(category.pk)
    return ids
