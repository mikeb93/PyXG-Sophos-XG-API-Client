# PyXG - Sophos XG Python API Client

PyXG is a python API client for the Sophos XG Firewall

## Getting Started

Clone the repository or download the file.

### Prerequisites

Python3 is required.
The script was developed and tested with Python 3.7

Following modules are required

```
pip install click
```

### Usage and Examples

Run the script with a python3 interpreter.
The Script needs authentication credentials as well as the URL or DNS Hostname of the XG Appliance.

You can enter the ``-help`` option after every option/command to display context sensitive help

````
Usage: pyxg.py [OPTIONS] COMMAND [ARGS]...

Options:
  -U, --username TEXT  API User Name  [required]
  -P, --password TEXT  API User Password  [required]
  -u, --url TEXT       Hostname or IP of Sophos XG Appliance  [required]
  -p, --port TEXT      Webadmin Port [default: 4444]
  --help               Show this message and exit.

Commands:
  get  Get data from API
  set  Set data to API
````

#### Examples
##### Get DNS Commands

```
Options:
  --search [hostname|ip]
  --help                  Show this message and exit.
```

Search for Hostname in DNS
```
python3 pyxg.py -U apiuser -P 'IAmASafeAPIPass1234' -u mysophosxg.tld.com get dns --search=hostname myserver01

Hostname:  myserver01.tld.com
IP Address:  10.0.0.10

```

Search for IP in DNS

```
python3 pyxg.py -U apiuser -P 'IAmASafeAPIPass1234' -u mysophosxg.tld.com  get dns --search=ip 10.0.0.10

Hostname:  myserver01.tld.com
IP Address:  10.0.0.10
```

##### Set DNS commands

```
Options:
  -H, --hostname TEXT  Set FQDN Hostname  [required]
  -I, --ip TEXT        Set IP Address  [required]
  --recursive          Set if PTR Record should be created  [default: True]
  -v6                  Set IPv6 Address  [default: False]
  --help               Show this message and exit.
```

Set new DNS Record

```
python3 pyxg.py -U apiuser -P 'IAmASafeAPIPass1234' -u mysophosxg.tld.com set dns -H myserver02.tld.com -I 10.0.0.11

Configuration applied successfully.
```

##### Remove DNS commands

```
Options:
  -H, --hostname TEXT  Hostname FQDN to be removed  [required]
  --help               Show this message and exit.
```

Remove DNS Record

```
python3 pyxg.py -U apiuser -P 'IAmASafeAPIPass1234' -u mysophosxg.tld.com remove dns -H myserver02.tld.com -I 10.0.0.11

Configuration applied successfully.
```

## ToDo
* [ ] Implement more Get and Set commands other than DNS
* [ ] Implement a way to store credentials and url

## Contributing

Feel free to fork this repository and submit PR's.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

