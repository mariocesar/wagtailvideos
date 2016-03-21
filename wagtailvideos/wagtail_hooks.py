from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^videos/', include(urls, namespace='wagtailvideos', app_name='wagtailvideos')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('wagtailvideos/js/hallo-plugins/hallo-wagtailvideo.js'),
        static('wagtailvideos/js/video-chooser.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
            window.chooserUrls.videoChooser = '{0}';
            registerHalloPlugin('hallowagtailvideo');
        </script>
        """,
        urlresolvers.reverse('wagtailvideos:chooser')
    )


@hooks.register('register_admin_menu_item')
def register_images_menu_item():
    return MenuItem(
        _('Videos'), urlresolvers.reverse('wagtailvideos:index'),
        name='videos', classnames='icon icon-video', order=300
    )