from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

import jobs.views
from jobs.models import Jobs

job_updated = Signal()


@receiver(post_save, sender=Jobs)
def send_job_created_mail(sender, instance, created, **kwargs) -> None:
    if created:
        print(f"JOB {instance.id} CREATED")


@receiver(job_updated, sender=jobs.views.JobsViewSet)
def send_job_updated_mail(sender, **kwargs) -> None:
    print(f"JOB {kwargs['job_id']} UPDATED")
    print("OLD JOB TITLE: {}".format(kwargs["old_job_title"]))
    print("NEW JOB TITLE: {}".format(kwargs["new_job_title"]))
