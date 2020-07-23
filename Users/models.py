import unicodedata

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from Core.settings import DOMAIN_NAME


def normalize_username(username):
    return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username


class UserManager(BaseUserManager):
    def create_user(
            self, username, email, first_name, last_name, userRole, discordID, password=None,
            commit=True):
        """
        Creates and saves a User with the given username, first name, last name
        and password.
        """
        if not username:
            raise ValueError(_('Users must have an username address'))
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        if not userRole:
            raise ValueError(_('userRole. Enter one.'))

        user = self.model(
            username=normalize_username(username),
            email=email,
            first_name=first_name,
            last_name=last_name,
            userRole=userRole,
            discordID=discordID,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, userRole, password, discordID):
        """
        Creates and saves a superuser with the given username, first name,
        last name and password.
        """
        user = self.create_user(
            username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            userRole=userRole,
            discordID=discordID,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'auth_user'

    username = models.CharField(
        verbose_name=_('username'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    userRole = models.CharField(_('userRole'), max_length=255)
    discordID = models.CharField(_('discordID'), max_length=255, blank=True)
    last_known_ip_address = models.CharField(_('last_ip'), max_length=20, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'userRole', 'discordID']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        #'reset_password_url': DOMAIN_NAME + "{}?token={}".format(reverse('password_reset:reset-password-request'),
        #                                           reset_password_token.key)
        'reset_password_url': DOMAIN_NAME + '/set-new-password/' + "{}".format(reset_password_token.key)
    }
    # render email text
    email_html_message = render_to_string('users/email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('users/email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title='HLHAvailSPA'),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
