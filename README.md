# Log Analyzer
A command-line tool that takes a web server access log as input and produces a report based off three factors:
- HTTP errors (4xx/5xx), grouped and counted
- Abnormal traffic patterns (Web traffic spikes near 100% or drops to 0%)
- Overall entries (Total requests, unique IPs, top endpoints, error rate, time range covered)

## Prerequisites
Python 3.9+

Standard library only for the core version (re, statistics, collections, argparse, datetime) no pip installs required.

A sample log file in Apache/Nginx Combined Log Format (generator script included)
