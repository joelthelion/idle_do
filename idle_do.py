#!/usr/bin/env python3
# coding: utf-8
""" Run a job (specified as command-line arguments) whenever the computer is
    idle, as defined by logind dbus events """
import sys
from signal import SIGCONT, SIGSTOP
import subprocess as sp
import pydbus
from gi.repository import GLib
import basic_logging as log


class Job:
    """ Resumable job, controlled by unix signals,
        with a dbus signal handler """

    def __init__(self):
        self.running = False
        self.proc = None

    def create(self):
        log.info("Creating job process")
        self.proc = sp.Popen(sys.argv[1:])

    def check_running(self):
        if self.proc is None:
            return
        ret = self.proc.poll()
        if ret is not None:
            log.info("Job process exited with return code %s."
                     " Preparing to exit", ret)
            sys.exit()

    def start(self):
        log.info("Preparing to start.")
        if self.proc is None:
            self.create()
        else:
            self.proc.send_signal(SIGCONT)

    def stop(self):
        log.info("Preparing to stop.")
        if self.proc is not None:
            self.proc.send_signal(SIGSTOP)

    def handler(self, *args, **kwargs):
        self.check_running()
        who, changed, _ = args
        log.debug(f"{who}, {changed}")
        if who != "org.freedesktop.login1.Manager":
            return
        if "IdleHint" in changed:
            idle = changed["IdleHint"]
            if idle:
                self.start()
            else:
                self.stop()


if __name__ == '__main__':
    job = Job()
    bus = pydbus.SystemBus()
    lg = bus.get(".login1")
    lg.onPropertiesChanged = job.handler
    GLib.MainLoop().run()
