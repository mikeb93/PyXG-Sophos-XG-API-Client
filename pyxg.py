import requests
import xml.etree.ElementTree as ET
import click


# Build main Options for Authentication
@click.group()
@click.option('-U', '--username', required=True, help='API User Name')
@click.option('-P', '--password', required=True, help='API User Password')
@click.option('-u', '--url', required=True, help='Hostname or IP of Sophos XG Appliance')
@click.option('-p', '--port', required=False, help='Webadmin Port', show_default=True, default='4444')
# Create context to store auth options -> passing them on to other commands
@click.pass_context
def main(ctx, username, password, url, port):
    # Build URL
    api_url = 'https://' + url + ':' + port + '/webconsole/APIController?'

    # Ensure context is an object, store options in context
    ctx.ensure_object(dict)
    ctx.obj['username'] = username
    ctx.obj['password'] = password
    ctx.obj['api_url'] = api_url


# Build Main Group for get/set commands
# Build get command
@main.group()
@click.pass_context
def get(ctx):
    """Get data from API"""
    pass


# Build subcommand 'dns', pass context, create option for Hostname etc
@get.command()
@click.pass_context
@click.option('--search', type=click.Choice(['hostname', 'ip'], case_sensitive=False))
@click.argument('value')
def dns(ctx, search, value):
    # Pre-Build XML with Auth
    request = ET.Element('Request')
    login = ET.SubElement(request, 'Login')
    ET.SubElement(login, 'Username').text = ctx.obj['username']
    ET.SubElement(login, 'Password').text = ctx.obj['password']

    # Pre-Build XML GET for DNS
    get = ET.SubElement(request, 'GET')
    dnshostentry = ET.SubElement(get, 'DNSHostEntry')

    if search == 'hostname':
        # Hostname Option chosen
        # Continue building XML
        filter = ET.SubElement(dnshostentry, 'Filter')
        ET.SubElement(filter, 'key', name='HostName', criteria='like').text = value

        # call function
        # API Request
        data = {'reqxml': (None, ET.tostring(request))}
        response = requests.post(ctx.obj['api_url'], files=data)
        result = ET.fromstring(response.text)

        # Searching via Hostname
        print("Hostname: ", result[1][0].text)
        print("IP Address: ", result[1][1][0][2].text)

    elif search == 'ip':
        # IP Option chosen
        # XML is already sufficient

        # API Request
        data = {'reqxml': (None, ET.tostring(request))}
        response = requests.post(ctx.obj['api_url'], files=data)
        result = ET.fromstring(response.text)

        # Searching via IP (Dirty Workaround because the Filter wouldn't work on this stupid ass API)
        for data in result.findall('DNSHostEntry'):
            if data[1][0][2].text == value:
                print('Hostname: ', data.find('HostName').text)
                print('IP Address: ', data[1][0][2].text)

    else:
        # XML is already sufficient
        # API Request
        data = {'reqxml': (None, ET.tostring(request))}
        response = requests.post(ctx.obj['api_url'], files=data)
        result = ET.fromstring(response.text)

        # Searching for all DNS entities if no Hostname or IP was entered
        for data in result.findall('DNSHostEntry'):
            print('Hostname: ', data.find('HostName').text)
            print('IP Address: ', data[1][0][2].text, '\n')


# Create set command in main group
@main.group()
@click.pass_context
def set(ctx):
    """Set data to API"""
    pass


# Build subcommand 'dns', pass context, create option for Hostname etc.
@set.command()
@click.pass_context
@click.option('-H', '--hostname', required=True, help='Set FQDN Hostname')
@click.option('-I', '--ip', required=True, help='Set IP Address')
@click.option('--recursive', is_flag=True, default=True, show_default=True, help='Set if PTR Record should be created')
@click.option('-v6', is_flag=True, default=False, show_default=True, help='Set IPv6 Address')
def dns(ctx, hostname, ip, recursive, v6):
    if v6:
        ipversion = "IPv6"
    else:
        ipversion = "IPv4"
    if recursive:
        recursion = "Enable"
    else:
        recursion = "Disable"

    # Build XML with Auth
    request = ET.Element('Request')
    login = ET.SubElement(request, 'Login')
    ET.SubElement(login, 'Username').text = ctx.obj['username']
    ET.SubElement(login, 'Password').text = ctx.obj['password']

    # Build Set XML
    set = ET.SubElement(request, 'SET')
    set.set('operation', 'add')
    dnshostentry = ET.SubElement(set, 'DNSHostEntry')
    ET.SubElement(dnshostentry, 'HostName').text = hostname
    addresslist = ET.SubElement(dnshostentry, 'AddressList')
    address = ET.SubElement(addresslist, 'Address')
    ET.SubElement(address, 'EntryType').text = "Manual"
    ET.SubElement(address, 'IPFamily').text = ipversion
    ET.SubElement(address, 'IPAddress').text = ip
    ET.SubElement(address, 'TTL').text = "60"
    ET.SubElement(address, 'Weight').text = "1"
    ET.SubElement(address, 'PublishOnWAN').text = "Disable"
    ET.SubElement(dnshostentry, 'AddReverseDNSLookUp').text = recursion

    # API Request
    data = {'reqxml': (None, ET.tostring(request))}
    response = requests.post(ctx.obj['api_url'], files=data)
    result = ET.fromstring(response.text)
    print(result[1][0].text)


# Create remove command
@main.group()
@click.pass_context
def remove(ctx):
    """Remove data to API"""
    pass


# Build subcommand 'dns' to remove command. Pass Context, add option
@remove.command()
@click.pass_context
@click.option('-H', '--hostname', required=True, help='Hostname FQDN to be removed')
def dns(ctx, hostname):
    # Build XML with Auth
    request = ET.Element('Request')
    login = ET.SubElement(request, 'Login')
    ET.SubElement(login, 'Username').text = ctx.obj['username']
    ET.SubElement(login, 'Password').text = ctx.obj['password']

    # Build Remove XML
    remove = ET.SubElement(request, 'Remove')
    dnshostentry = ET.SubElement(remove, 'DNSHostEntry')
    ET.SubElement(dnshostentry, 'HostName').text = hostname

    # API Request
    data = {'reqxml': (None, ET.tostring(request))}
    response = requests.post(ctx.obj['api_url'], files=data)
    result = ET.fromstring(response.text)
    print(result[1][0].text)


# EntryPoint
if __name__ == '__main__':
    main(obj={})
