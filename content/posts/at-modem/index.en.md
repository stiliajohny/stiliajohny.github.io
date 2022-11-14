---
title: 'Playing with an GSM modem (SIM800L)'
date: 2022-11-11
author: 'John Stilia'
categories: []
tags: []

resources:
  - name: featured-image
    src: 'featured-image-preview.png'
  - name: featured-image-preview
    src: 'featured-image-preview.png'

draft: false
lightgallery: true
fontawesome: true
linkToMarkdown: true
rssFullText: false

toc:
  auto: false
comment:
  enable: true
---

<style>
img {
    box-shadow: inset 10px 10px 60px #fff;
    -moz-border-radius:25px;
    border-radius:10px;
}
</style>

Sunday Night playing with AT commands and a SIM800L GSM modem

<!--more-->

# Introduction

It has been a while that i bought a SIM800L GSM modem, but i never had the time to play with it. I was always busy with other projects, but this weekend i had some free time and i decided to play with it.
The most challenging part is to work with AT commands as ther eis a massive list to go thought. I found a great website that has a list of AT commands for the SIM800L modem. I will use this website as a reference for the AT commands that i will use in this post.

# Hardware

The hardware that i used for this project is the following:

- [SIM800L GSM modem](https://www.amazon.com/HiLetgo-Smallest-Breakout-Quad-band-3-7-4-2V/dp/B01DLIJM2E)
- [USB to Serial converter](https://www.amazon.com/JANSANE-PL2303TA-Serial-Console-Raspberry/dp/B07D9R5JFK)
- [Jumper wires](https://www.amazon.com/IZOKEE-Solderless-Breadboard-Arduino-Project/dp/B08151TQHG)

If the power to the SIM800L is enough, the on-board LED starts blinking. If it is blinking every second, this means it is searching for a network. You will know if it's connected to the network when it blinks every three seconds. If the LED blinks very fast, this means it's connected through GPRS.

# Software

Mostly I use CLI tools for this project. One of the following(whichever you might be more comfortable with):

- screen
- picocom
- minicom

# The Commands

## Basic AT check

Command: **AT**

```bash
AT
OK
```

## Check the modem

Command: **AT+CGREG?** / **AT+CEREG**<br>
Queries for the packet-switched network status. If the response is +CGREG: x, 5 or +CEREG: x,5 then you can jump ahead to step 5. The x in the x,5 part indicates the URC status and is not important for this step, the 5 indicates that the modem is registered to a network and is roaming. With Onomondo SIMs you will always be roaming which is why the response x,5 is always expected.

```bash
AT+CGREG?
+CGREG: 0,0

OK
```

## Check the firmware version

Command: **AT+CGMR**

```bash
AT+CGMR
Revision:1418B04SIM800L24

OK
```

## Check the signal strength

Command: **AT+CSQ**<br>
That return corresponds to a RSSI value of -93 dBm. This is only slightly better than marginal coverage. We should still be able to make a call on this signal condition, but the throughput may not be that good.

```bash
AT+CSQ
+CSQ: 20,0

OK
```

## Check the SIM card

Command: **AT+CPIN?**<br>

```bash
AT+CPIN?
+CPIN: READY

OK
```

## Check the network selection mode

Command: **AT+COPS?** <br>
Checks if the modem is in automatic selection mode. Some modems are set by default and don't need to be set manually. If the response is anything other than +COPS: 0, you will need to set it to choose network operator automatically using AT+COPS=0.

Beware of manually using AT+COPS=0 and AT+COPS=2, however.

```bash
AT+COPS?
+COPS: 0

OK
```

## Check the available networks

Command: **AT+COPS=?**<br>

```bash
AT+COPS=?
+COPS: (3,"T-Mobile","TMO UK","23430"),,(0-4),(0-2)

OK
```

## Make a phone call

Command: **ATD+447572785067;**<br>

```bash
ATD+447123456789;
OK
```

## Hang up the phone

Command: **AT**H<br>

```bash
ATH
OK
```

## Repeat the last call

Command: **ATDL**<br>

```bash
ATDL
OK
```

## Repeat the last command

Command: ATE1<br>
This command will repeat the last command that was sent to the modem. This is useful if you want to repeat a command without having to type it again.

```bash
ATE1
OK
```

## Receive a phone call

Command: **ATA**<br>

```bash
ATA
OK
```

## Send SMS

Command: **AT+CMGS="+447572785067"**<br>
The +CMGS command is used to send SMS messages. The +CMGS command is followed by the phone number of the recipient. The phone number must be enclosed in double quotes. The phone number must be in international format. The +CMGS command is terminated by a carriage return (CR) character. The modem will then respond with >. This indicates that the modem is ready to receive the SMS message. The SMS message must be terminated by a CTRL+Z character. The modem will then respond with +CMGS: <message reference>, <message length>. The message reference is a number that uniquely identifies the SMS message. The message length is the length of the SMS message in bytes.

```bash
AT+CMGS="+447123456789"
> This is a test message
+CMGS: 1, 20

OK
```

## Read the IMEI

Command: **AT+CGSN**

```bash
AT+CGSN
865691037901980
```

## Name of manufacturer

Command: **AT+CGMI**

```bash
AT+CGMI
SIMCOM_Ltd
```

## Model of the modem

Command: **AT+CGMM**

```bash
AT+CGMM
SIMCOM_SIM800L
```

## Read the battery voltage

Command: **AT+CBC**

```bash
AT+CBC
+CBC: 0,100,4200
```

# Resources/References

- <https://m2msupport.net/m2msupport/voice-call-at-commands-to-set-up-voice-call/>
- <https://www.smssolutions.net/tutorials/gsm/sendsmsat/>
- <https://m2msupport.net/m2msupport/voice-call-at-commands-to-set-up-voice-call/>
- <https://microchipsupport.force.com/s/article/Dial-phone-number-using-AT-command>
- <https://m2msupport.net/m2msupport/sim-at-commands-for-sim-presense-and-status/>
- <https://onomondo.com/help-center/testing-debugging/how-do-i-test-connectivity-with-at-commands/>
- <https://www.sparkfun.com/datasheets/Cellular%20Modules/AT_Commands_Reference_Guide_r0.pdf>