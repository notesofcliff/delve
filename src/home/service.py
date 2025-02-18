import sys
import os
import signal
from time import sleep
import shlex
import logging
import subprocess
import socket

import django
os.environ["DJANGO_SETTINGS_MODULE"] = "flashlight.settings"
django.setup()
from django.conf import settings

import win32service
import win32serviceutil
import win32event

import psutil

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

class PySvc(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "flashlight"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "Flashlight (supervisor)"
    # this text shows up as the description in the SCM
    _svc_description_ = "Supervisor process for flashlight"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcDoRun(self):
        log = logging.getLogger(f"flashlight.{__name__}")
        import servicemanager
        commands = settings.FLASHLIGHT_SERVICE_COMMANDS
        # log.debug(f"Found {commands=}")
        rc = None
        # if the stop event hasn't been fired keep looping
        processes = {}
        log.debug(f"Entering main loop")
        while True:
            if self.stop_requested:
                logging.info("Service stopping.")
                break
            if processes:
                # Not first run
                log.debug(f"{processes=}")
                log.debug(f"Sleeping for {settings.FLASHLIGHT_SERVICE_INTERVAL} seconds.")
                sleep(settings.FLASHLIGHT_SERVICE_INTERVAL)
                # rc = win32event.WaitForSingleObject(self.hWaitStop, settings.FLASHLIGHT_SERVICE_INTERVAL*1000)
            for command in commands:
                if command not in processes:
                    # First run
                    log.debug(f"Creating process")
                    processes[command] = subprocess.Popen(
                        shlex.split(f"{command}", posix=False),
                        bufsize=-1,
                        executable=None,
                        stdin=None,
                        stdout=None,
                        stderr=None,
                        preexec_fn=None,
                        close_fds=True,
                        shell=False,
                        cwd=None,
                        env=None,
                        universal_newlines=None,
                        startupinfo=None,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                        # restore_signals=True,
                        # start_new_session=False,
                        pass_fds=(),
                        # group=None,
                        # extra_groups=None,
                        # user=None,
                        # umask=-1,
                        # encoding=None,
                        # errors=None,
                        # text=None,
                    )
                else:
                    # Already running, check status
                    rc = processes[command].poll()
                    if processes[command].returncode is None:
                        # Still running
                        log.debug(f"process for still running")
                    else:
                        # Stopped, try to create again
                        log.debug(f"Process found dead. Creating new process")
                        processes[command] = subprocess.Popen(
                            shlex.split(f"{command}", posix=False),
                            bufsize=-1,
                            executable=None,
                            stdin=None,
                            stdout=None,
                            stderr=None,
                            preexec_fn=None,
                            close_fds=True,
                            shell=False,
                            cwd=None,
                            env=None,
                            universal_newlines=None,
                            startupinfo=None,
                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                            # restore_signals=True,
                            # start_new_session=False,
                            pass_fds=(),
                            # group=None,
                            # extra_groups=None,
                            # user=None,
                            # umask=-1,
                            # encoding=None,
                            # errors=None,
                            # text=None,
                        )
        # First, send a terminate signal to all subprocesses
        for cmd, proc in processes.items():
            log.debug(f"Found {proc=}")
            log.info(f"Shutting down process")
            kill(proc.pid)
            try:
                out = proc.communicate(timeout=5)
                log.debug(f"Found {out=}")
            except subprocess.TimeoutExpired as exception:
                log.debug(f"Failed to gracefully stop process, {exception=}")

    def SvcStop(self):
        log = logging.getLogger(f"flashlight.{__name__}")
        log.warning("Shutting down")
        # tell the SCM we're shutting down
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop_requested = True
        # fire the stop event
        win32event.SetEvent(self.hWaitStop)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(PySvc)
