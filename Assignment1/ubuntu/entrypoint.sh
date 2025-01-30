#!/bin/bash
sudo ntpd -gq &
exec ./ntp_data.sh