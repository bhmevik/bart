#
# Configration and parsing module.
#
# Module for the SGAS Batch system Reporting Tool (BaRT).
#
# Author: Henrik Thostrup Jensen <htj@ndgf.org>
# Copyright: Nordic Data Grid Facility (2009, 2010)

import re
import ConfigParser
from optparse import OptionParser

DEFAULT_CONFIG_FILE     = '/etc/bart/bart.conf'
DEFAULT_USERMAP_FILE    = '/etc/bart/usermap'
DEFAULT_VOMAP_FILE      = '/etc/bart/vomap'
DEFAULT_LOG_FILE        = '/var/log/bart-logger.log'
DEFAULT_LOG_DIR         = '/var/spool/bart/usagerecords'
DEFAULT_STATEDIR        = '/var/spool/bart'
DEFAULT_IDTIMESTAMP     = 'false'
DEFAULT_SUPPRESS_USERMAP_INFO = 'false'

DEFAULT_MAUI_SPOOL_DIR  = '/var/spool/maui'
DEFAULT_MAUI_STATE_FILE = 'maui.state'
DEFAULT_TORQUE_SPOOL_DIR = '/var/spool/torque'
DEFAULT_TORQUE_STATE_FILE = 'torque.state'
DEFAULT_SLURM_STATE_FILE = 'slurm.state'

SECTION_COMMON = 'common'
SECTION_MAUI   = 'maui'
SECTION_TORQUE = 'torque'
SECTION_SLURM = 'slurm'

HOSTNAME   = 'hostname'
USERMAP    = 'usermap'
VOMAP      = 'vomap'
LOGDIR     = 'logdir'
LOGFILE    = 'logfile'
STATEDIR   = 'statedir'
IDTIMESTAMP = 'idtimestamp'
SUPPRESS_USERMAP_INFO = 'suppress_usermap_info'

MAUI_SPOOL_DIR  = 'spooldir'
MAUI_STATE_FILE = 'statefile'

TORQUE_SPOOL_DIR = 'spooldir'
TORQUE_STATE_FILE = 'statefile'

SLURM_STATE_FILE = 'statefile'

# regular expression for matching mapping lines
rx = re.compile('''\s*(.*)\s*"(.*)"''')



def getParser():

    parser = OptionParser()
    parser.add_option('-l', '--log-file', dest='logfile', help='Log file (overwrites config option).')
    parser.add_option('-c', '--config', dest='config', help='Configuration file.',
                      default=DEFAULT_CONFIG_FILE, metavar='FILE')
    return parser


def getConfig(config_file):

    cfg = ConfigParser.ConfigParser()
    cfg.read(config_file)
    return cfg


def getConfigValue(cfg, section, value, default=None):

    try:
        return cfg.get(section, value)
    except ConfigParser.NoSectionError:
        return default
    except ConfigParser.NoOptionError:
        return default


def getConfigValueBool(cfg, section, value, default=None):

    value = getConfigValue(cfg, section, value, default);
    if value.lower() in ('true', 'yes', '1'):
        return True
    elif value.lower() in ('false', 'no', '0'):
        return False
    else:
        logging.error('Invalid option for % (%)' % (value, idtimestamp))

    if default.lower() in ('true', 'yes', '1'):
        return True
    elif default.lower() in ('false', 'no', '0'):
        return False

    return False;


def readFileMap(map_file):

    map_ = {}

    for line in open(map_file).readlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = rx.match(line)
        if not m:
            continue
        key, mapped_value = m.groups()
        key = key.strip()
        mapped_value = mapped_value.strip()
        if mapped_value == '-':
            mapped_value = None
        map_[key] = mapped_value

    return map_


def getMapping(map_file):

    map_ = readFileMap(map_file)
    return map_


def getStateFile(cfg):
    if SECTION_MAUI in cfg.sections():
        return getConfigValue(cfg, SECTION_MAUI, MAUI_STATE_FILE, DEFAULT_MAUI_STATE_FILE)
    elif SECTION_TORQUE in cfg.sections():
        return getConfigValue(cfg, SECTION_TORQUE, TORQUE_STATE_FILE, DEFAULT_TORQUE_STATE_FILE)
    elif SECTION_SLURM in cfg.sections():
        return getConfigValue(cfg, SECTION_SLURM, SLURM_STATE_FILE, DEFAULT_SLURM_STATE_FILE)


