from django.db import models


class FakeDashboard(models.Model):
    id = models.AutoField(primary_key=True)
    fake_name = models.CharField(max_length=1)

    class Meta:
        db_table = "fake_dashboards"
        verbose_name = "dashboard"
