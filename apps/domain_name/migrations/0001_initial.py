# Generated by Django 2.1.7 on 2019-06-21 09:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DomainName',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('domain_name', models.CharField(max_length=20, verbose_name='域名')),
                ('project', models.CharField(blank=True, max_length=20, null=True, verbose_name='所属项目')),
                ('registrar', models.CharField(max_length=50, verbose_name='域名注册商')),
                ('registration_date', models.CharField(max_length=20, verbose_name='注册时间')),
                ('expiration_date', models.CharField(max_length=20, verbose_name='到期时间')),
                ('domain_status', models.IntegerField(verbose_name='状态')),
                ('dns_high_anti', models.CharField(blank=True, max_length=50, null=True, verbose_name='高防')),
                ('ch_lose', models.IntegerField(blank=True, default=2, null=True, verbose_name='被墙')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='Comment')),
            ],
            options={
                'verbose_name': 'DomainName',
                'db_table': 'domain_name',
            },
        ),
        migrations.CreateModel(
            name='DomainNameAccount',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('access_id', models.CharField(max_length=50, verbose_name='账号')),
                ('_access_key', models.CharField(max_length=128, verbose_name='key')),
                ('resolver', models.CharField(choices=[('aliyun', '阿里云')], max_length=50, verbose_name='所属域名解析商')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='Comment')),
            ],
            options={
                'db_table': 'domain_name_account',
            },
        ),
        migrations.CreateModel(
            name='DomainNameRecords',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('record_id', models.CharField(max_length=50, verbose_name='记录ID')),
                ('type', models.CharField(choices=[('A', 'A'), ('CNAME', 'CNAME'), ('AAAA', 'AAAA'), ('NS', 'NS'), ('MX', 'MX'), ('SRV', 'SRV'), ('TXT', 'TXT'), ('CAA', 'CAA'), ('REDIRECT_URL', '显性URL'), ('FORWARD_URL', '隐性URL')], max_length=15, verbose_name='记录类型')),
                ('rr', models.CharField(max_length=50, verbose_name='主机记录')),
                ('line', models.CharField(choices=[('default', '默认'), ('telecom', '电信'), ('unicom', '联通'), ('mobile', '移动'), ('oversea', '海外'), ('edu', '教育网'), ('drpeng', '鹏博士'), ('btvn', '广电网')], default='default', max_length=25, verbose_name='解析线路')),
                ('value', models.CharField(max_length=512, verbose_name='记录值')),
                ('priority', models.IntegerField(blank=True, null=True, verbose_name='MX优先级')),
                ('ttl', models.IntegerField(default=600, verbose_name='TTL')),
                ('status', models.CharField(default='ENABLE', max_length=10, verbose_name='状态')),
                ('locked', models.CharField(blank=True, max_length=10, null=True, verbose_name='锁定状态')),
                ('comment', models.TextField(blank=True, default='', max_length=128, verbose_name='Comment')),
                ('domain_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain_name.DomainName', verbose_name='域名')),
            ],
            options={
                'verbose_name': 'DomainNameRecords',
                'db_table': 'domain_name_records',
            },
        ),
        migrations.AlterUniqueTogether(
            name='domainnameaccount',
            unique_together={('name',)},
        ),
        migrations.AddField(
            model_name='domainname',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain_name.DomainNameAccount', verbose_name='所属账号'),
        ),
        migrations.AlterUniqueTogether(
            name='domainname',
            unique_together={('domain_name',)},
        ),
    ]
