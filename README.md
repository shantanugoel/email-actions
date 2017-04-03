# Table Of Contents

- [email-actions](#email-actions)
- [Why did you make email-actions](#why-did-you-make-email-actions)
- [What are the benefits/differences compared to hosted services like IFTTT](#what-are-the-benefits-differences-compared-to-hosted-services-like-ifttt)
- [Current high level feature list](#current-high-level-feature-list)
- [Installation](#installation)
- [Usage](#usage)
  * [Config file format](#config-file-format)
  * [Rules](#rules)
  * [Plugin settings](#plugin-settings)
- [Contributing](#contributing)
  * [How to write a plugin](#how-to-write-a-plugin)
  
# email-actions
email-actions is a tiny SMTP server with a rules based engine to trigger any actions (notifications/commands etc) based on the emails sent to this server.
Think of it like [IFTTT](https://ifttt.com) but where input trigger is email and can be set up and run locally as well.

# Why did you make email-actions
Like most of my projects, email-actions is a 'scratch-your-own-itch' project. I bought a NAS (Synology ds216j) which also doubled as a downloader of anime/tv shows etc through RSS using its inbuilt "Download Station" app. I also used Plex to watch them over the network but these needed to be moved to a proper folder and named in a specific format (and some crap deleted and other maintenance done or sometimes some post processing done) to have Plex display/play them properly. I used Filebot and a few custom scripts for this but had to either do this manually or use a fixed time task scheduling (which tended to delay watching). This was semi-irritating. 
I also wanted to know when something had been downloaded so I could binge on that latest episode as soon as it was done :)
Download station had a hack (by changing internal files) to run custom script after a download was completed but it had to be redone after every firmware update and sometimes, after every restart. And finally it stopped working altogether with recent updates.

It did support email notifications though. Thus email-actions was born. So I could push notifications for downloaded items run my custom scripts on the downloaded items.

Since then, I've started using it for many other things as email is pervasive and most of the devices support email based notifications. So I can trap them and carry out other actions.

# What are the benefits/differences compared to hosted services like IFTTT
IFTTT provides email hooks as well. I *think* email-actions may be an alternative (you can decide whether it's better or not) with respect to below:
- IFTTT works as a client once email is received so you still need an available SMTP server to be able to send email. This can be expensive or risky as you'd have to share your server username/pwd to the email sending entity. email-actions is an SMTP server that takes actions before any actual email delivery.
- Can be run locally with minimal dependencies. You don't need to send your data to internet or even have an internet connection
- Tiny footprint
- Can run local commands as well while IFTTT still needs to be integrated with something else if that's what you need
- You are in control of your info
- Free(er), that is, no limitations on hooks/conditions etc

# Current high level feature list
- aiosmtpd based for aync email processing for performance
- The action execution is also asyncio based, so will free up the email sender while processing the action in background
- Easy yaml based configuration
- Global or local variables for full customization/reuse
- Action decision based on "To" email address filtering (Addition of many other filters on the roadmap)
- Plugins supported:
  - [Join](https://joaoapps.com/join/) push notifications (Will add pushbullet if there's a demand or can use custom external script for now)
  - Custom Local commands (Any arguments, any script type, custom environment variables)
  - Email (Can forward the email to custom upstream servers further if needed for more actions or actual email delivery)

# Installation

Pre-requisites: You need Python 3.4+ to be able to run this

- Install using pip (May need to use `pip3` instead of `pip` according to your OS/python installation. May need to use `sudo` prefix before below command if installing system wide)

`pip install email-actions` 

- Install directly

```
git clone git@github.com:shantanugoel/email-actions.git
cd email-actions
python setup.py install
```

# Usage

```
usage: email_actions [-h] [-v] [-H HOSTNAME] [-p PORT] [-l LOG] -c CONFIG

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Host IP or name to bind the server to
  -p PORT, --port PORT  Port number to bind the server to
  -l LOG, --log LOG     Set log level. 0=> Warning, 1=>Info, 2=>Debug

required arguments:
  -c CONFIG, --config CONFIG
                        Specify config file (yaml format) to be used. If it
                        doesn't exist, we'll try to create it

```

Examples:
```
email_actions -H 127.0.0.1 -p 8500 -l 2 -c /home/shantanu/email_actions_cfg.yml
```
```
email_actions -c /home/shantanu/email_actions_cfg.yml
```

Most of the options above are self explanatory. If you don't specify a hostname, it will choose `localhost` by default. If you don't specify a port, it'll choose `8025` by default. 

**Note** I recommend running the server on localhost or an internal network interface so that it can't be abused from internet. Right now it doesn't support authentication (limitation of aiosmtpd. Will be fixed soon), so if you must open it up to the internet, add your own scheme of verification either through a randomly generated email address in "To" rule or some other check in subject/content in your own external script that you are triggering.

Specifying a config file is mandatory. If the specified file doesn't exist, we'll generate a dummy one which you can fill. But essentially this is a step that you can't avoid. The config file is explained in more detail below.

## Config file format

email-actions uses the simple `yaml` format for its configuration. Learning this is a small task (few minutes at most for the basic usage that we need). You can look at [this page](https://learn.getgrav.org/advanced/yaml) for a quick reference.

email-actions works on the basis of user specified `filters`. Each filter can have `rules` specified which decide whether to run an action or not on the incoming email. Each filter also specifies `actions` (which is 1 or more plugins) to run an action on the incoming email if it passes the `rules`.

At least 1 filter is necessary in the configuration. Each filter must have at least 1 action. Rest all is optional. Each action plugin may have it's own mandatory OR optional settings. See [Plugin Settings](#plugin-settings) for all available plugins and their options/variables

The config file has the following general format. All text after `#` is an explanation, not a part of the config itself.

Names within `<>` can be substituted by user as per their choice. Names outside `<>` are reserved by email-actions and must be used as is.

All settings are case-sensitive. So take care of that.

```
global:  # Optional keyword that specifies global variables for plugins. These are available in all instances of your plugins in each filter
  <plugin_name>:  # Plugin name for which you are specifying a global variable
    <setting_1>: <abcd> # Variable/setting for this plugin.
    <setting_2>: <efgh> # Variable/setting for this plugin.

filters: #Mandatory keyword to signify start of your filters specifications.
  <filter_name>: # User specified name for a filter
    rules:       # Rules specifications start
      to: <email_id> # A rule that matches
```

Example: Take a look at the below sample config (Also found in [this location](https://github.com/shantanugoel/email-actions/blob/master/sample/config.yml)) 

```
# Specify a global variable for join plugin's api key
global:
  join:
    apikey: my_join_app_api_key

# Specify 2 filters.
# my_filter matches only the emails which are sent to abc@a.com and runs below 2 actions:
## Send join push notification using the global join api key
## Send an email using the credentials specified
# my_second_filter runs on all emails since there is no rule specified
# It runs below 2 actions:
## Send join notification using another_api_key. Local variable overrides the global one
## Run external command with given args and also sets up a environment variable called "MY_ENV_VAR" which can be accessed in external command

filters:
  my_filter:
    rules:
      to: abc@a.com
    actions:
      join:
      email:
        host: smtp.example.com
        username: my_email_username
        password: my_email_password
        port: 587
        secure: True
  my_second_filter:
      join:
        apikey: another_api_key
      exec:
        cmd: /home/shantanu/test.sh
        args:
          - /home/shantanu/abc_file
          - another_arg
        env:
          MY_ENV_VAR: 'Some Value'

```

## Rules
Currently, below rules are supported. These can be specified under a `rules` block.


| Rule Keyword | Value                                                                        |
|--------------|------------------------------------------------------------------------------|
| to           | Any email id which should exactly match the "To" field in the incoming email |

## Plugin Settings

### join

This plugin sends a push notification to your devices using the [Join](https://joaoapps.com/join/) app

Options:


| Option Keyword | Mandatory / Optional | Default Value | Comment                                                     |
|----------------|----------------------|---------------|-------------------------------------------------------------|
| apikey         | Mandatory            | None          | Your API key from [here](https://joinjoaomgcd.appspot.com/) |
| deviceId       | Optional             | group.all     | See valid options [here](https://joaoapps.com/join/api/)    |
| title          | Optional             | Email Subject | See valid options [here](https://joaoapps.com/join/api/)    |
| text           | Optional             | Email content | See valid options [here](https://joaoapps.com/join/api/)    |

### exec

This plugin allows to run any arbitrary command or script on your local system on which email-actions server is running.


| Option Keyword | Mandatory / Optional | Default Value    | Comment                                                                                          |
|----------------|----------------------|------------------|--------------------------------------------------------------------------------------------------|
| cmd            | Mandatory            | None             | Full path to the command to be run. Don't include arguments. Enclose in quotes if space in path  |
| args           | Optional             | Empty list       | List of arguments to be passed to command, 1 on each line.                                       |
| env            | Optional             | Empty dictionary | Key value pair of custom environment variables for the external command/script. One on each line |

### email

This plugin allows to forward the incoming email further to an upstream smtp server


| Option Keyword | Mandatory / Optional | Default Value | Comment                                                          |
|----------------|----------------------|---------------|------------------------------------------------------------------|
| host           | Mandatory            | None          | Provide hostname or ip of your upstream smtp server              |
| port           | Optional             | 25            | Port for upstream smtp server                                    |
| username       | Optional             | None          | username if required                                             |
| password       | Optional             | None          | Password if required                                             |
| secure         | Optional             | False         | Set it to true if upstream server requires secure/TLS connection |

# Contributing
Feel free to fork the repo and send PRs for any changes. If you can't make changes but want to report issues or provide feedback, open an Issue on github or ping me on twitter [@shantanugoel](https://twitter.com/shantanugoel)

You can contribute either to the core or write a plugin for your usecase. The only guiding principle is to keep it as simple/minimal as possible.

## How to write a plugin
Take a look at any plugin in [plugins](https://github.com/shantanugoel/email-actions/tree/master/email_actions/plugins) directory
A minimal plugin needs to do following things:
- Define 'PLUGIN_NAME'. This need not be same as the file name but is preferred to keep that way
- A function that takes these parameters: `filter_name, msg_from, msg_to, msg_subject, msg_content` and doesn't return anything
- Read plugin's configuration (if any) using email_actions.config.read_config_plugin function
  - Ideally the plugin should not need to use any other function from the core
- After writing the plugin, add the plugin's name and entry function in `entry_funcs` dict in [plugins init file](https://github.com/shantanugoel/email-actions/tree/master/email_actions/plugins/__init__.py)
