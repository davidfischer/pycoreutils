from __future__ import print_function, unicode_literals
import collections
import logging
import sched
import subprocess
import sys
import time

import pycoreutils
import pycoreutils.lib


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    # TODO: Environment variables, different users and daemonize
    p.set_defaults(func=func)
    p.description = "Very simple cron daemon"
    p.epilog = "If CRONFILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_argument("filelist", nargs='+')
    p.add_argument("-l", "--logfile", dest="logfile", help="log to file")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                   help="show debug info")
    p.add_argument("--dryrun", action="store_true", dest="dryrun",
                   help="don't actually do anything")
    return p


def func(args):
    if args.logfile:
        logfile = open(args.logfile, 'a')
    else:
        logfile = sys.stdout

    scheduler = sched.scheduler(time.time, time.sleep)
    joblist = []
    Job = collections.namedtuple('Job',
                                 'min, hour, mday, mon, wday, user, cmd')

    # Create logger
    logger = logging.getLogger("crond")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(logfile)
    handler.setFormatter(logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    # Read crontab and load jobs
    for line in pycoreutils.lib.parsefilelist(args.FILE):
        # Strip comments and split the string
        split = line.strip().partition('#')[0].split(None, 6)
        if len(split) == 7:
            job = Job(min=split[0], hour=split[1], mday=split[2],
                        mon=split[3], wday=split[4], user=split[5],
                        cmd=split[6])
            joblist.append(job)
            if args.verbose:
                print('Read {0}'.format(job))
        elif split:
            print('Ignoring invalid line {0}'.format(line))

    def checkjobs():
        ''' Check if there are jobs available '''
        t = int(time.time() / 60 + 1) * 60  # start of the next minute
        scheduler.enterabs(t, 1, checkjobs, ())
        now = time.localtime(t)
        for job in joblist:
            if job.min in ['*', now.tm_min]    \
            and job.hour in ['*', now.tm_hour] \
            and job.mday in ['*', now.tm_mday] \
            and job.mon in ['*', now.tm_mon]   \
            and job.wday in ['*', now.tm_wday]:
                cmd = job.cmd
                if args.verbose:
                    logger.info("Running job {0}".format(cmd))

                if args.dryrun:
                    break

                # Run the command
                stdout, stderr = subprocess.Popen(cmd,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  shell=True).communicate()
                if args.verbose:
                    if stdout:
                        logger.info("{0}: {1}".format(cmd, stdout.strip()))
                    if stderr:
                        logger.error("{0}: {1}".format(cmd, stderr.strip()))
            else:
                if args.verbose:
                    logger.info("Skipping job {0}".format(job))

    scheduler.enter(1, 1, checkjobs, ())
    scheduler.run()
    print("No more jobs. This should not happen!", file=sys.stderr)
