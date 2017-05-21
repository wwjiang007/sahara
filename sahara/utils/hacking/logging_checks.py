#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import re


# NOTE(Kezar): this checks was copied from cinder/nova and should be one day
# appear at general hacking checks. So we need to try remember it and remove it
# when it'll be happened.
# FIXME(Kezar): may be it will be better to right in the way that introduced in
# keystone but it will need additional work and total checks refactoring.


accepted_log_level = re.compile(
    r"^LOG\.(debug|info|exception|warning|error|critical)\(")


def no_translate_debug_logs(logical_line, filename):
    """Check for 'LOG.debug(_('

    As per our translation policy,
    https://wiki.openstack.org/wiki/LoggingStandards#Log_Translation
    we shouldn't translate debug level logs.

    * This check assumes that 'LOG' is a logger.
    * Use filename so we can start enforcing this in specific folders instead
      of needing to do so all at once.
    S373
    """

    msg = "S373 Don't translate debug level logs"
    if logical_line.startswith("LOG.debug(_("):
        yield(0, msg)


def accepted_log_levels(logical_line, filename):
    """In Sahara we use only 5 log levels.

    This check is needed because we don't want new contributors to
    use deprecated log levels.
    S373
    """

    # NOTE(Kezar): sahara/tests included because we don't require translations
    # in tests. sahara/db/templates provide separate cli interface so we don't
    # want to translate it.

    ignore_dirs = ["sahara/db/templates",
                   "sahara/tests"]
    for directory in ignore_dirs:
        if directory in filename:
            return
    msg = ("S373 You used deprecated log level. Accepted log levels are "
           "debug|info|warning|error|critical")
    if logical_line.startswith("LOG."):
        if not accepted_log_level.search(logical_line):
            yield(0, msg)
