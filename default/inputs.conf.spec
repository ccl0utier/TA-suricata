# Configure this input stanza to point to the Suricata EVE formatted logs on your IDS instance.
# Adapt the index as preferred, but ensure to keep the suricata default sourcetype, which is what controls the field extractions, etc.
#
# This should be deployed to a UF installed alongside the IDS on your instance.
[monitor:///var/log/suricata/suricata_iface_name/eve.json]
sourcetype = suricata
index = ids
disabled = 1


# Examples:

# Ingest pfSense Suricata eve.json logs - igb0 (WAN) interface.
# [monitor:///var/log/suricata/suricata_igb010777/eve.json]
# sourcetype = suricata
# index = ids

# Ingest pfSense Suricata eve.json logs - igb1 (LAN) interface.
# [monitor:///var/log/suricata/suricata_igb12036/eve.json]
# sourcetype = suricata
# index = ids
