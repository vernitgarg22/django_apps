from django.db import models


class TestDataA(models.Model):
    app_label = 'default'

    data = models.CharField(max_length=8)


class TestDataB(models.Model):
    app_label = 'default'

    test_data_a = models.ForeignKey(TestDataA, on_delete=models.SET_NULL, null=True)
    data = models.CharField(max_length=8)
