import glob
import os
from datetime import datetime

import schedule as schedule
from django.core.management import call_command
from pytz import timezone


class BackupManager:
    SEPARATOR = '-'
    BACKUP_NAME = f"database{SEPARATOR}backup{SEPARATOR}%s.json"
    BACKUP_NAME_GLOB = f"database{SEPARATOR}backup{SEPARATOR}*.json"
    DATE_FORMAT = "%Y/%m/%d_%H:%M:%S_%z"
    BACKUP_COUNT = 10
    BACKUP_PATH = "/TiAPI/backup/%s"
    AUTO_BACKUP_INTERVAL = 120  # MINUTES
    TIMEZONE = timezone('UTC')

    @classmethod
    def open_backup_file(cls):
        f = open(cls.BACKUP_PATH.format(
            cls.BACKUP_NAME.format(datetime.strftime(datetime.now(tz=cls.TIMEZONE), cls.DATE_FORMAT))), "w+")
        yield f, f.name
        cls.delete_oldest_backups()

    @classmethod
    def backup(cls):
        f, filename = cls.open_backup_file()
        result = call_command('dumpdata', stdout=f)
        print(result)
        f.close()
        return filename

    @classmethod
    def restore(cls, name):
        if not os.path.exists(cls.BACKUP_PATH.format(name)):
            return f"Invalid backup name '{name}'. Please select a file from '{cls.BACKUP_PATH.format('')}' directory", False
        call_command('loaddata', cls.BACKUP_PATH.format(name))
        call_command('makemigrations')
        call_command('migrate')
        return "Restore successful", True

    @classmethod
    def get_backup_filenames(cls):
        return list(glob.glob(cls.BACKUP_PATH.format(cls.BACKUP_NAME_GLOB)))

    @classmethod
    def delete_oldest_backups(cls):
        files = {}
        for f in glob.glob(cls.BACKUP_PATH.format(cls.BACKUP_NAME_GLOB)):
            _, _, date = f.split(cls.SEPARATOR)
            date = date.split('.')[0]
            date = datetime.strptime(date, cls.DATE_FORMAT)
            files[date] = f
        dates = sorted(files, reverse=True)
        for i in range(len(dates)):
            if i >= cls.BACKUP_COUNT:
                os.remove(files[dates[i]])

    @classmethod
    def setup_auto_backup(cls):
        schedule.every(cls.AUTO_BACKUP_INTERVAL).minutes.do(cls.backup())
