# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import APIView, Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics

from django.views.generic.detail import SingleObjectMixin

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin, IsAppUser, IsOrgAdminOrAppUser

from ..models import DomainName, Records, Account
from .. import serializers

from ..domain_name_api import DomainNameApi
from ..beian import beian
from ..check_gfw import CheckGFW


logger = get_logger(__file__)
__all__ = ['AccountViewSet', 'DomainNameViewSet', 'RecordsViewSet',
         'DomainNameNetAPIUpdateApi', 'DomainNameRecordUpdateApi', 
         'DomainNameBeiAnCheckApi', 'DomainNameGFWCheckApi']
GetDomainName=DomainNameApi()
BeiAnCheck=beian()
GFWCheck = CheckGFW()

class AccountViewSet(BulkModelViewSet):
    filter_fields = ("name", "resolver")
    search_fields = filter_fields
    queryset = Account.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.DomainNameAccountSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        return queryset

class DomainNameViewSet(BulkModelViewSet):
    filter_fields = ("domain_name", "project")
    search_fields = filter_fields
    queryset = DomainName.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.DomainNameSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        return queryset

class DomainNameNetAPIUpdateApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def get(self, request, *args, **kwargs):
        domain_name_account = Account.objects.all()
        for account in domain_name_account:
            domain_name_data = GetDomainName.domain_name_list(account)
            if domain_name_data['code']:
                domain_name_data = domain_name_data['message']
                for domain_name_info in domain_name_data:
                    domain_name = domain_name_info['DomainName']
                    db_domain_name = get_object_or_none(DomainName,domain_name=domain_name)
                    if not db_domain_name:
                        try:
                            DomainName.objects.create(
                                account = account,
                                domain_name = domain_name_info['DomainName'],
                                registrar = account.get_resolver_display,
                                registration_date = domain_name_info['RegistrationDate'],
                                expiration_date = domain_name_info['ExpirationDate'],
                                domain_status = domain_name_info['DomainStatus']
                            )
                        except Exception as e:
                            return Response({"failed": e}, status=404)
                    else:
                        db_domain_name.account = account
                        if domain_name_info['RegistrationDate']:
                            db_domain_name.registration_date = domain_name_info['RegistrationDate']
                        if domain_name_info['ExpirationDate']:
                            db_domain_name.expiration_date = domain_name_info['ExpirationDate']
                        db_domain_name.domain_status = domain_name_info['DomainStatus']
                        try:
                            db_domain_name.save()
                        except Exception as e:
                            return Response({"failed": e}, status=404)
                return Response({"msg": "ok"})
            else:
                return Response({'error': domain_name_data['message']}, status=400)

class DomainNameBeiAnCheckApi(generics.UpdateAPIView):
    queryset = DomainName.objects.all()
    permission_classes = (IsOrgAdmin,)

    def update(self, request, *args, **kwargs):
        domain = self.get_object()
        try:
            beian_check = BeiAnCheck.check_beian_slow(domain.domain_name)
            code = beian_check.get('code')
            if code == -1:
                return Response({'msg': beian_check.get('msg')}, status=400)
            domain.beian = code
            domain.save()
            return Response({"msg": "%s备案状态:%s" % (domain,code)})
        except:
            return Response(status=400)

class DomainNameGFWCheckApi(generics.UpdateAPIView):
    queryset = DomainName.objects.all()
    permission_classes = (IsOrgAdmin,)

    def update(self, request, *args, **kwargs):
        domain = self.get_object()
        try:
            gfw_check = GFWCheck.check_gfw(domain.domain_name)
            code = gfw_check.get('code')
            if code == -1:
                return Response({'msg': gfw_check.get('msg')}, status=400)
            domain.ch_lose = code
            domain.save()
            return Response({"msg": "%s被墙状态:%s" % (domain,code)})
        except Exception as e:
            return Response({'msg': e}, status=400)

class RecordsViewSet(BulkModelViewSet):
    filter_fields = ("domain_name",)
    search_fields = ("value", "rr")
    queryset = Records.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.RecordsSerializer
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        try:
            req = request.data.copy()
            domain_name = req.get('domain_name')
            domain = DomainName.objects.get(domain_name=domain_name)

            req['domain_name'] = domain.id
            serializer = self.serializer_class(data=req)
            if serializer.is_valid():
                record = serializer.save()
                add_record = GetDomainName.record_create(record)
                if add_record['code']:
                    add_record = add_record['message']
                    record.record_id = add_record['RecordId']
                    serializer.save()
                    return Response({'msg': 'success'}, status=200)
                else:
                    return Response({'msg': add_record}, status=400)
            else:
                return Response({'msg':serializer.errors}, status=400)
        except Exception as e:
            return Response({'msg': e}, status=400)

    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        del_record = GetDomainName.record_remove(record)
        if del_record['code']:
            record.delete()
            return Response({"msg": "ok"})
        else:
            return Response({'error': del_record['message']}, status=400)

class DomainNameRecordUpdateApi(generics.UpdateAPIView):
    queryset = Records.objects.all()
    serializer_class = serializers.RecordStatusUpdateSerializer
    permission_classes = (IsOrgAdmin,)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            status = serializer.validated_data['status']
            record.status = status
            set_status = GetDomainName.record_status(record)
            if set_status['code']:
                record.save()
                return Response({"msg": "ok"})
            else:
                return Response({'error': del_record['message']}, status=400)
        else:
            return Response({'error': serializer.errors}, status=400)