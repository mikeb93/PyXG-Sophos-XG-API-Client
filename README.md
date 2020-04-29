# PyXG - Sophos XG Python API Client

PyXG is a python API client for the Sophos XG Firewall

## Getting Started

Clone the repository or download the file.

### Prerequisites

Python3 is required.
The script was developed and tested with Python 3.7

### Usage and Examples

Run the script with a python3 interpreter.
The Script needs authentication credentials as well as the URL or DNS Hostname of the XG Appliance.

````
usage: pyxg.py [-h] [-U USERNAME] [-P PASSWORD] [-u URL] [-p [PORT]]
               {get,set} ...

positional arguments:
  {get,set}
    get                 Get Information from API
    set                 Set Information to API

optional arguments:
  -h, --help            show this help message and exit
  -U USERNAME, --username USERNAME
                        API User Name
  -P PASSWORD, --password PASSWORD
                        API User Password
  -u URL, --url URL     Hostname or IP of your Sophos XG Appliance
  -p [PORT], --port [PORT]
                        Webadmin Port. Default: 4444
````

#### Examples

Search for a Hostname in DNS
```
python3 pyxg.py -U apiuser -P 'IAmASafeAPIPass1234' -u mysophosxg.tld.com get dns -H myserver01

Hostname:  myserver01.tld.com
IP Address:  10.0.0.10

```

Search for IP in DNS

```
python3 pyxg.py -U apiuser -P 'IAmASafeAPIPass1234' -u mysophosxg.tld.com get dns -I 10.0.0.10

Hostname:  myserver01.tld.com
IP Address:  10.0.0.10
```


## ToDo
* [ ] Implement Set DNS commands
* [ ] Redesign ArgumentParser implementation to be properly nested and only consider usable options
* [ ] Implement more Get and Set commands other than DNS

## Contributing

Feel free to fork this repository and submit PR's.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

