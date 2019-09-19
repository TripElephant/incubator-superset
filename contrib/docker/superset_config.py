# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os

from celery.schedules import crontab


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s:%s/%s" % (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")


class CeleryConfig(object):
    BROKER_URL = "redis://%s:%s/0" % (REDIS_HOST, REDIS_PORT)
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks")
    CELERY_RESULT_BACKEND = "redis://%s:%s/1" % (REDIS_HOST, REDIS_PORT)
    CELERY_TASK_PROTOCOL = 1
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True
    CELERY_ANNOTATIONS = {
        "sql_lab.get_sql_results": {"rate_limit": "100/s"},
        "email_reports.send": {
            "rate_limit": "1/s",
            "time_limit": 120,
            "soft_time_limit": 150,
            "ignore_result": True,
        },
    }
    CELERYBEAT_SCHEDULE = {
        "email_reports.schedule_hourly": {
            "task": "email_reports.schedule_hourly",
            "schedule": crontab(minute=1, hour="*"),
        }
    }


CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
    host=REDIS_HOST, port=REDIS_PORT, key_prefix="superset_results"
)

SECRET_KEY = ""

EMAIL_NOTIFICATIONS = True
SMTP_HOST = "smtp.sendgrid.net"
SMTP_USER = "apikey"
SMTP_PASSWORD = ""
SMTP_MAIL_FROM = ""

ENABLE_SCHEDULED_EMAIL_REPORTS = True
WEBDRIVER_BASEURL = "http://0.0.0.0:8088/"
EMAIL_REPORT_FROM_ADDRESS = ""
EMAIL_REPORT_BCC_ADDRESS = ""
EMAIL_REPORTS_WEBDRIVER = "chrome"
