from django.contrib import admin

from products.models import (
    Product,
    SpecificationName,
    SpecificationValue,
    Specifications,
    Review,
    ImagesProduct
)

admin.site.register(SpecificationName)
admin.site.register(SpecificationValue)
admin.site.register(Specifications)


class ImagesProductInLine(admin.StackedInline):
    model = ImagesProduct


class ReviewsInLine(admin.StackedInline):
    model = Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (
        'category',
        'price',
        'count',
        'title',
        'description',
        'full_description',
        'free_delivery',
        'tags',
    )
    inlines = [
        ImagesProductInLine,
        ReviewsInLine,
        ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'product',
        'text',
        'rate',
    )
