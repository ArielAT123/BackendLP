from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('is_vendor', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={'db_table': 'users'},
        ),

        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[
                    ('gaming', 'Gaming'),
                    ('laptop', 'Laptop'),
                    ('pc', 'PC'),
                    ('celular', 'Celular'),
                    ('tablet', 'Tablet'),
                    ('accesorio', 'Accesorio'),
                    ('ssd', 'SSD'),
                    ('ram', 'RAM'),
                ], max_length=50, unique=True)),
            ],
            options={'db_table': 'tags'},
        ),

        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_product', models.CharField(max_length=100, unique=True)),
                ('name_product', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('status', models.CharField(
                    max_length=20,
                    choices=[('active', 'Activo'), ('paused', 'Pausado'), ('sold', 'Vendido')],
                    default='active'
                )),
                ('vendor', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='products',
                    to='auth_app.user',
                    db_column='vendor_id'
                )),
                ('tags', models.ManyToManyField(blank=True, related_name='products', to='auth_app.tag')),
            ],
            options={'db_table': 'products'},
        ),
    ]
