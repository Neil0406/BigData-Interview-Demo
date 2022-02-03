# Generated by Django 3.2.5 on 2022-02-03 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='帳號(Email)')),
                ('name', models.CharField(max_length=255, verbose_name='姓名')),
                ('is_staff', models.BooleanField(default=False, verbose_name='管理員')),
                ('is_active', models.BooleanField(default=False, verbose_name='啟用帳號')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='超級使用者')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立日期')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]