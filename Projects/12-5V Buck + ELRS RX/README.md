# 12V-5V 4A Buck Converter + ELRS Receiver
## Summary
The 12V-5V 4A Buck Converter + ELRS Board is intent for several foam fixed wing planes at the Waterloo Aerial Robotics Group. It includes a ESP32-C3 for PWM signalling and SX1281 for RF control over ELRS, as well as the requisite power electronics to have the system be powered by a single 12V input (1x 3S battery).

This implementation is designed to optimize and integrate the system of the foam fixed-wings, which currently requires a separate buck converter, and a commercial, off-the-shelf ELRS receiver. By implementing the two main features on a single 30.5x30.5mm board, we save on weight, size, and complexity of the foam plane’s overall system.

This board does not currently integrate an ESC for high-speed motor control.

## Resources
Confluence Information: https://uwarg-docs.atlassian.net/wiki/spaces/EL/pages/2702213129/12V+-+5V+4A+Buck+Converter+ELRS+Board

Altium 365: https://warg.365.altium.com/designs/CE23A3F1-03CB-4AA7-B2C5-656FA2B470E9#design