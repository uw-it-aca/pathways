from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("pathways", "0031_data_release_sync")]

    operations = [
        migrations.AddField(
            model_name="datareleasesyncattempt", name="claimed_on",
            field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(
            model_name="datareleasesyncattempt", name="worker_id",
            field=models.UUIDField(blank=True, null=True)),
        migrations.AlterField(
            model_name="datareleasesyncattempt", name="status",
            field=models.CharField(max_length=16, choices=[
                ("queued", "Queued"), ("downloading", "Downloading"),
                ("importing", "Importing"), ("succeeded", "Succeeded"),
                ("unchanged", "Unchanged"), ("failed", "Failed")])),
        migrations.AddConstraint(
            model_name="datareleasesyncattempt",
            constraint=models.UniqueConstraint(
                fields=("release_id",), condition=models.Q(status="queued"),
                name="unique_queued_release_sync")),
    ]