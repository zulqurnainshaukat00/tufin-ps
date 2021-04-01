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

    try:
        ticket_info = sc_helper.read_ticket_info()
    except ValueError:
        logger.info('Assuming script was triggered from test')
        sys.exit(0)

    ticket = sc_helper.get_ticket_by_id(ticket_info.id)

    # ticket = sc_helper.get_ticket_by_id(8)

    # print(ticket.subject)
    # print(ticket.requester)
    #
    # user = sc_helper.get_user_by_username(ticket.requester)
    # print(user.last_name)

    entscheidung = ticket.get_step_by_name("Re-Check").get_last_task().get_field_list_by_name("Ihre Entscheidung")[0].text

    urlaubstage = ticket.get_step_by_name("Urlaub in AERAsec").get_last_task().get_field_list_by_name("Wie Viel Tage brauchen Sie für Urlaub?")[0].text

    entscheidung2 = ticket.get_step_by_name("Überprüfen").get_last_task().get_field_list_by_name("Unterschrift mit Vor und Nachname")[0].text

    comment = "Requester: " + ticket.requester + "\nTitel: " + ticket.subject + "\nEntscheidung aus Schritt 2: " + entscheidung \
              + "\nAnzahl Urlaubstage: " + urlaubstage + "\nEntscheidungstep3: " + entscheidung2

    # update_ticket_field(ticket, comment)

    ticket_handler = Secure_Change_API_Handler(ticket, ticket_info)
    ticket_handler.register_action(Secure_Change_API_Handler.PRE_ASSIGNMENT_SCRIPT, update_ticket_field, ticket, comment)


    try:
        ticket_handler.run()
    except (ValueError, IOError) as error:
        logger.error('Failed to run Antragstellerinfos script. Error: %s', error)
        sys.exit(1)


if __name__ == '__main__':
    main()
