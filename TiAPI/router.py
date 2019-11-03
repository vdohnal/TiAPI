from rest_framework.routers import DefaultRouter

from TiAPI.views import *

router = DefaultRouter(trailing_slash=False)
router.register('groups', CodeGroupViewSet, base_name='group')
router.register('codes', CodeViewSet, base_name='code')
