# How to schedule the worker script

In case the site you're acessing requires login, we suggest you hardcode the profile_name in the worker so it runs automatically.
Just edit this line in worker.py

`profile_name = input("Enter a profile name.  If no profile exists with this name, one will be created: ").strip()`

# Crontab (Linux, Mac)

To schedule the worker with crontab you can create a cronjob with

`crontab -e`

Example of how to make the worker run every day

`@daily python [PATH TO web_agent]/worker.py`

Full documentation

https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules

# Task Scheduler (Windows)

You can use task scheduler in Windows

https://learn.microsoft.com/en-us/windows/win32/taskschd/daily-trigger-example--scripting-

# Supervisord

You can also use supervisord as a task scheduler

http://supervisord.org/running.html
