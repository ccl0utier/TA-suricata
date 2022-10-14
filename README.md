# Suricata Add-on for Splunk

## Overview

### About the Suricata Add-on for Splunk

|                       |                                                         |
|-----------------------|---------------------------------------------------------|
| Version               | 1.0.0                                                   |
| Vendor Products       | Suricata 5.0+                                           |
| Visible in Splunk Web | No.                                                     |

The **Suricata Add-on for Splunk** collects operational log data from the Suricata IDS. You can install the Add-on on a forwarder to send data from Suricata to a Splunk Enterprise indexer or group of indexers. You can also use the add-on to provide data for other apps, such as Splunk Enterprise Security.  Sending EVE formatted log data through SYSLOG is currently untested, but I plan to add support for it shortly.

The **Suricata Add-on for Splunk** collects the following data using file inputs:

- IDS Logs in [EVE](https://suricata.readthedocs.io/en/suricata-6.0.0/output/eve/index.html) format

### Source types for the Suricata Add-on for Splunk

The **Suricata Add-on for Splunk** provides index-time, search-time and CIM normalization for Suricata IDS, HTTO, DNS, SSL/TLS and other operational data in the following formats:

| Source Type        | Suricata Event Type | Description                       | CIM Data Models      |
|--------------------|---------------------|-----------------------------------|----------------------|
| suricata           | alert               | Suricata IDS Alerts               | Intrusion Detection  |
| suricata           | dns                 | Suricata DNS Events               | Network Resolution   |
| suricata           | http                | Suricata HTTP Events              | Web                  |
| suricata           | tls                 | Suricata SSL/TLS Events           | Certificates         |
| suricata           | flow                | Suricata Flow Events              | Network Traffic      |

### Compatibility

This version of the add-on is compatible with the following platform, OS and CIM versions:

|                                  |                           |
|----------------------------------|---------------------------|
| Splunk Platform                  | 8.x and later             |
| CIM                              | 4.2 and later             | 
| Supported OS for data collection | Any supported by Suricata |

## Installation

### Install the Suricata Add-on for Splunk

You can install the **Suricata Add-on for Splunk** with Splunk Web or from the command line. You can install the add-on onto any type of Splunk Enterprise instance (indexer, search head, or forwarder).

1. Download the add-on from [Github](https://github.com/ccl0utier/TA-suricata/releases) or alternatively clone the project using your `git` client.
2. Determine where and how to install this add-on in your deployment.
3. Perform any prerequisite steps before installing.
4. Complete your installation.

See Installing add-ons in Splunk Add-Ons for detailed instructions describing how to install a Splunk add-on in the following deployment scenarios:

- [Single-instance Splunk Enterprise](http://docs.splunk.com/Documentation/AddOns/released/Overview/Singleserverinstall)
- [Distributed Splunk Enterprise](http://docs.splunk.com/Documentation/AddOns/released/Overview/Distributedinstall)

### Distributed installation of this add-on

Use the tables below to determine where and how to install this add-on in a distributed deployment of Splunk Enterprise or any deployment for which you are using forwarders to get your data in. Depending on your environment, your preferences, and the requirements of the add-on, you may need to install the add-on in multiple places.

| Splunk instance type | Supported | Required    | Comments                                                                                          |
|----------------------|-----------|-------------|---------------------------------------------------------------------------------------------------|
| Search Heads         | Yes       | Yes         | Install this add-on to all search heads where Suricata knowledge management is required.           |
| Indexers             | Yes       | Yes         | Install this add-on to all indexers, it has index-time configurations.                            |
| Heavy Forwarders     | Yes       | Conditional | Required if you have Heavy Forwarders in your ingestion path or they perform data collection.     |
| Universal Forwarders | Yes       | Recommended | Install this add-on to the Universal Forwarders installed on your Suricata hosts to collect data.  |

### Distributed deployment compatibility

This table provides a quick reference for the compatibility of this add-on with Splunk distributed deployment features.

| Distributed deployment feature | Supported | Comments                                                         |
|--------------------------------|-----------|------------------------------------------------------------------|
| Search Head Clusters           | Yes       | N/A                                                              |
| Indexer Clusters               | Yes       | N/A                                                              |
| Deployment Server              | Yes       | Supported for deploying the configured add-on to multiple nodes. |


## Configuration

### Enable data inputs for the Suricata Add-on for Splunk

After you have installed the **Suricata Add-on for Splunk**, you must enable the data inputs within the add-on so that it collects data from your Suricata devices in your environment.
You must enable the inputs using the configuration files.

> Note: When you configure data and scripted inputs using configuration files, copy only the input stanzas whose configurations you want to change. Do not copy the entire file, as those changes persist even after an upgrade.

1. Create `inputs.conf` in the `$SPLUNK_HOME/etc/apps/TA-suricata/local` directory.
2. Open `$SPLUNK_HOME/etc/apps/TA-suricata/local/inputs.conf` for editing.
3. Open `$SPLUNK_HOME/etc/apps/TA-suricata/default/inputs.conf` for editing.
4. Copy the input stanza text that you want to enable from the `$SPLUNK_HOME/etc/apps/TA-suricata/default/inputs.conf.spec` file and paste them into the `$SPLUNK_HOME/etc/apps/TA-suricata/local/inputs.conf` file.
5. In the `$SPLUNK_HOME/etc/apps/TA-suricata/local/inputs.conf` file, enable the inputs that you want the add-on to monitor by setting the `disabled` attribute for each input stanza to `0` or alternatively removing it completely (the default is "enabled").
6. Save the `$SPLUNK_HOME/etc/apps/TA-suricata/local/inputs.conf` file.
7. Restart the Splunk enterprise instance.

The recommended approach is to deploy the **configured** add-on to the relevant nodes using a **Deployment Server**.  

### (Optional) Configure the Suricata Add-on for Splunk to send data to another index

You can (and likely should in most cases) send the collected data to a dedicated Splunk index.

This can be achieved by creating the relevant index on your indexers and then adding:

```
index = myindexofchoice
```

... to the relevant input configuration stanza.  So if you wanted to send your Suricata data to an index named `ids`, your configuration would look like this:

```
[monitor:///var/log/suricata/suricata_iface_name/eve.json]
sourcetype = suricata
index = ids
```
> Note: This works for all input stanzas, i.e. `monitor` inputs.

### Enable the TCP input for Vulnerability Scan Data

Use the provided input stanza to enable the TCP input on your indexers by deploying the **configured** stanza to your indexers.

Alternatively, configure the UDP input using Splunk Web on your indexers:

1. Log into Splunk Web on your indexer (or Heavy Forwarder) node.
2. Navigate to **Settings** > **Data inputs**.
3. Click **+ Add New** next to **UDP**.
4. Enter the desired UDP port in the "Port" field (suggested: `5514`).
5. Optionally, enter allowed Suricata hosts as the value for "Only accept connection from".
6. Click **Next**.
7. Set the **Source type** as `Suricata`.
8. Optionally, select your preferred index instead of `Default`.
9. Review and save your UDP Input configuration.

### Enable sending log data from Suricata.

In order for Suricata to send its logs to Splunk, perform the following:

For a plain Suricata installation:

1. Follow the [Suricata Documentation](https://suricata.readthedocs.io/en/suricata-6.0.0/index.html) to configure your installation to log locally in EVE format.
2. Find the path to your `eve.json` log file(s).
3. Adjust the add-on monitor inputs to point to the path of your `eve.json` files above.
4. Restart your Splunk forwarder.

If using Suricata on **pfSense**:

1. Log in to your **pfSense** instance using SSH and drop to a shell.
2. Go into the `/var/log/suricata/` folder and look for directories named `suricata_ifacename`, for example: `suricata_igb01234` and note them.  There should be one folder per interface setup to be monitored by Suricata in pfSense.  Confirm the folder(s) have an `eve.json` file.  See **Services** > **Suricata** in the pfSense Web interface for details.
3. Adjust the add-on monitor inputs to point to the path of your `eve.json` files above.
4. Restart your Splunk forwarder.

Now that you have a proper configuration to send results to Splunk, events should start being ingested into Splunk.

## Troubleshooting

### General troubleshooting

For troubleshooting tips that you can apply to all add-ons, see [Troubleshoot add-ons](http://docs.splunk.com/Documentation/AddOns/released/Overview/Troubleshootadd-ons) in Splunk Add-ons.

## Credits, References & Notes

This add-on was loosely based on the original Add-on published on Splunkbase [here](https://splunkbase.splunk.com/app/2760).

 "Suricata" is a trademark*SURICATA* is a trademark of Open Information Security Foundation Inc. and they are in no way affiliated with this work.  Any rights, title and interest in these trademarks remains solely with them.

> Author: Christian Cloutier <ccloutier@splunk.com>
