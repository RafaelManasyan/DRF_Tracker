from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('tracker', '0006_habit_last_notified_alter_habit_period'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE tracker_habit
                ALTER COLUMN period TYPE smallint USING period::smallint;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
