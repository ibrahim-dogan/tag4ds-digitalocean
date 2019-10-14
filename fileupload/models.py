from django.db import models


# Create your models here.
class JsonFile(models.Model):
    name = models.CharField(max_length=100, default="uploaded_file")
    json = models.TextField(default='Json', null=False)
    tags_added = models.BooleanField(default=False)
    row_count = models.IntegerField(default=10)
    index = models.IntegerField(default=0)

    @property
    def get_processed_row_count(self):
        # return ProcessedRow.objects.filter(file_id=self.id).count()
        return self.index

    @property
    def complete_percentage(self):
        try:
            # return '{0:.2f}'.format(ProcessedRow.objects.filter(file_id=self.id).count() / self.row_count * 100)
            return '{0:.2f}'.format(self.index / self.row_count * 100)
        except:
            return 0.00


class Tag(models.Model):
    file = models.ForeignKey(JsonFile, models.CASCADE)
    tag = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    color = models.CharField(default='#FFF', max_length=20)
    percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.tag
