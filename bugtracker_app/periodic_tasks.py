from django_cron import CronJobBase, Schedule
from datetime import datetime


class Test(CronJobBase):
    RUN_EVERY_MINS = 1  - 0.1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'    # a unique code

    def do(self):
        with open("foo.txt", "a") as f:
            f.write("\n"+str(datetime.now()))