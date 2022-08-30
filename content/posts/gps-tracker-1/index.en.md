---
title: "Building a GPS tracker for fun and profit"
date: 2022-08-29
author: "John Stilia"
categories: ["Hardware", "PCB"]
tags: ["GPS", "Tracker", "Hardware", "PCB", "Arduino", "ARM", "Microcontrolers", "Microprocessors"]

resources:
  - name: featured-image
    src: tracker1.jpg
  - name: featured-image-preview
    src: tracker1.jpg

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

Building a GPS tracker because why not?

<!--more-->

# Why?

I wanted to build a GPS tracker with all other trackers' features without having to buy them separately.
I also wanted to make it Open source so anyone can build it and use it for their own purposes.

In the summer of 2020, I had my first motorbike stolen. A beautiful Yamaha MT07 was parked in my resident's underground car park.
The sadness of the situation was that I had no way of tracking it. I didn't know where it was or if it was still alive.
Then I had the idea of building a GPS tracker. I had no idea how to do it, but I had a few ideas.

So I decided to build a **GPS Tracker for Theft and Performance tracking**

# First steps

I started with some research. I wanted to know what was out there and what I could do to improve it.
I found a few trackers on the market, but they were all costly. I wanted to build something cheap and easy to use, with features only Elon Musk would have thought of.

## The Arduino family

I started with an Arduino Nano. I had a few of them lying around, and I knew I could get a GPS module.
The code worked out of the box. I got the GPS coordinates and sent them to a Serial port.
My next step was sending them to a server and visualising them.

- Pros

  - The code exists and works out of the box. It's easy to get started with.

- Cons
  - CPU is not the greatest. It's not very power efficient. It's not very fast. It's not very good at anything.

## The ESP family

The ESP32 is a great little board. It has WiFi, Bluetooth, and a lot of other features. I decided to use it for my project during prototyping and testing.
I got the GPS coordinates and sent them to a Serial port. I was also able to send them to a server. For that, I used [dweet.io](https://dweet.io/), which acts as a store of the last values sent to it. I could get the coordinates from the server and display them on a map.
For the visualisation, I used [freeboard.io](https://freeboard.io/). It is an excellent tool for visualising data. It is accessible as a trial and has a lot of features.

- Pros
  - It has WiFi and Bluetooth. It's easy to get started with.
- Cons
  - Limited number of GPIO for the sensors I want to connect to it.

## The ARM family

Following the most recent trends, I thought of exploring the ARM family of RP2040 or STM32. I had no experience with them, but I was willing to try them.
Each ARM processor had its own SDK, and I had to RTFM to use it in a Native way. I am more accustomed to using Arduino IDE, so I had to learn many new things.
Luckily there is an Arduino IDE Library that allows using of Arduino C++ on ARM.[https://github.com/earlephilhower/arduino-pico](https://github.com/earlephilhower/arduino-pico)

- Pros

  - Loads of ports fully customisable
  - Dual-core
  - Faster than the ESP8266

- Cons
  - No WiFi or Bluetooth ( not always )
  - Custom SDK and libraries

# Next steps

I decided to go with ARM RP240. It was a bit of a learning curve. I had to learn how to use the SDK and the Arduino IDE.
Currently, I am working on my code as I am testing all the different sensors I have on my board.

I will be working on writing code, and the next post will describe the hardware and how I will integrate it.

# References

- My own codebase
  - <https://github.com/stiliajohny/hardware-gps-tracker>
- <https://github.com/earlephilhower/arduino-pico>
