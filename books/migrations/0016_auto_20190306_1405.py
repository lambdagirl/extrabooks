# Generated by Django 2.2b1 on 2019-03-06 22:05

import books.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_auto_20190225_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='rating_counts',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='book',
            name='city',
            field=models.CharField(max_length=50, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price'),
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=books.models.user_directory_path)),
                ('thumbnail', models.ImageField(null=True, upload_to=books.models.user_directory_path2)),
                ('book', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='books.Book')),
            ],
        ),
    ]
