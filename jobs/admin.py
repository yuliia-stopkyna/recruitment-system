from django.contrib import admin

from jobs.models import Jobs, JobHeaders, Applications


class JobHeadersInline(admin.TabularInline):
    model = JobHeaders
    extra = 1


@admin.register(Jobs)
class JobsAdmin(admin.ModelAdmin):
    inlines = [JobHeadersInline]


admin.site.register(JobHeaders)
admin.site.register(Applications)
