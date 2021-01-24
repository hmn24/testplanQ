import psutil, subprocess, os, time
from qpython import qconnection

# Examples:
# kdbTP = kdbTP = kdbProc(proc='tickerplant', cmd=['kdb-tick/tick.q'], port=5010)
# kdbRDB = kdbProc(proc='realtimeDB', cmd=['kdb-tick/tick/r.q'], port=5011)


class kdbProc(object):
    def __init__(self, proc, cmd, host=None, port=None, username=None, password=None):

        if port is not None:
            cmd += ["-p", str(port)]
        self.cmd = ["q"] + cmd

        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password

        self.procName = proc
        self.logFile = f"{proc}.log"

    def startProc(self):
        # Sleep for about a second after starting to check if it started up
        logFileHdl = open(self.logFile, "a")
        try:
            self.proc = psutil.Popen(
                self.cmd, stdin=subprocess.DEVNULL, stdout=logFileHdl, stderr=logFileHdl
            )
            if self.checkAlive():
                print(f"{self.procName} is started successfully!")
            else:
                print(f"Error connecting to {self.procName}")
        except Exception as e:
            print(f"Error starting {self.procName}: {e}")

    def _queryProc(self, isSync, *args, **kwargs):
        # "Private" function
        try:
            with qconnection.QConnection(
                host="localhost" if self.host is None else self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            ) as q:
                res = (
                    q.sendSync(*args, **kwargs)
                    if isSync
                    else q.sendAsync(*args, **kwargs)
                )
        except Exception as e:
            print(f"Exception querying kdb process: {e}")
            res = None
        return res

    def syncQueryProc(self, *args, **kwargs):
        return self._queryProc(True, *args, **kwargs)

    def asyncQueryProc(self, *args, **kwargs):
        return self._queryProc(False, *args, **kwargs)

    def stopProc(self):
        try:
            if self.checkAlive():
                self.proc.terminate()
                time.sleep(1)
                if self.checkAlive():
                    print(f"Error stopping {self.procName} - Proceeding to SIGKILL")
                    self.proc.kill()
                if not self.checkAlive():
                    print(f"Successfully stopped {self.procName}")
        except Exception as e:
            print(f"Error stopping {self.procName}: {e}")

    def checkAlive(self):
        return self.proc.is_running()
