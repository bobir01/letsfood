from django.db import models
from datetime import datetime
from django.utils.html import escape, mark_safe


class MerchatTransactionsModel(models.Model):
    _id = models.CharField(max_length=255, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=False)
    order_id = models.BigIntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True, )
    time = models.BigIntegerField(null=True, blank=True)
    perform_time = models.BigIntegerField(null=True, default=0)
    cancel_time = models.BigIntegerField(null=True, default=0)
    state = models.IntegerField(null=True, default=1)
    reason = models.CharField(max_length=255, null=True, blank=True)
    created_at_ms = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self._id} | {self.order_id} | {self.state} | {self.amount} "


class Orders(models.Model):
    class Meta:
        db_table = 'orders'

    order_id = models.BigIntegerField(verbose_name="Order id", null=False)
    user_id = models.BigIntegerField(verbose_name="User telegram_id", null=False)
    full_name = models.CharField(verbose_name='Name of User', max_length=50, null=False)
    phone = models.CharField(verbose_name='Phone of User', max_length=50, null=False)
    menu_id = models.IntegerField(verbose_name="Menu id", null=False)
    menu_type = models.CharField(verbose_name="Menu type", max_length=10, default="full", null=False)
    address_lat = models.FloatField(verbose_name="Address latitude", null=True)
    address_lon = models.FloatField(verbose_name="Address longitude", null=True)
    comment = models.CharField(verbose_name="Comment", max_length=255, null=True)
    quantity = models.IntegerField(verbose_name="Quantity", null=False)
    price = models.IntegerField(verbose_name="Price", null=False)
    event = models.CharField(verbose_name="Event", max_length=10, default='lunch', null=True)
    order_time = models.DateTimeField(verbose_name="Order time", null=True)
    is_paid = models.BooleanField(verbose_name="Is paid", default=False)

    def __str__(self):
        return "{order_id}  |  {user_id}  |  {full_name}  |  {phone}  |  {menu_id}  |  {menu_type}  |  {address_lat}  |  " \
               "{address_lon}  |  {comment}  |  {quantity} | {price} | {event}  |  {order_time}  |  {is_paid}".format(
            order_id=self.order_id,
            user_id=self.user_id,
            full_name=self.full_name,
            phone=self.phone,
            menu_id=self.menu_id,
            menu_type=self.menu_type,
            address_lat=self.address_lat,
            address_lon=self.address_lon,
            comment=self.comment,
            quantity=self.quantity,
            price=self.price,
            event=self.event,
            order_time=self.order_time.strftime("%d.%m.%Y %H:%M"),
            is_paid=self.is_paid
        )


class MenuLunch(models.Model):
    class Meta:
        db_table = 'menu_lunch'

    name = models.CharField(verbose_name="Name", max_length=255, null=False)
    price_full = models.IntegerField(verbose_name="Price full", null=False)
    price_par = models.IntegerField(verbose_name="Price partial", null=False)
    full_text_uz = models.TextField(verbose_name="Full text uz", null=False)
    full_text_ru = models.TextField(verbose_name="Full text ru", null=False)
    full_text_en = models.TextField(verbose_name="Full text en", null=False)
    par_text_uz = models.TextField(verbose_name="Partial text uz", null=False)
    par_text_ru = models.TextField(verbose_name="Partial text ru", null=False)
    par_text_en = models.TextField(verbose_name="Partial text en", null=False)
    photo = models.CharField(verbose_name="Photo", max_length=255, null=False)

    def __str__(self):
        return "{name}  |  {price_full}  |  {price_par}  |  {full_text_uz}  |  {full_text_ru}  |  {full_text_en}  |  " \
               "{par_text_uz}  |  {par_text_ru}  |  {par_text_en}  |  {photo}".format(
            name=self.name,
            price_full=self.price_full,
            price_par=self.price_par,
            full_text_uz=self.full_text_uz,
            full_text_ru=self.full_text_ru,
            full_text_en=self.full_text_en,
            par_text_uz=self.par_text_uz,
            par_text_ru=self.par_text_ru,
            par_text_en=self.par_text_en,
            photo=self.photo
        )

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.photo)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class MenuDinner(models.Model):
    class Meta:
        db_table = 'menu_dinner'

    name = models.CharField(verbose_name="Name", max_length=255, null=False)
    price_full = models.IntegerField(verbose_name="Price full", null=False)
    price_par = models.IntegerField(verbose_name="Price partial", null=False)
    full_text_uz = models.TextField(verbose_name="Full text uz", null=False)
    full_text_ru = models.TextField(verbose_name="Full text ru", null=False)
    full_text_en = models.TextField(verbose_name="Full text en", null=False)
    par_text_uz = models.TextField(verbose_name="Partial text uz", null=False)
    par_text_ru = models.TextField(verbose_name="Partial text ru", null=False)
    par_text_en = models.TextField(verbose_name="Partial text en", null=False)
    photo = models.CharField(verbose_name="Photo", max_length=255, null=False)

    def __str__(self):
        return "{name}  |  {price_full}  |  {price_par}  |  {full_text_uz}  |  {full_text_ru}  |  {full_text_en}  |  " \
               "{par_text_uz}  |  {par_text_ru}  |  {par_text_en}  |  {photo}".format(
            name=self.name,
            price_full=self.price_full,
            price_par=self.price_par,
            full_text_uz=self.full_text_uz,
            full_text_ru=self.full_text_ru,
            full_text_en=self.full_text_en,
            par_text_uz=self.par_text_uz,
            par_text_ru=self.par_text_ru,
            par_text_en=self.par_text_en,
            photo=self.photo
        )

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.photo)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
