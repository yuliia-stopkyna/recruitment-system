def send_job_created_mail(job_id: int) -> None:
    print(f"JOB {job_id} CREATED")


def send_job_updated_mail(
    job_id: int, old_title_rich_text: str, new_title_rich_text: str
) -> None:
    print(f"JOB {job_id} UPDATED")
    print("OLD JOB TITLE: {}".format(old_title_rich_text))
    print("NEW JOB TITLE: {}".format(new_title_rich_text))
