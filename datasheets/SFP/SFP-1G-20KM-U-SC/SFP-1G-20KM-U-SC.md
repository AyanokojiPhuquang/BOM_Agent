
## DATA SHEET

## Product Specification

## 1.25Gbps SFP Bi-Directional Transceiver, 20km Reach 1550nm TX / 1310 nm RX

## Features

- Dual data-rate of 1.25Gbps/1.063Gbps operation
- 1550nm DFB laser and PIN photodetector for 20km transmission
- Compliant with SFP MSA and SFF-8472 with simplex SC receptacle
- Digital Diagnostic Monitoring: Internal Calibration or External Calibration
- Compatible with SONET OC-24-LR-1
- Compatible with RoHS
- +3.3V single power supply
- Operating case temperature:

Standard :

0 to +70° C

Industry :

-45 to +85° C

## Applications

- Gigabit Ethernet
- Fiber Channel
- Switch to Switch interface
- Switched backplane applications
- Router/Server interface
- Other optical transmission systems

## Description

The SFP-BIDI transceivers are high performance, cost effective modules supporting dual data-rate of 1.25Gbps/1.0625Gbps and 20km transmission distance with SMF.

The transceiver consists of three sections: a DFB laser transmitter, a PIN photodiode integrated with a trans-impedance  preamplifier  (TIA)  and  MCU  control  unit.  All  modules  satisfy  class  I  laser  safety requirements.

The transceivers are compatible with SFP Multi-Source Agreement (MSA) and SFF-8472. For   further

UYS01L2B53S


UYS01L2B53S

information, please refer to SFP MSA.

![Image](/SFP/SFP-1G-20KM-U-SC/SFP-1G-20KM-U-SC_artifacts/image_000002_eafbf62089029c5f53772e1e97ab0dc3db417ff7475463bdff62167856cb9262.png)

## Absolute Maximum Ratings

Table 1 - Absolute Maximum Ratings

| Parameter           | Symbol   |   Min |   Max | Unit   |
|---------------------|----------|-------|-------|--------|
| Supply Voltage      | Vcc      |  -0.5 |   4.5 | V      |
| Storage Temperature | Ts       | -40   |  85   | ° C    |
| Operating Humidity  | -        |   5   |  85   | %      |

## Recommended Operating Conditions

Table 2 - Recommended Operating Conditions

| Parameter                  | Parameter                  | Parameter            | Symbol   |   Min |   Typical |    Max | Unit   |
|----------------------------|----------------------------|----------------------|----------|-------|-----------|--------|--------|
| Operating Case Temperature | Operating Case Temperature | Standard             | Tc       |  0    |           |  70    | ° C    |
| Power Supply Voltage       | Power Supply Voltage       | Power Supply Voltage | Vcc      |  3.13 |     3.3   |   3.47 | V      |
| Power Supply Current       | Power Supply Current       | Power Supply Current | Icc      |       |           | 300    | mA     |
| Data Rate                  | Gigabit Ethernet           | Gigabit Ethernet     |          |       |     1.25  |        | Gbps   |
| Data Rate                  | Fiber Channel              | Fiber Channel        |          |       |     1.063 |        | Gbps   |


UYS01L2B53S

## Optical and Electrical Characteristics

UYS01L2B53:

(DFB and PIN, 20km Reach)

Table 3 - Optical and Electrical Characteristics

| Parameter                        | Parameter                        | Symbol      | Min         | Typical     | Max         | Unit        | Notes       |
|----------------------------------|----------------------------------|-------------|-------------|-------------|-------------|-------------|-------------|
| Transmitter                      | Transmitter                      | Transmitter | Transmitter | Transmitter | Transmitter | Transmitter | Transmitter |
| Centre Wavelength                | Centre Wavelength                | λc          | 1530        | 1550        | 1570        | nm          |             |
| Spectral Width (-20dB)           | Spectral Width (-20dB)           | ∆λ          |             |             | 1           | nm          |             |
| Side Mode Suppression Ratio      | Side Mode Suppression Ratio      | SMSR        | 30          |             |             | dB          |             |
| Average Output Power             | Average Output Power             | Pout        | -9          |             | 0           | dBm         | 1           |
| Extinction Ratio                 | Extinction Ratio                 | ER          | 9           |             |             | dB          |             |
| Optical Rise/Fall Time (20%~80%) | Optical Rise/Fall Time (20%~80%) | tr/tf       |             |             | 0.26        | ns          |             |
| Data Input Swing Differential    | Data Input Swing Differential    | V IN        | 400         |             | 1800        | mV          | 2           |
| Input Differential Impedance     | Input Differential Impedance     | Z IN        | 90          | 100         | 110         | Ω           |             |
| TX Disable                       | Disable                          |             | 2.0         |             | Vcc         | V           |             |
| TX Disable                       | Enable                           |             | 0           |             | 0.8         | V           |             |
| TX Fault                         | Fault                            |             | 2.0         |             | Vcc         | V           |             |
| TX Fault                         | Normal                           |             | 0           |             | 0.8         | V           |             |
| Receiver                         | Receiver                         | Receiver    | Receiver    | Receiver    | Receiver    | Receiver    | Receiver    |
| Centre Wavelength                | Centre Wavelength                | λc          | 1260        |             | 1360        | nm          |             |
| Receiver Sensitivity             | Receiver Sensitivity             |             |             |             | -23         | dBm         | 3           |
| Receiver Overload                | Receiver Overload                |             | -3          |             |             | dBm         | 3           |
| LOS De-Assert                    | LOS De-Assert                    | LOS D       |             |             | -24         | dBm         |             |
| LOS Assert                       | LOS Assert                       | LOS A       | -30         |             |             | dBm         |             |
| LOS Hysteresis                   | LOS Hysteresis                   |             | 1           |             | 4           | dB          |             |
| Data Output Swing Differential   | Data Output Swing Differential   | Vout        | 400         |             | 1800        | mV          | 4           |
|                                  |                                  | High        | 2.0         |             | Vcc         | V           |             |
|                                  |                                  | Low         |             |             | 0.8         | V           |             |

## Notes:

1. The optical power is launched into SMF.

2. PECL input, internally AC-coupled and terminated.

3. Measured with a PRBS 2 7 -1 test pattern @1250Mbps, BER ≤1×10 -12 .

4. Internally AC-coupled.

UYS01L2B53S

## Timing and Electrical

## Table 4 - Timing and Electrical

| Parameter                                       | Symbol         |   Min | Typical   | Max   | Unit   |
|-------------------------------------------------|----------------|-------|-----------|-------|--------|
| Tx Disable Negate Time                          | t_on           |       |           | 1     | ms     |
| Tx Disable Assert Time                          | t_off          |       |           | 10    | µs     |
| Time To Initialize, including Reset of Tx Fault | t_init         |       |           | 300   | ms     |
| Tx Fault Assert Time                            | t_fault        |       |           | 100   | µs     |
| Tx Disable To Reset                             | t_reset        |    10 |           |       | µs     |
| LOS Assert Time                                 | t_loss_on      |       |           | 100   | µs     |
| LOS De-assert Time                              | t_loss_off     |       |           | 100   | µs     |
| Serial ID Clock Rate                            | f_serial_clock |       |           | 400   | KHz    |
| MOD_DEF (0:2)-High                              | V H            |     2 |           | Vcc   | V      |
| MOD_DEF (0:2)-Low                               | V L            |       |           | 0.8   | V      |

## Diagnostics

## Table 5 -Diagnostics Specification

| Parameter    | Range      | Unit   | Accuracy   | Calibration         |
|--------------|------------|--------|------------|---------------------|
| Temperature  | 0 to +70   | ° C    | ±3° C      | Internal / External |
| Voltage      | 3.0 to 3.6 | V      | ±3%        | Internal / External |
| Bias Current | 0 to 100   | mA     | ±10%       | Internal / External |
| TX Power     | -9 to 0    | dBm    | ±3dB       | Internal / External |
| RX Power     | -23 to -3  | dBm    | ±3dB       | Internal / External |

## Digital Diagnostic Memory Map

The transceivers provide serial ID memory contents and diagnostic information about the present operating conditions by the 2-wire serial interface (SCL, SDA).

The diagnostic information with internal calibration or external calibration all are implemented, including received power monitoring, transmitted power monitoring, bias current monitoring, supply voltage monitoring and temperature monitoring.

The digital diagnostic memory map specific data field defines as following.

2 wire address 1010000x (A0h)

![Image](/SFP/SFP-1G-20KM-U-SC/SFP-1G-20KM-U-SC_artifacts/image_000004_10688e7af0db5d603e7fe7f6075358e6dfb50f66c768fde63f0e679856f3ec15.png)

2 wire address 1010001X (A2h)

![Image](/SFP/SFP-1G-20KM-U-SC/SFP-1G-20KM-U-SC_artifacts/image_000005_b6d18171a8b07d0ade96231b0c21b7aeb5c85a7cfeef5f9dd83f961799843479.png)

| 0       | Alarm and Warning Thresholds (56 bytes)              |
|---------|------------------------------------------------------|
| 55      |                                                      |
| 95      | (40 bytes) Real Time Diagnostic Interface (24 bytes) |
| 119     | Vendor Specific (8 bytes)                            |
| 127     | User Writable EEPROM (120 bytes)                     |
| 247 255 | Vendor Specific (8 bytes)                            |

## Pin Definitions

Pin Diagram

![Image](/SFP/SFP-1G-20KM-U-SC/SFP-1G-20KM-U-SC_artifacts/image_000006_da312c910213bad20f43dc6340d5b8bb3c1b83e69efe84bd12c8517ab25f0dc1.png)

UYS01L2B53S


## Pin Descriptions

UYS01L2B53S

|   Pin | Signal Name   | Description                  |   Plug Seq. | Notes   |
|-------|---------------|------------------------------|-------------|---------|
|     1 | V EET         | Transmitter Ground           |           1 |         |
|     2 | TX FAULT      | Transmitter Fault Indication |           3 | Note 1  |
|     3 | TX DISABLE    | Transmitter Disable          |           3 | Note 2  |
|     4 | MOD_DEF(2)    | SDA Serial Data Signal       |           3 | Note 3  |
|     5 | MOD_DEF(1)    | SCL Serial Clock Signal      |           3 | Note 3  |
|     6 | MOD_DEF(0)    | TTL Low                      |           3 | Note 3  |
|     7 | Rate Select   | Not Connected                |           3 |         |
|     8 | LOS           | Loss of Signal               |           3 | Note 4  |
|     9 | V EER         | Receiver ground              |           1 |         |
|    10 | V EER         | Receiver ground              |           1 |         |
|    11 | V EER         | Receiver ground              |           1 |         |
|    12 | RD-           | Inv. Received Data Out       |           3 | Note 5  |
|    13 | RD+           | Received Data Out            |           3 | Note 5  |
|    14 | V EER         | Receiver ground              |           1 |         |
|    15 | V CCR         | Receiver Power Supply        |           2 |         |
|    16 | V CCT         | Transmitter Power Supply     |           2 |         |
|    17 | V EET         | Transmitter Ground           |           1 |         |
|    18 | TD+           | Transmit Data In             |           3 | Note 6  |
|    19 | TD-           | Inv. Transmit Data In        |           3 | Note 6  |
|    20 | V EET         | Transmitter Ground           |           1 |         |

## Notes:

Plug Seq.: Pin engagement sequence during hot plugging.

- 1) TX Fault is an open collector output, which should be pulled up with a 4.7k~10kΩ resistor on the host board to a voltage between 2.0V and Vcc+0.3V. Logic 0 indicates normal operation; Logic 1 indicates a laser fault of some kind. In the low state, the output will be pulled to less than 0.8V.
- 2)  TX  Disable is an input that is used to shut down the transmitter optical output. It is pulled up within the module with a 4.7k~10kΩ resistor. Its states are:
- 3) Mod-Def 0,1,2. These are the module definition pins. They should be pulled up with a 4.7k~10kΩ resistor on the host board. The pull-up voltage shall be VccT or VccR.

Low (0 to 0.8V):

Transmitter on

(&gt;0.8V, &lt; 2.0V):

Undefined

High (2.0 to 3.465V):

Transmitter Disabled

Open:

Transmitter Disabled

Mod-Def 0 is grounded by the module to indicate that the module is present

Mod-Def 1 is the clock line of two wire serial interface for serial ID

Mod-Def 2 is the data line of two wire serial interface for serial ID

- 4) LOS is an open collector output, which s hould be pulled up with a 4.7k~10kΩ resistor. Pull up voltage between 2.0V and Vcc+0.3V. Logic 1 indicates loss of signal; Logic 0 indicates normal operation. In the low state, the output will be pulled to less than 0.8V.
- 5)  RD-/+: These are the differential receiver outputs. They are internally AC-coupled 100 differential lines which should be terminated with 100Ω (differential) at the user SERDES.
- 6) TD-/+: These are the differential transmitter inputs. They are internally AC-coupled, differential lines with 100Ω differential termination inside the module.


UYS01L2B53S

## Recommended Interface Circuit

![Image](/SFP/SFP-1G-20KM-U-SC/SFP-1G-20KM-U-SC_artifacts/image_000009_d79ce0e0b6d55819373fe49ee753c3664c2d5859eb482b7dd4e0d59192f0f5cb.png)