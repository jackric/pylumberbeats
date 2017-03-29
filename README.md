# Pylumberbeats

Pure Python implementation of the Lumberjack protocol, for pushing events (beats) to Logstash.
Also comes with a logging handler, to easily send logs using Python's built in logging module.

Based on the Lumberjack (v2) implementation in github.com/elastic/go-lumber

## TODO
- [ ] Batch events and send asynchronously
- [ ] Re-establish connection when unexpectedly dropped
- [ ] Resend un-acked events on reconnect
- [ ] Capture and send locals for exceptions
- [ ] Send abritrary metadata dict, defined at Handler creation