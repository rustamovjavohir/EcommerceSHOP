from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):  # PermissionsMixin
    objects = UserManager()
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    profile_image = models.ImageField(max_length=255, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True)
    username = models.CharField(_('username'),
                                max_length=150,
                                unique=True,
                                help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                }, )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
        null=True, blank=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ), null=True, blank=True
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['id']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def update_profile(self, validated_data):
        self.first_name = validated_data.get("first_name", self.first_name)
        self.last_name = validated_data.get("last_name", self.last_name)
        self.profile_image = validated_data.get(
            "profile_image", self.profile_image
        )
        self.email = validated_data.get("email", self.email)
        self.date_of_birth = validated_data.get(
            "date_of_birth", self.date_of_birth
        )
        self.save()
        return self

    def __str__(self):
        return f"{self.username}"

    @property
    def photo_url(self):
        try:
            return self.profile_image.url
        except Exception as e:
            return ''
