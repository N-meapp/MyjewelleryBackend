# Generated by Django 5.2.3 on 2025-06-13 11:53

import cloudinary.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gemstone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_images', models.JSONField(blank=True, default=list, null=True)),
                ('main_mobile_img', models.JSONField(blank=True, default=list, null=True)),
                ('main_img', models.JSONField(blank=True, default=list, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('otp', models.CharField(max_length=6)),
                ('is_verified', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchGif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('categories', 'Categories'), ('occasions', 'Occasions'), ('price', 'Price'), ('gender', 'Gender')], max_length=20)),
                ('label', models.CharField(max_length=100)),
                ('icon', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('mobile', models.BigIntegerField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Metal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('karat', models.FloatField(blank=True, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.material')),
            ],
        ),
        migrations.CreateModel(
            name='NavbarCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_handcrafted', models.BooleanField(default=False)),
                ('handcrafted_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('is_all_jewellery', models.BooleanField(default=False)),
                ('all_jewellery_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('is_gemstone', models.BooleanField(default=False)),
                ('gemstone_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.category')),
                ('gemstone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.gemstone')),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.material')),
                ('occasion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewelleryapp.occasion')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=255)),
                ('metal_weight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('karat', models.FloatField(blank=True, null=True)),
                ('images', models.JSONField(blank=True, null=True)),
                ('ar_model_glb', models.URLField(blank=True, null=True)),
                ('ar_model_gltf', models.URLField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=1550, null=True)),
                ('pendant_width', models.CharField(blank=True, max_length=20, null=True)),
                ('pendant_height', models.CharField(blank=True, max_length=20, null=True)),
                ('frozen_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('making_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('making_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('product_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('gst', models.DecimalField(decimal_places=2, default=3, max_digits=10)),
                ('handcrafted_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_handcrafted', models.BooleanField(default=False)),
                ('is_classic', models.BooleanField(default=False)),
                ('designing_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_stock', models.PositiveIntegerField(default=0)),
                ('sold_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.category')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.gender')),
                ('metal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.metal')),
                ('occasion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.occasion')),
                ('stones', models.ManyToManyField(blank=True, related_name='products', to='jewelleryapp.gemstone')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='jewelleryapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
                ('weight', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.product')),
                ('stone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.gemstone')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.BigIntegerField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jewelleryapp.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Visit',
                'verbose_name_plural': 'User Visits',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='jewelleryapp.product')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]
