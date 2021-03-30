#!/opt/tufin/securitysuite/ps/python/bin/python3

import argparse
import logging
import shlex
import sys

sys.path.append('/opt/tufin/securitysuite/ps/lib')

from Secure_Common.Logging.Logger import setup_loggers
from Secure_Common.Logging.Defines import COMMON_LOGGER_NAME
from Secure_Common.REST_Functions.Config import Secure_Config_Parser
from Secure_Change.Helpers import Secure_Change_Helper, Secure_Change_API_Handler

conf = Secure_Config_Parser()
logger = logging.getLogger(COMMON_LOGGER_NAME)
sc_helper = Secure_Change_Helper.from_secure_config_parser(conf)


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Print out logging information to STDOUT.')
    args = parser.parse_args(shlex.split(' '.join(sys.argv[1:])))
    return args


def update_ticket_field(ticket, comment):
    field = ""
    current_step = ticket.get_current_step()

    try:
        field = current_step.get_last_task().get_field_list_by_name("Informationen aus anderen Schritten")[0]

    except IndexError:
        logger.error("Field not found")

    field.set_field_value(comment)
    sc_helper.put_field(field)


def main():
    cli_args = get_cli_args()
    setup_loggers(conf.dict('log_levels'), log_to_stdout=cli_args.debug)

    ticket = sc_helper.get_ticket_by_id(8)

    print(ticket.subject)
    print(ticket.requester)

    user = sc_helper.get_user_by_username(ticket.requester)
    print(user.last_name)

    entscheidung = ticket.get_step_by_name("Re-Check").get_last_task().get_field_list_by_name("Ihre Entscheidung")[0]

    comment = "Requester: " + ticket.requester + "Titel: " + ticket.subject + "Entscheidung aus Schritt 2: " + entscheidung

    update_ticket_field(ticket, comment)

    print(123)
    print(234)


if __name__ == '__main__':
    main()
