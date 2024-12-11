# How to run automatically the worker script

In case the site you're acessing requires login, we suggest you hardcode the profile_id in the worker so it runs automatically.
Just edit this line in worlker.py

`profile_id = input("Enter a profileId (or press Enter to skip): ").strip()`

# Crontab (Linux, Mac)

To schedule the worker with crontab you can create a cronjob with

`crontab -e`

Example of how to make the worker run every day

`@daily python [PATH TO web_agent]/worker.py`

Full documentation

https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules?hl=pt-br

# Task Scheduler (Windows)

You can use task scheduler in Windows

https://learn.microsoft.com/en-us/windows/win32/taskschd/daily-trigger-example--scripting-

# Supervisord

You can use supervisord to setup the automation of your task

http://supervisord.org/running.html
