import requests
import xml.etree.ElementTree as ET
import click


# Build main Options for Authentication
@click.group()
@click.option('-U', '--username', required=True, help='API User Name')
@click.option('-P', '--password', required=True, help='API User Password')
@click.option('-u', '--url', required=True, help='Hostname or IP of Sophos XG Appliance')
@click.option('-p', '--port', required=False, help='Webadmin Port',show_default=True, default='4444')
# Create contect to store auth options -> passing them on to other commands
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
@main.group()
@click.pass_context
def get(ctx):
    """Get data from API"""
    pass


# Build get command, pass context, create option for Hostname
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


@main.group()
@click.pass_context
def set(ctx):
    """Set data to API"""
    pass


# Build get command, pass context, create option for Hostname
@set.command()
@click.pass_context
@click.option('-H', '--hostname', required=True)
@click.option('-I', '--ip', required=True)
def dns(ctx, hostname, ip):
    # Pre-Build XML with Auth
    request = ET.Element('Request')
    login = ET.SubElement(request, 'Login')
    ET.SubElement(login, 'Username').text = ctx.obj['username']
    ET.SubElement(login, 'Password').text = ctx.obj['password']

    click.echo("SET DNS CMD")


if __name__ == '__main__':
    main(obj={})
