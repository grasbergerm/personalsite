import json
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


from bs4 import BeautifulSoup


def send_email(outlook_username, outlook_password, to_address, message, child_name_for_email_subject):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(outlook_username, outlook_password)

    msg = MIMEMultipart()  # create a message

    # setup the parameters of the message
    recipients = to_address
    msg['From'] = outlook_username
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Hopecam Connection for " + child_name_for_email_subject

    # add in the message body
    msg.attach(MIMEText(message, 'html'))

    # prompt to send message

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg


def get_textarea_value(soup, field_id):
    if "value" in soup.find_all('textarea', id=field_id)[0].attrs:
        return soup.find('textarea', id=field_id)['value']
    else:
        return ""


def get_other_value(soup, field_id):
    if "value" in soup.find_all('input', id=field_id)[0].attrs:
        return soup.find('input', id=field_id)['value']
    else:
        return ""


def get_checkbox_value(soup, field_id):
    for checkbox in soup.find_all('input', {"name": field_id}):
        if checkbox.has_attr('checked'):
            return checkbox['value']


def get_input_value(soup, field_id):
    return soup.find('input', id=field_id)['value']


def update_connection_status(session, username):
    import post_test

    report_json, session = post_test.get_report_json(session, username)

    connection_status_form_id, connection_status_url = get_url_for_connection_status(report_json)

    response = session.get(connection_status_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dupe_flag = get_input_value(soup, "dupeFlag")
    document_id = get_input_value(soup, "document_id")
    row_id = get_input_value(soup, "row_id")
    parent_id = get_input_value(soup, "parent_id")
    tier1_id = get_input_value(soup, "tier1_id")
    tier1_name = get_input_value(soup, "tier1_name")
    is_bulk = get_input_value(soup, "is_bulk")
    audit = get_input_value(soup, "audit")
    changed_fields = get_input_value(soup, "changed_fields")
    program_ids = get_input_value(soup, "program_ids")
    new_owner = get_input_value(soup, "new_owner")
    link_json = json.loads(get_input_value(soup, "link_json") or '{}')
    errors = get_input_value(soup, "errors")
    unique_key = get_input_value(soup, "unique_key")
    aff_type = get_input_value(soup, "aff_type")
    is_application = get_input_value(soup, "is_application")
    wizard_linked_document = get_input_value(soup, "wizard_linked_document")
    wizard_link_js = get_input_value(soup, "wizard_link_js")
    wizard_windowApricot = get_input_value(soup, "wizard_windowApricot")
    display_name_field_id = get_input_value(soup, "display_name_field_id")
    parent_program_ids = get_input_value(soup, "parent_program_ids")
    possible_program_ids = get_input_value(soup, "possible_program_ids")
    field_578_first = get_input_value(soup, "field_578_first")
    field_578_middle = get_input_value(soup, "field_578_middle")
    field_578_last = get_input_value(soup, "field_578_last")
    field_586 = get_input_value(soup, "field_586")
    field_586_dateType = get_other_value(soup, "field_586_dateType")
    field_592 = get_checkbox_value(soup, "field_592")
    field_592_other = get_other_value(soup, "field_592_other")
    field_588 = soup.find('select', id='field_588')['value']
    field_588_other = get_other_value(soup, "field_588_other")
    field_587 = get_input_value(soup, "field_587")
    field_587_dateType = get_other_value(soup, "field_587_dateType")
    field_589 = get_input_value(soup, "field_589")
    field_590 = get_input_value(soup, "field_590")
    field_721 = get_checkbox_value(soup, "field_721")
    field_721_other = get_other_value(soup, "field_721_other")
    field_444 = get_checkbox_value(soup, "field_444")
    field_444_other = get_input_value(soup, "field_444_other")
    field_495 = get_checkbox_value(soup, "field_495")
    field_495_other = get_other_value(soup, "field_495_other")
    field_640 = "Intro Email Sent- Awaiting School Response"
    field_640_other = get_other_value(soup, "field_640_other")
    field_725_other = get_other_value(soup, "field_725_other")
    field_445 = get_input_value(soup, "field_445")
    field_445_dateType = get_other_value(soup, "field_445_dateType")
    mod_time = get_input_value(soup, "mod_time")
    mod_user = get_input_value(soup, "mod_user")
    creation_time = get_input_value(soup, "creation_time")
    creation_user = get_input_value(soup, "creation_user")
    if soup.find('select', id='field_716').has_attr('value'):
        field_716 = soup.find('select', id='field_716')['value']
    else:
        field_716 = ""
    field_716_other = get_other_value(soup, "field_716_other")

    connection_status_update_url = "https://apricot.socialsolutions.com/document/save/form_id/{0}/parent_id/{1}/document_id/{2}".format(
        connection_status_form_id, parent_id, document_id)

    payload = {
        "form_id": str(connection_status_form_id),
        "dupeFlag": dupe_flag,
        "document_id": document_id,
        "row_id": row_id,
        "parent_id": parent_id,
        "tier1_id": tier1_id,
        "tier1_name": tier1_name,
        "is_bulk": is_bulk,
        "audit": audit,
        "changed_fields": changed_fields,
        "program_ids": program_ids,
        "new_owner": new_owner,
        "link_json": str(link_json),
        "errors": errors,
        "unique_key": unique_key,
        "aff_type": aff_type,
        "is_application": is_application,
        "wizard_linked_document": wizard_linked_document,
        "wizard_link_js": wizard_link_js,
        "wizard_windowApricot": wizard_windowApricot,
        "display_name_field_id": display_name_field_id,
        "parent_program_ids": parent_program_ids,
        "possible_program_ids": possible_program_ids,
        "field_578_first": field_578_first,
        "field_578_middle": field_578_middle,
        "field_578_last": field_578_last,
        "field_586": field_586,
        "field_586_dateType": field_586_dateType,
        "field_592": field_592,
        "field_592_other": field_592_other,
        "field_588": field_588,
        "field_588_other": field_588_other,
        "field_587": field_587,
        "field_587_dateType": field_587_dateType,
        "field_589": field_589,
        "field_590": field_590,
        "field_721": field_721,
        "field_721_other": field_721_other,
        "field_444": field_444,
        "field_444_other": field_444_other,
        "field_495": field_495,
        "field_495_other": field_495_other,
        "field_640[]": field_640,
        "field_640_other": field_640_other,
        "field_725_other": field_725_other,
        "field_445": field_445,
        "field_445_dateType": field_445_dateType,
        "mod_time": mod_time,
        "mod_user": mod_user,
        "creation_time": creation_time,
        "creation_user": creation_user,
        "field_716": field_716,
        "field_716_other": field_716_other,
    }

    session.post(connection_status_update_url, data=payload)

    school_info_form_id, school_info_url = get_url_for_school_info(report_json)

    response = session.get(school_info_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dupe_flag = get_input_value(soup, "dupeFlag")
    document_id = get_input_value(soup, "document_id")
    row_id = get_input_value(soup, "row_id")
    parent_id = get_input_value(soup, "parent_id")
    tier1_id = get_input_value(soup, "tier1_id")
    tier1_name = get_input_value(soup, "tier1_name")
    is_bulk = get_input_value(soup, "is_bulk")
    audit = get_input_value(soup, "audit")
    changed_fields = get_input_value(soup, "changed_fields")
    program_ids = get_input_value(soup, "program_ids")
    new_owner = get_input_value(soup, "new_owner")
    link_json = json.loads(get_input_value(soup, "link_json") or '{}')
    errors = get_input_value(soup, "errors")
    unique_key = get_input_value(soup, "unique_key")
    aff_type = get_input_value(soup, "aff_type")
    is_application = get_input_value(soup, "is_application")
    wizard_linked_document = get_input_value(soup, "wizard_linked_document")
    wizard_link_js = get_input_value(soup, "wizard_link_js")
    wizard_windowApricot = get_input_value(soup, "wizard_windowApricot")
    display_name_field_id = get_input_value(soup, "display_name_field_id")
    parent_program_ids = get_input_value(soup, "parent_program_ids")
    possible_program_ids = get_input_value(soup, "possible_program_ids")
    field_541 = get_input_value(soup, "field_541")
    field_574 = get_input_value(soup, "field_574")
    field_542_p1 = get_input_value(soup, "field_542_p1")
    field_542_p2 = get_input_value(soup, "field_542_p2")
    field_542_p3 = get_input_value(soup, "field_542_p3")
    field_542_p4 = get_input_value(soup, "field_542_p4")
    field_571_line1 = get_input_value(soup, "field_571_line1")
    field_571_line2 = get_input_value(soup, "field_571_line2")
    field_571_neighborhood = get_input_value(soup, "field_571_neighborhood")
    field_571_city = get_input_value(soup, "field_571_city")
    field_571_state = soup.find('select', id="field_571_state")['value']
    field_571_state_other = get_input_value(soup, "field_571_state_other")
    field_571_county = get_input_value(soup, "field_571_county")
    field_571_zip_p1 = get_input_value(soup, "field_571_zip_p1")
    field_571_zip_p2 = get_input_value(soup, "field_571_zip_p2")
    field_571_country = get_input_value(soup, "field_571_country")
    field_571_geolocation = get_input_value(soup, "field_571_geolocation")
    field_571_address_from = get_input_value(soup, "field_571_address_from")
    field_571_default_zoom_level = get_input_value(soup, "field_571_default_zoom_level")
    field_571_hide_map = get_input_value(soup, "field_571_hide_map")
    field_569 = get_input_value(soup, "field_569")
    field_569_dateType = get_other_value(soup, "field_569_dateType")
    field_570 = get_input_value(soup, "field_570")
    field_570_dateType = get_other_value(soup, "field_570_dateType")
    field_627 = get_checkbox_value(soup, "field_627")
    field_627_other = get_other_value(soup, "field_627_other")
    field_582 = get_input_value(soup, "field_582")
    field_577 = get_textarea_value(soup, "field_577")
    field_573_first = get_input_value(soup, "field_573_first")
    field_573_middle = get_input_value(soup, "field_573_middle")
    field_573_last = get_input_value(soup, "field_573_last")
    field_576 = get_input_value(soup, "field_576")
    field_579 = get_input_value(soup, "field_579")
    field_580_p1 = get_input_value(soup, "field_580_p1")
    field_580_p2 = get_input_value(soup, "field_580_p2")
    field_580_p3 = get_input_value(soup, "field_580_p3")
    field_580_p4 = get_input_value(soup, "field_580_p4")
    field_551_first = get_input_value(soup, "field_551_first")
    field_551_middle = get_input_value(soup, "field_551_middle")
    field_551_last = get_input_value(soup, "field_551_last")
    field_555 = get_input_value(soup, "field_555")
    field_559_p1 = get_input_value(soup, "field_559_p1")
    field_559_p2 = get_input_value(soup, "field_559_p2")
    field_559_p3 = get_input_value(soup, "field_559_p3")
    field_559_p4 = get_input_value(soup, "field_559_p4")
    field_562_first = get_input_value(soup, "field_562_first")
    field_562_middle = get_input_value(soup, "field_562_middle")
    field_562_last = get_input_value(soup, "field_562_last")
    field_566 = get_input_value(soup, "field_566")
    field_552_first = get_input_value(soup, "field_552_first")
    field_552_middle = get_input_value(soup, "field_552_middle")
    field_552_last = get_input_value(soup, "field_552_last")
    field_556 = get_input_value(soup, "field_556")
    field_553_first = get_input_value(soup, "field_553_first")
    field_553_middle = get_input_value(soup, "field_553_middle")
    field_553_last = get_input_value(soup, "field_553_last")
    field_557 = get_input_value(soup, "field_557")
    field_554_first = get_input_value(soup, "field_554_first")
    field_554_middle = get_input_value(soup, "field_554_middle")
    field_554_last = get_input_value(soup, "field_554_last")
    field_558 = get_input_value(soup, "field_558")
    field_572 = get_input_value(soup, "field_572")
    field_560_first = get_input_value(soup, "field_560_first")
    field_560_middle = get_input_value(soup, "field_560_middle")
    field_560_last = get_input_value(soup, "field_560_last")
    field_564 = get_input_value(soup, "field_564")
    field_561_first = get_input_value(soup, "field_561_first")
    field_561_middle = get_input_value(soup, "field_561_middle")
    field_561_last = get_input_value(soup, "field_561_last")
    field_565 = get_input_value(soup, "field_565")
    field_563_first = get_input_value(soup, "field_563_first")
    field_563_middle = get_input_value(soup, "field_563_middle")
    field_563_last = get_input_value(soup, "field_563_last")
    field_567 = get_input_value(soup, "field_567")
    field_568 = get_input_value(soup, "field_568")
    field_719 = datetime.today().strftime('%m/%d/%Y')
    field_719_dateType = get_other_value(soup, "field_719_dateType")
    field_720 = "Intro Email Sent"
    field_720_other = get_other_value(soup, "field_720_other")
    mod_time = get_input_value(soup, "mod_time")
    mod_user = get_input_value(soup, "mod_user")
    creation_time = get_input_value(soup, "creation_time")
    creation_user = get_input_value(soup, "creation_user")
    if soup.find('input', id="field_629_showhide_box").has_attr('CHECKED'):
        field_629_showhide = "on"
    else:
        field_629_showhide = "off"
    field_629 = get_input_value(soup, "field_629")
    field_629_link_count = get_input_value(soup, "field_629_link_count")

    school_info_update_url = "https://apricot.socialsolutions.com/document/save/form_id/{0}/parent_id/{1}/document_id/{2}".format(
        school_info_form_id, parent_id, document_id)

    payload = {
        "form_id": str(connection_status_form_id),
        "dupeFlag": dupe_flag,
        "document_id": document_id,
        "row_id": row_id,
        "parent_id": parent_id,
        "tier1_id": tier1_id,
        "tier1_name": tier1_name,
        "is_bulk": is_bulk,
        "audit": audit,
        "changed_fields": changed_fields,
        "program_ids": program_ids,
        "new_owner": new_owner,
        "link_json": str(link_json),
        "errors": errors,
        "unique_key": unique_key,
        "aff_type": aff_type,
        "is_application": is_application,
        "wizard_linked_document": wizard_linked_document,
        "wizard_link_js": wizard_link_js,
        "wizard_windowApricot": wizard_windowApricot,
        "display_name_field_id": display_name_field_id,
        "parent_program_ids": parent_program_ids,
        "possible_program_ids": possible_program_ids,
        "field_541": field_541,
        "field_574": field_574,
        "field_542_p1": field_542_p1,
        "field_542_p2": field_542_p2,
        "field_542_p3": field_542_p3,
        "field_542_p4": field_542_p4,
        "field_571_line1": field_571_line1,
        "field_571_line2": field_571_line2,
        "field_571_neighborhood": field_571_neighborhood,
        "field_571_city": field_571_city,
        "field_571_state": field_571_state,
        "field_571_state_other": field_571_state_other,
        "field_571_county": field_571_county,
        "field_571_zip_p1": field_571_zip_p1,
        "field_571_zip_p2": field_571_zip_p2,
        "field_571_country": field_571_country,
        "field_571_geolocation": field_571_geolocation,
        "field_571_address_from": field_571_address_from,
        "field_571_default_zoom_level": field_571_default_zoom_level,
        "field_571_hide_map": field_571_hide_map,
        "field_569": field_569,
        "field_569_dateType": field_569_dateType,
        "field_570": field_570,
        "field_570_dateType": field_570_dateType,
        "field_627": field_627,
        "field_627_other": field_627_other,
        "field_582": field_582,
        "field_577": field_577,
        "field_573_first": field_573_first,
        "field_573_middle": field_573_middle,
        "field_573_last": field_573_last,
        "field_576": field_576,
        "field_579": field_579,
        "field_580_p1": field_580_p1,
        "field_580_p2": field_580_p2,
        "field_580_p3": field_580_p3,
        "field_580_p4": field_580_p4,
        "field_551_first": field_551_first,
        "field_551_middle": field_551_middle,
        "field_551_last": field_551_last,
        "field_555": field_555,
        "field_559_p1": field_559_p1,
        "field_559_p2": field_559_p2,
        "field_559_p3": field_559_p3,
        "field_559_p4": field_559_p4,
        "field_562_first": field_562_first,
        "field_562_middle": field_562_middle,
        "field_562_last": field_562_last,
        "field_566": field_566,
        "field_552_first": field_552_first,
        "field_552_middle": field_552_middle,
        "field_552_last": field_552_last,
        "field_556": field_556,
        "field_553_first": field_553_first,
        "field_553_middle": field_553_middle,
        "field_553_last": field_553_last,
        "field_557": field_557,
        "field_554_first": field_554_first,
        "field_554_middle": field_554_middle,
        "field_554_last": field_554_last,
        "field_558": field_558,
        "field_572": field_572,
        "field_560_first": field_560_first,
        "field_560_middle": field_560_middle,
        "field_560_last": field_560_last,
        "field_564": field_564,
        "field_561_first": field_561_first,
        "field_561_middle": field_561_middle,
        "field_561_last": field_561_last,
        "field_565": field_565,
        "field_563_first": field_563_first,
        "field_563_middle": field_563_middle,
        "field_563_last": field_563_last,
        "field_567": field_567,
        "field_568": field_568,
        "field_719": field_719,
        "field_719_dateType": field_719_dateType,
        "field_720[]": field_720,
        "field_720_other": field_720_other,
        "mod_time": mod_time,
        "mod_user": mod_user,
        "creation_time": creation_time,
        "creation_user": creation_user,
        "field_629_showhide": field_629_showhide,
        "field_629": field_629,
        "field_629_link_count": field_629_link_count,

    }
    session.post(school_info_update_url, data=payload)


def get_url_for_connection_status(report_json):
    connection_status_form_id = 0
    for key in report_json['count_filters'].keys():
        if report_json['count_filters'][key] == "Connection Status Records":
            connection_status_form_id = key
    document_id = 0
    for column_obj in report_json['columns']:
        if report_json['columns'][column_obj]['name'] == "School Connection Process":
            document_id = report_json['dataset']['groups']['All Rows']['document_ids'][0][column_obj]
            break
    parent_id = report_json['dataset']['groups']['All Rows']['document_ids'][0] \
        [next(iter(report_json['dataset']['groups']['All Rows']['document_ids'][0].keys()))]
    url = "https://apricot.socialsolutions.com/document/edit/id/{0}/parent_id/{1}".format(document_id, parent_id)
    return connection_status_form_id, url


def get_url_for_school_info(report_json):
    school_info_form_id = 0
    for key in report_json['count_filters'].keys():
        if report_json['count_filters'][key] == "School Information Records":
            school_info_form_id = key
    document_id = 0
    for column_obj in report_json['columns']:
        if report_json['columns'][column_obj]['name'] == "Name of School":
            document_id = report_json['dataset']['groups']['All Rows']['document_ids'][0][column_obj]
            break
    parent_id = report_json['dataset']['groups']['All Rows']['document_ids'][0] \
        [next(iter(report_json['dataset']['groups']['All Rows']['document_ids'][0].keys()))]
    url = "https://apricot.socialsolutions.com/document/edit/id/{0}/parent_id/{1}".format(document_id, parent_id)
    return school_info_form_id, url