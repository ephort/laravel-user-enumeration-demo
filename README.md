# User enumeration through timeless timing attack in Laravel

This repository works as a demo to exploit the user enumeration vulnerability in Laravel.

The script is build on [Timeless Timing Attack](https://tom.vg/papers/timeless-timing-attack_usenix2020.pdf) by Tom Van Goethem et al.
The repository containing the proof of concept script h2time (which is part of this demo) can be found on https://github.com/DistriNet/timeless-timing-attacks 

## Pre-requisites

 - The site must have CSRF protection disabled. If it is enabled you have to obtain a valid CSRF token before trying to login.
 - You - as the attacker - must know one valid email and password combination on the target site.

## How to run

 - In `h2time.py` there is a built in login+logout for each 4 request pairs to the server to prevent the application from doing rate limiting.
This has to be amended to match a known user+password combination on the target site.
 - In `laravel.py` post_data must contain the email you want to test if exists on the target site.
 - In `laravel.py` post_data2 must contain an email you know exists on the target site. The password must be wrong, so that it does not login.

 - Run the script with the following command:

```bash
python3 laravel.py
```

The script will tell you which request from the request-pair that most of the times took longest to return.
If it "could not determine winner" that means they generally took the same time to return meaning the email under test exists on the server.

## Contributions

Tom Van Goethem et al (Timeless timing attacks)

[Jens Just Iversen](https://ephort.dk) (laravel user enumation)
