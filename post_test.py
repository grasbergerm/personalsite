import requests, json, re, urllib.parse

from string import Template
from bs4 import BeautifulSoup
import new_email


def read_value(soup, id):
    value = soup.find(id=id).get('value')
    if value.lower() == "n/a":
        return ""
    else:
        return value


def get_email(email):
    if email.lower() == "n/a":
        return ""
    else:
        return email


def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def create_message(your_name, best_school_contact_full_name, principal_full_name,
                   best_school_contact_email, principal_email, child_full_name, child_first_name,
                   school_name):
    message_template = read_template('message.txt')

    # create the addressee based on which contact is filled out in the application
    if best_school_contact_full_name or principal_full_name:
        addressee = ' and '.join(filter(None, list({best_school_contact_full_name, principal_full_name})))
    else:
        raise Exception('No best school contact name or principal name found, got ' +
                        ' and '.join([best_school_contact_full_name, principal_full_name]))

    # add in the values to the message template
    message = message_template.substitute(YOUR_NAME=your_name, ADDRESSEE=addressee,
                                          CHILD_FULL_NAME=child_full_name, CHILD_FIRST_NAME=child_first_name,
                                          SCHOOL_NAME=school_name)
    return (list(filter(None, list({get_email(best_school_contact_email), get_email(principal_email)}))), message)


def generate_email_params(username, apricot_username, apricot_password):
    # Create a session, holds all the cookies across API calls
    session = requests.Session()

    session = authenticate(apricot_password, apricot_username, session)

    report_json, session = get_report_json(session, username)

    # List of tuples containing addressee and message
    emails = []

    # Record each of the report ids from the JSON
    for ids in report_json['dataset']['groups']['All Rows']['document_ids']:
        # Report ID for the first record in the row
        report_id = ids[next(iter(ids.keys()))]

        # Setup for full report request
        url = "https://apricot.socialsolutions.com/document/edit/id/" + report_id
        session.headers.update({'Referer': "https://apricot.socialsolutions.com/auth/approved"})

        response = session.get(url)

        # Create a lovely soup of the report response
        soup = BeautifulSoup(response.text, 'html.parser')

        child_first_name = read_value(soup, "field_2_first")
        child_middle_name = read_value(soup, "field_2_middle")
        child_last_name = read_value(soup, "field_2_last")
        child_full_name = ' '.join(filter(None, [child_first_name, child_middle_name, child_last_name]))
        child_name_for_email_subject = ', '.join(
            filter(None, [child_last_name, ' '.join(filter(None, [child_first_name, child_middle_name]))]))

        school_info_form_id, school_info_url = new_email.get_url_for_school_info(report_json)

        response = session.get(school_info_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        school_name = read_value(soup, "field_541")

        best_school_contact_first_name = read_value(soup, "field_573_first")
        best_school_contact_middle_name = read_value(soup, "field_573_middle")
        best_school_contact_last_name = read_value(soup, "field_573_last")
        best_school_contact_full_name = ' '.join(filter(None, [best_school_contact_first_name,
                                                               best_school_contact_middle_name,
                                                               best_school_contact_last_name]))

        best_school_contact_email = read_value(soup, "field_579")

        principal_first_name = read_value(soup, "field_551_first")
        principal_middle_name = read_value(soup, "field_551_middle")
        principal_last_name = read_value(soup, "field_551_last")
        principal_full_name = ' '.join(filter(None, [principal_first_name, principal_middle_name, principal_last_name]))

        principal_email = read_value(soup, "field_555")

        emails.append(
            create_message(username, best_school_contact_full_name,
                           principal_full_name,
                           best_school_contact_email, principal_email, child_full_name, child_first_name, school_name))
    return emails, session, child_name_for_email_subject


def get_report_list(session):
    url = "https://apricot.socialsolutions.com/report/list"
    # Get reports list

    return session.get(url)


def get_report_json(session, username):
    url = "https://apricot.socialsolutions.com/report/list"
    # Get reports list

    response = session.get(url)
    # Get first name to identify report element
    first_name = username.split(' ')[0]
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(".*" + first_name + ".*")
    # Get link to report for username
    report_path = list(filter(lambda item: pattern.search(item.text.strip()), soup.find_all('h4')))[0].findNext('a')[
        'href']
    url = "https://apricot.socialsolutions.com" + report_path
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    state_id = soup.find('input', id='state_id')['value']
    section_id = \
        json.loads(soup.find('script', language="JavaScript").text.split("=", 1)[1].strip().strip(";"))['report_state'][
            'sections'][0]['id']
    # Setup for the report post
    url = "https://apricot.socialsolutions.com/report/refresh/reloading/false"
    session.headers.update({'Referer': "https://apricot.socialsolutions.com/bulletins/list"})
    payload = "state_id=" + state_id + "&section_id=" + section_id + "&mode=run&in_bulletin=true&fetchNew=true"
    response = session.post(url, data=payload)
    # Create a lovely soup of the report response
    soup = BeautifulSoup(response.text, 'html.parser')
    # Grab the JSON from the report response
    report_json = json.loads(soup.find(id="section_" + section_id + "_json").get('data-json'))
    return report_json, session


def authenticate(apricot_password, apricot_username, session):
    # Grab the initial cookie values
    session.get("https://apricot.socialsolutions.com/auth")
    # Setup for login post
    url = "https://apricot.socialsolutions.com/auth/check"
    payload = "serverLocation=https%3A%2F%2Fapricot.socialsolutions.com%2Fauth&username={0}&password={1}".format(
        urllib.parse.quote(apricot_username), urllib.parse.quote(apricot_password))
    session.headers.update(
        {'Referer': "https://apricot.socialsolutions.com/auth", 'content-type': "application/x-www-form-urlencoded"})
    # Login post
    response = session.post(url, data=payload)
    # If the account is logged in already message is found, send the new login request and update cookies accordingly
    if ("This account is currently logged in on another device" in response.text):
        url = "https://apricot.socialsolutions.com/auth/confirmnewlogin"
        response = session.get(url)
    return session
