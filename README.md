## Cisco DevNet Learning Labs: Cisco DNA Center Sample Code

This repository contains the sample code to go along with [Cisco DevNet Learning Labs](https://developer.cisco.com/learning) covering network programmability topics.  During the setup steps of the labs, you'll be asked to clone this repository down to your workstation to get started.  

## About this Sample Code

Contributions are welcome, and we are glad to review changes through pull requests. See [contributing.md](contributing.md) for details.

Within this repository are several files and folders covering different topics and labs.  This table provides details on what each is used for, and which labs they correspond to.  

|  File / Folder  |  Description  | 
|  ---  |  ---  | 
|  [`env_lab.py`](env_lab.py)  |  A Python file containing lab infrastructure details for routers, switches and appliances leveraged in the different labs.  This file provides a centralized  Python `import` that is used in  other code samples to retrieve IPs, usernames, and passwords for connections  | 
|  [`env_user.template`](env_user.template)  |  Similar to `env_lab.py`, this is a template for end users to copy within their own code repo as `env_user.py` where they can provide unique details for their own accounts.  For example, their Webex Teams (formerly Cisco Spark) authentication token.  Not all labs require this file, if one does it will be specified in setup.  | 
|  [`requirements.txt`](requirements.txt)  |  Global Python requirements file containing the requirements for **all** labs within this repository.  Each folder also contains a local `requirements.txt` file.  | 
|  [`intro-python/`](intro-python/)  |  Sample code and exercises for the [Python Fundamentals Learning Labs](https://developer.cisco.com/learning/modules/programming-fundamentals/intro-python-part1/step/1) <br> | 
|  [`rest-api/`](rest-api/)  |  Sample code and exercises for the [REST API Fundamentals Learning Labs](https://developer.cisco.com/learning/modules/rest-api-fundamentals/hands-on-postman/step/1) <br>  | 
|  [`intro-dnac/`](intro-dnac/)  |  Sample code and exercises for the [Cisco DNA Center Learning Labs](https://developer.cisco.com/learning/modules/dnac-rest-apis/dnac-101-auth/step/1) <br>  | 
|  [`intro-mdp/`](intro-mdp/)  |  Sample code and exercises for the [Introduction to Model Drive Programmability (NETCONF/RESTCONF/YANG) Learning Labs](https://developer.cisco.com/learning/modules/intro-device-level-interfaces)  | 
|  [`intro-guestshell/`](intro-guestshell/)  |  Sample code and exercises for the [Introduction to Guest Shell on IOS XE Learning Labs](https://developer.cisco.com/learning/modules/net_app_hosting/intro-guestshell/step/1) <br> | 
|  [`intro-meraki/`](intro-meraki/)  |  Sample code and exercises for the [Introduction to Meraki Programmability Learning Labs](https://developer.cisco.com/learning/modules/getting-started-with-meraki/meraki-01-integrations/step/1) <br> | 
|  [`intro-nfvis/`](intro-nfvis/)  |  Sample code and exercises for the [Introduction to Network Function Virtualization with NFVIS APIs Learning Labs](https://developer.cisco.com/learning/devnet-express/dnav4-track/dnav3-intro-nfvis/dnav3-why-nfvis/step/1) <br> | 
|  [`verify/`](verify/)  |  A series of verification scripts primarily used during DevNet Express for DNA events to ensure the workshop environment is fully operational.  | 
|  [`dev/`](dev/)  |  Resources and information for building code samples and labs.  | 
|  [`requirements-dev.txt`](requirements-dev.txt)  |  Python requirements file containing requirements only needed if developing new code samples.  | 

> Note: These code samples are also leveraged during DevNet Express for DNA events.  If you are one of these events, your event proctors and hosts will walk you through event setup and verification steps as part of agenda.  

## Contributing

These learning modules are for public consumption, so you must ensure that you have the rights to any content that you contribute.

## Getting Involved

* If you'd like to contribute to an existing lab, refer to [contributing.md](contributing.md).
* If you're interested in creating a new Cisco DevNet Learning Lab, please contact a DevNet administrator for guidance.
