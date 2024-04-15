Gnu Radio Receiver README

In order to run the receiver, Gnu Radio Version 3.8.5 is required. In addition, the PlutoSDR drivers and requirements must be installed.

Follow this link for installation instructions for the PlutoSDR
https://wiki.analog.com/university/tools/pluto/drivers/linux

Follow this link for the Github Repository for Gnu Radio 3.8.5
https://github.com/gnuradio/gnuradio/releases/tag/v3.8.5.0

Follow this guide for installation instructions for building from source on gnu radio
https://wiki.gnuradio.org/index.php?title=LinuxInstall

Installation did not go smoothly. There were over 40+ hours spent troubleshooting to get the exact version of Gnu Radio required (3.8.5.0). This involved reading through documentation, trying different installation methods, manually installing various versions of specific libraries or dependencies that were not properly configured, altering the PATH, and a host of other problems. Hundreds of steps were taken and troubleshooted to get a working version of GR 3.8.5.0

Achieving software compatibility across all libraries for a deprecated version of Gnu Radio while building from source was one of the largest hangups of this assignment. In the future, explore using Docker and/or finding a way to create a working GR flowgraph that can use more up-to-date versions, like 3.9 or 3.10

To install the PlutoSDR source blocks in Gnu Radio, follow these links:
https://gist.github.com/cmcquinn/d9fdac957294ebbb470f238121bfc0f9
https://wiki.gnuradio.org/index.php/PlutoSDR_Source
