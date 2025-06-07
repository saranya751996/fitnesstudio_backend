from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
import uuid
from django.http import JsonResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class Timestamps(models.Model):
    datetime_created = models.DateTimeField(
        _("Date created"), auto_now_add=True, db_index=True)
    datetime_updated = models.DateTimeField(
        _("Date updated"), auto_now=True, db_index=True)

    class Meta:
        abstract = True


class SoftDelete(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        abstract = True


class ResponseViewMixin(object):
    ignore_keys = ['non_field_errors', ]
    renderer_classes = [JSONRenderer, ]

    @staticmethod
    def jp_response(s_code='HTTP_200_OK', data=None):
        response = JsonResponse({'status': getattr(status, s_code),
                                 'data': data,
                                 'success': True})
        response.status_code = getattr(status, s_code)
        return response

    @staticmethod
    def jp_error_response(s_code='HTTP_500_INTERNAL_SERVER_ERROR', e_code='EXCEPTION', data=None):

        # print("Error code", ERROR_CODE)
        print("E code", e_code)
        if e_code == 'EXCEPTION':
            e_code = data
        # response = JsonResponse({'status': getattr(status, s_code),
        #                          'success': False,
        #                          'error': {'code': getattr(ERROR_CODE, e_code),
        #                                    'message': data}})
        response = JsonResponse({'status': getattr(status, s_code),
                                'success': False,
                                 'error': {'message': e_code}})
        response.status_code = getattr(status, s_code)
        return response

    def exception_response(self, data=None):
        return self.jp_error_response('HTTP_500_INTERNAL_SERVER_ERROR', data, data)

    def error_msg_list(self, errors):
        errors_list = []
        for k, v in errors.items():
            if isinstance(v, dict):
                v = self.error_msg_list(v)
            for msg in v:
                if k in self.ignore_keys:
                    errors_list.append(msg)
                else:
                    errors_list.append(
                        ' '.join(k.title().split('_')) + '- ' + str(msg))
        return errors_list
