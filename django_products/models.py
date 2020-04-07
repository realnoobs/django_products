import uuid
import enum
from django.db import models
from django.db.utils import cached_property
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import translation, timezone
from django.core.validators import MinValueValidator

from taggit.models import TaggedItemBase, TagBase
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from polymorphic.models import PolymorphicModel, PolymorphicManager

from .utils import unique_slugify

_ = translation.gettext_lazy


class MaxLength(enum.Enum):
    SHORT = 128
    MEDIUM = 256
    LONG = 512
    XLONG = 1024
    TEXT = 2048
    RICHTEXT = 10000


class BaseManager(PolymorphicManager):
    """ Implement paranoid mechanism queryset """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return super().get(*args, **kwargs)


class ProductAbstract(PolymorphicModel):
    class Meta:
        abstract = True

    objects = BaseManager()

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_("The post title as you'd like it to be seen by the public"))
    # to reflect title of a current draft in the admin UI
    draft_title = models.CharField(
        max_length=255,
        editable=False)
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        verbose_name=_("price"))
    display_price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        verbose_name=_("display price"))
    slug = models.SlugField(
        unique=True, null=True,
        blank=False, max_length=80)
    is_deleted = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_('is deleted?'))
    deleted_by = models.ForeignKey(
        get_user_model(),
        editable=False,
        null=True, blank=True,
        related_name="deleted_%(class)ss",
        on_delete=models.CASCADE,
        verbose_name=_('deleter'))
    deleted_at = models.DateTimeField(
        null=True, blank=True, editable=False)
    owner = models.ForeignKey(
        get_user_model(),
        editable=False,
        null=True, blank=True,
        related_name="owned_%(class)ss",
        on_delete=models.CASCADE,
        verbose_name=_('owner'))
    created_at = models.DateTimeField(
        default=timezone.now, editable=False)
    modified_at = models.DateTimeField(
        null=True, blank=True, editable=False)

    def __str__(self):
        return self.title

    @cached_property
    def name(self):
        return self.title

    @property
    def opts(self):
        return self.get_real_instance_class()._meta

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        self.draft_title = self.title
        self.modified_at = timezone.now()
        super().save(**kwargs)

    def delete(self, using=None, keep_parents=False, paranoid=False):
        """
            Give paranoid delete mechanism to each record
        """
        if paranoid:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)


# TODO make swappable next time
class Category(MPTTModel):
    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = TreeForeignKey(
        'self', blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.'), )
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    @property
    def opts(self):
        return self._meta

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)


# TODO make swappable next time
class Tag(TagBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    @property
    def opts(self):
        return self._meta


# TODO make swappable next time
class TaggedProduct(TaggedItemBase):
    class Meta:
        verbose_name = _("Tagged Product")
        verbose_name_plural = _("Tagged Products")

    content_object = models.ForeignKey(
        'Product', on_delete=models.CASCADE,
        related_name='tagged_products')
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        related_name="tagged_products")


# TODO make swappable next time
class Product(ProductAbstract):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    tags = TaggableManager(
        through='TaggedProduct',
        blank=True,
        related_name='products',
        verbose_name=_("Tags"))
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("Category"))
