# Idle Do

A script to run commands when your computer is idle. Simply prefix your command
with `idle_do.py`:

```idle_do.py my_resource_intensitive_job [args...]```

I use this to upload files using my slow DSL connection when I'm not around,
but it might be useful for other things, too.

Internally, this uses dbus and logind to receive notifications when the system
becomes idle, and Unix signals to control the running job.
