from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number',   models.CharField(editable=False, max_length=20, unique=True)),
                ('title',           models.CharField(max_length=200)),
                ('description',     models.TextField()),
                ('category',        models.CharField(max_length=30, choices=[
                    ('hardware','Hardware Issue'),('software','Software Issue'),
                    ('network','Network / Internet'),('email','Email / Outlook'),
                    ('printer','Printer / Scanner'),('access','Access / Login'),
                    ('erp','ERP System'),('other','Other'),
                ])),
                ('priority',        models.CharField(max_length=20, default='medium', choices=[
                    ('low','Low'),('medium','Medium'),('high','High'),('critical','Critical'),
                ])),
                ('status',          models.CharField(max_length=20, default='open', choices=[
                    ('open','Open'),('in_progress','In Progress'),('on_hold','On Hold'),
                    ('resolved','Resolved'),('closed','Closed'),
                ])),
                ('resolution_note', models.TextField(blank=True)),
                ('resolved_at',     models.DateTimeField(blank=True, null=True)),
                ('created_at',      models.DateTimeField(auto_now_add=True)),
                ('updated_at',      models.DateTimeField(auto_now=True)),
                ('raised_by',       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raised_tickets',   to=settings.AUTH_USER_MODEL)),
                ('assigned_to',     models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name': 'Help Desk Ticket'},
        ),
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment',     models.TextField()),
                ('is_internal', models.BooleanField(default=False, verbose_name='Internal Note (IT only)')),
                ('created_at',  models.DateTimeField(auto_now_add=True)),
                ('ticket',  models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',        to='helpdesk.ticket')),
                ('author',  models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['created_at']},
        ),
    ]
