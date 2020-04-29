import requests
from argparse import ArgumentParser
import xml.etree.ElementTree as ET

# Create ArgumentParser and SubParser
parent_parser = ArgumentParser()
subarg = parent_parser.add_subparsers(title="Actions")
main_parser = ArgumentParser()

# Add auth Arguments
parent_parser.add_argument('-U', '--username', help='API User Name', required=True)
parent_parser.add_argument('-P', '--password', help='API User Password', required=True)
parent_parser.add_argument('-u', '--url', help='Hostname or IP of your Sophos XG Appliance', required=True)
parent_parser.add_argument('-p', '--port', help='Webadmin Port. (default: %(default)s)', default='4444', nargs='?',
                           required=False)

# Add Subargs for get commands
get_arg = subarg.add_parser('get', help='Get Information from API')
get_arg.add_argument('dns', help='Get DNS Information From API')

get_arg_dns = get_arg.add_mutually_exclusive_group(required=True)
get_arg_dns.add_argument('-H', '--hostname', help='Search for Hostname in DNS')
get_arg_dns.add_argument('-I', '--ip', help='Search for IP Address in DNS')

# Add Subargs for set commands
set_arg = subarg.add_parser('set', help='Set Information to API')
set_arg.add_argument('dns', help='Set DNS Host Record')
set_arg.add_argument('-H', '--hostname', help='Set Hostname of DNS Record as FQDN')
set_arg.add_argument('-I', '--ip', help='Set IP Address of DNS Record')
set_arg.add_argument('-R', '--reverse', help='Set reverse DNS Lookup', action='store_true', default='true')

# Parse args
args = parent_parser.parse_args()


def get_dns():
    """
    Fetch DNS Information from API depending on the entered Arguments.
    :return: String with either the IP Address or the Hostname
    """
    # API Request
    data = {'reqxml': (None, ET.tostring(request))}
    response = requests.post(api_url, files=data)
    result = ET.fromstring(response.text)

    if args.hostname:
        # Searching via Hostname
        print("Hostname: ", result[1][0].text)
        print("IP Address: ", result[1][1][0][2].text)
    elif args.ip:
        # Searching via IP (Dirty Workaround because the Filter wouldn't work on this stupid ass API)
        for data in result.findall('DNSHostEntry'):
            if data[1][0][2].text == get_keyvalue:
                print('Hostname: ', data.find('HostName').text)
                print('IP Address: ', data[1][0][2].text)
    else:
        # Searching for all DNS entities if no Hostname or IP was entered
        for data in result.findall('DNSHostEntry'):
            print('Hostname: ', data.find('HostName').text)
            print('IP Address: ', data[1][0][2].text, '\n')


def get_iphost():
    """
    Fetch IP Host Object information from API
    :return: String with IP or Host Object Name
    """
    data = {'reqxml': (None, xml_get_iphost)}
    response = requests.post(api_url, files=data)

    print(response.text)


def set_dns():
    """
    Set DNS Host Record
    :return:
    """


# Pre-Build XML with Auth
request = ET.Element('Request')
login = ET.SubElement(request, 'Login')
ET.SubElement(login, 'Username').text = args.username
ET.SubElement(login, 'Password').text = args.password

api_url = 'https://' + args.url + ':' + args.port + '/webconsole/APIController?'

if __name__ == '__main__':

    if args.dns:
        # DNS Parameter chosen
        if args.hostname:
            # Hostname Parameter chosen

            get_keyname = 'HostName'
            get_keyvalue = args.hostname

            # Continue building XML
            get = ET.SubElement(request, 'GET')
            dnshostentry = ET.SubElement(get, 'DNSHostEntry')
            filter = ET.SubElement(dnshostentry, 'Filter')
            ET.SubElement(filter, 'key', name='HostName', criteria='like').text = get_keyvalue

            # Call function
            get_dns()

        elif args.ip:
            # IP Parameter Chosen

            get_keyname = "IPAddress"
            get_keyvalue = args.ip

            # Continue building XML
            get = ET.SubElement(request, 'GET')
            dnshostentry = ET.SubElement(get, 'DNSHostEntry')
            addresslist = ET.SubElement(dnshostentry, 'AddressList')
            address = ET.SubElement(addresslist, 'Address')
            filter = ET.SubElement(address, 'Filter')
            ET.SubElement(filter, 'key', name='IPAddress', criteria='like').text = get_keyvalue

            # Call function
            get_dns()

        else:
            # Neither Hostname nor IP Parameter was chosen
            # Get everything in DNS if that's the case
            get = ET.SubElement(request, 'GET')
            dnshostentry = ET.SubElement(get, 'DNSHostEntry')
            get_dns()