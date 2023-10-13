import csv

from django.http import HttpResponse


class ExportCsvMixin:

    @classmethod
    def export_as_csv(cls, queryset, **kwargs):
        file_name = kwargs.get("file_name", "csvfile")
        field_names = kwargs.get("field_names", [])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
