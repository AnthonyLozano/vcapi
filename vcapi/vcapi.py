#!/usr/local/bin/python3 -u
import click
from clint.textui.progress import Bar as ProgressBar
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import logging
from os.path import expanduser

VERACODE_API_URL = 'https://analysiscenter.veracode.com/api/5.0/'

app_types = ["Application Design/Construction/IDE/Analysis",
             "Application Life-Cycle Management",
             "Application Server/Integration Server",
             "Back-Office Enterprise",
             "CRM",
             "Collaboration/Groupware/ Messaging",
             "Consumer",
             "Content Management/Authoring",
             "Engineering",
             "Enterprise Resource Planning",
             "Information Access/Delivery/Mining/Portal",
             "Information/Data Management/Database",
             "Middleware/Message-oriented/ Transaction",
             "Network Management",
             "Networking",
             "Other",
             "Other Development Tools",
             "Security",
             "ServerWare/Clustering/Web/VM",
             "Storage",
             "System-Level Software",
             "Systems Management",
             "Testing Tools"]

criticalities = ['Very High', 'High', 'Medium', 'Low', 'Very Low']

deployments = ["Web Based",
               "Enterprise Application",
               "Enhancement",
               "Client/Server",
               "Mobile",
               "Stand Alone"]

industries = ["Aerospace",
              "Agriculture",
              "Apparel",
              "Automotive and Transport",
              "Banking",
              "Beverages",
              "Biotechnology",
              "Business Services",
              "Charitable Organizations",
              "Chemicals",
              "Communications",
              "Computer Hardware",
              "Consulting",
              "Construction",
              "Consumer Products Manufacturers",
              "Consumer Services",
              "Cultural Institutions",
              "Education",
              "Electronics",
              "Energy",
              "Engineering",
              "Environmental",
              "Finance",
              "Food & Beverage",
              "Foundations",
              "Government",
              "Healthcare",
              "Hospitality",
              "Insurance",
              "Manufacturing",
              "Machinery",
              "Media & Entertainment",
              "Membership Organizations",
              "Metals and Mining",
              "Other",
              "Pharmaceuticals",
              "Real Estate",
              "Recreation",
              "Retail",
              "Security Products and Services",
              "Software",
              "Technology",
              "Telecommunications Equipment",
              "Telecommunications",
              "Transportation",
              "Utilities"]

origins = ["3rd party library",
           "Purchased Application",
           "Contractor",
           "Internally Developed",
           "Open Source",
           "Outsourced Team"]


class ApiCredential:
    """Stores the user's name and password"""
    def __init__(self, username=None, password=None, api_id=None, key=None):
        self.username = username
        self.password = password


@click.group()
@click.option('--cred-file', default=expanduser('~')+'/.veracoderc',
              help="Two line file containing username and password.")
@click.option('--verbose', '-v', is_flag=True, help="Enables logging")
@click.pass_context
def main(cred, cred_file, verbose):
    """
    Veracode command line interface.
    This function is the main command group for veracode's upload API.

    For documentation on each command check out
    https://analysiscenter.veracode.com/auth/helpCenter/api/c_UploadAPI_calls.html

    :param cred: click context
    :param cred_file: a file that contains your veracode username on one line, and your password on the next.
    :param verbose: When this flag is passed, logging will be enabled for python's request lib.
    """
    if verbose:
        # Enabling debugging at http.client level (requests->urllib3->http.client)
        # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
        # the only thing missing will be the response.body which is not logged.
        try:  # for Python 3
            from http.client import HTTPConnection
        except ImportError:
            from httplib import HTTPConnection
        HTTPConnection.debuglevel = 1
        logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
        logging.getLogger().setLevel(logging.INFO)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.INFO)
        requests_log.propagate = True
    cred.obj = read_credential_from_file(cred_file)


def read_credential_from_file(cred_file):
    with open(cred_file) as credentialFile:
        username = credentialFile.readline().strip()
        password = credentialFile.readline().strip()
    return ApiCredential(username, password)


@main.command("begin-scan")
@click.argument('app-id')
@click.option('--modules', '-m', multiple=True, help="Adds a module. Use multiple -m for multiple modules.")
@click.option('--scan-all-top-level-modules/--no-scan-all-top-level-modules', default=False)
@click.option('--scan-selected-modules/--no-scan-selected-modules', default=False)
@click.option('--scan-previously-selected-modules/--no-scan-previously-selected-modules', default=False)
@click.option('--sandbox-id')
@click.pass_obj
def begin_scan(credential, **payload):
    """Begins a scan."""
    api_endpoint = 'beginscan.do'
    if payload['modules']:
        payload['modules'] = ', '.join(payload['modules'])
    return api_submit(api_endpoint, credential, payload)


@main.command("begin-prescan")
@click.argument('app-id')
@click.option('--autoscan/--no-autoscan', default=False)
@click.option('--sandbox-id')
@click.option('--scan-all-nonfatal-top-level-modules/--no-scan-all-nonfatal-top-level-modules', default=False)
@click.pass_obj
def begin_prescan(credential, **payload):
    """
    Begins the prescan.
    """
    api_endpoint = "beginprescan.do"
    return api_submit(api_endpoint, credential, payload)


@main.command("create-app")
@click.argument("app-name")
@click.option("--description")
@click.option("--vender-id")
@click.argument("business-criticality", type=click.Choice(criticalities))
@click.option("--policy")
@click.option("--business-unit")
@click.option("--business-owner")
@click.option("--business-owner-email")
@click.option("--teams")
@click.option("--origin", type=click.Choice(origins))
@click.option("--industry", type=click.Choice(industries))
@click.option("--app-type", type=click.Choice(app_types))
@click.option("--deployment-method", type=click.Choice(deployments))
@click.option("--web-application", is_flag=True)
@click.option("--archer-app-name")
@click.option("--tags", "-t", help="Adds a tag. Can use multiple -t options for multiple tags")
@click.pass_obj
def create_app(credential, **payload):
    """Creates a new app."""
    api_endpoint = 'createapp.do'
    if payload['tags']:
        payload['tags'] = ', '.join(payload['tags'])
    api_submit(api_endpoint, credential, payload)


@main.command("create-build")
@click.argument('app-id')
@click.argument('version')
@click.pass_obj
def create_build(credential, **payload):
    """Creates a build."""
    api_endpoint = "createbuild.do"
    return api_submit(api_endpoint, credential, payload)


@click.argument("app-id")
@click.pass_obj
def delete_app(credential, **payload):
    """Deletes an app."""
    api_endpoint = "deleteapp.do"
    api_submit(api_endpoint, credential, payload)


@main.command("delete-build")
@click.argument("app-id")
@click.option("--sandbox-id", default=None, help="optional sandbox id")
@click.pass_obj
def delete_build(credential, **payload):
    """Deletes a build."""
    api_endpoint = "deletebuild.do"
    return api_submit(api_endpoint, credential, payload)


@main.command("get-app-info")
@click.argument("app-id")
@click.pass_obj
def get_app_info(credential, **payload):
    """Gets information for a particular app."""
    api_endpoint = "getappinfo.do"
    return api_submit(api_endpoint, credential, payload)


@main.command("get-app-list")
@click.pass_obj
def get_app_list(credential):
    """Gets a list of apps and their ids."""
    api_endpoint = "getapplist.do"
    return api_submit(api_endpoint, credential)


@main.command("get-build-info")
@click.argument('app-id')
@click.option('--build-id', default=None, help="Defaults to the most recent static scan.")
@click.option('--sandbox-id', default=None, help="Optional")
@click.pass_obj
def get_build_info(credential, **payload):
    """Gets info for an app build."""
    api_endpoint = "getbuildinfo.do"
    api_submit(api_endpoint, credential, payload)


@main.command("get-build-list")
@click.argument("app-id")
@click.option("--sandbox-id")
@click.pass_obj
def get_build_list(credential, **payload):
    """Gets a list of builds for an app."""
    api_endpoint = "getbuildlist.do"
    api_submit(api_endpoint, credential, payload)


@main.command("get-file-list")
@click.argument("app-id")
@click.option("--build-id", help="Defaults to most recent build-id")
@click.option("--sandbox-id")
@click.pass_obj
def get_file_list(credential, **payload):
    """Gets a list of files uploaded to a build."""
    api_endpoint = "getfilelist.do"
    api_submit(api_endpoint, credential, payload)


@main.command("get-policy-list")
@click.pass_obj
def get_policy_list(credential):
    """Gets a list of policies you have defined."""
    api_endpoint = "getpolicylist.do"
    api_submit(api_endpoint, credential)


@main.command("get-prescan-results")
@click.argument("app-id")
@click.option("--build-id", help="Defaults to most recent build-id")
@click.option("--sandbox-id")
@click.pass_obj
def get_prescan_results(credential, **payload):
    """Gets the results of a prescan."""
    api_endpoint = "getprescanresults.do"
    api_submit(api_endpoint, credential, payload)


@main.command("get-vendor-list")
@click.pass_obj
def get_vendor_list(credential):
    """Gets a list of vendors you have defined."""
    api_endpoint = "getvendorlist.do"
    api_submit(api_endpoint, credential)


@main.command("remove-file")
@click.argument("app-id")
@click.argument("file-id")
@click.option("--sandbox-id")
@click.pass_obj
def remove_file(credential, **payload):
    """Removes a file from an app."""
    api_endpoint = "removefile.do"
    api_submit(api_endpoint, credential, payload)


@main.command("update-app")
@click.argument("app-id")
@click.argument("app-name")
@click.option("--description")
@click.argument("business-criticality", type=click.Choice(criticalities))
@click.option("--policy")
@click.option("--business-unit")
@click.option("--business-owner")
@click.option("--business-owner-email")
@click.option("--teams")
@click.option("--origin", type=click.Choice(origins))
@click.option("--industry", type=click.Choice(industries))
@click.option("--app-type", type=click.Choice(app_types))
@click.option("--deployment-method", type=click.Choice(deployments))
@click.option("--archer-app-name")
@click.option("--tags", "-t", help="Adds a tag. Can use multiple -t options for multiple tags")
@click.option("--custom-field-name")
@click.option("--custom-field_value")
@click.pass_obj
def update_app(credential, **payload):
    """Updates an app. To add multiple custom fields, you have to call this api multiple times."""
    api_endpoint = 'updateapp.do'
    if payload['tags']:
        payload['tags'] = ', '.join(payload['tags'])
    api_submit(api_endpoint, credential, payload)


@main.command("update-build")
@click.argument("app-id")
@click.option("--build-id")
@click.option("--version")
@click.option("--lifecycle-stage")
@click.option("--launch-date", help="MM/dd/yyyy format")
@click.option("--sandbox-id")
@click.pass_obj
def update_build(credential, **payload):
    """Updates build infomation for a build."""
    api_endpoint = "updatebuild.do"
    api_submit(api_endpoint, credential, payload)


@main.command("upload-file")
@click.argument('app-id')
@click.argument('filename')
@click.option('--sandbox-id')
@click.option('--save-as')
@click.pass_obj
def upload_file(credential, app_id, filename, sandbox_id, save_as):
    """Uploads a file"""
    fields = {'app_id': app_id}
    if sandbox_id:
        fields['sandbox_id'] = sandbox_id
    if save_as:
        fields['save_as'] = save_as
    fields['file'] = (filename, open(filename, 'rb'), 'application/binary')
    encoder = MultipartEncoder(fields=fields)
    callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, callback)

    api_endpoint = "uploadfile.do"
    r = requests.post(VERACODE_API_URL + api_endpoint, data=monitor, headers={'Content-Type': encoder.content_type},
                      auth=(credential.username, credential.password))
    print(r.text)
    return r


def create_callback(encoder):
    bar = ProgressBar(expected_size=encoder.len, filled_char='=', hide=False)

    def callback(monitor):
        bar.show(monitor.bytes_read)
    return callback


def api_submit(api_endpoint, credential, payload=None, files=None):
    r = requests.post(VERACODE_API_URL + api_endpoint, params=payload, files=files,
                      auth=(credential.username, credential.password))
    print(r.text)
    return r


if __name__ == "__main__":
    main()
