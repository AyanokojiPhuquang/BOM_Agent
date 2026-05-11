
## AOC-40-xM

## 40Gbps 850nm QSFP+ Active Optical Cable

## Features

- Four-channel full-duplex active optical cable
- Transmission data rate up to 11.3Gbps per channel
- High Reliability 850nm VCSEL technology
- Available in standard lengths of 3, 5, 10, 15, 20, 30, 50,100m
- Low power consumption &lt;1.5W
- Operating case temperature -5°C to +70°C
- 3.3V power supply voltage
- RoHS 6 compliant
- Hot Pluggable QSFP form factor

## Application

- Infiniband QDR/DDR/SDR
- 40G Ethernet
- Datacenter
- 4G/8G/10G Fiber Channel

## General Description

The QSFP+ active optic cables are a high performance, low power consumption, short range interconnect solution supporting InfiniBand QDR/DDR/SDR,12.5G/10G/8G/4G/2G fiber channel, PCIe and SAS. It is compliant with the QSFP MSA and IEEE P802.3ba. QSFP AOC is an assembly of 4 full-duplex lanes, where each lane is capable of transmitting data at rates up to 11.3Gb/s, providing an aggregated rate of 45.2Gb/s. QSFP+ AOC is one kind of parallel transceiver which provides increased port density and total system cost savings.

## Specification:

| Absolute Maximum Ratings    | Absolute Maximum Ratings   | Absolute Maximum Ratings   | Absolute Maximum Ratings   | Absolute Maximum Ratings   |
|-----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|
| Parameter                   | Symbol                     | Min                        | Max                        | Unit                       |
| Storage Ambient Temperature | T STG                      | -40                        | 85                         | ℃                          |
| Operating Case Temperature  | Tc                         | 0                          | 70                         | ℃                          |
| Operating Humidity          | H O                        | 5                          | 85                         | %                          |
| Power Supply Voltage        | Vcc                        | -0.3                       | +3.6                       | V                          |


| Input Voltage   | Vin   | -0.3   | Vcc+0.3   | V   |
|-----------------|-------|--------|-----------|-----|

| Recommended Operating Conditions   | Recommended Operating Conditions   | Recommended Operating Conditions   | Recommended Operating Conditions   | Recommended Operating Conditions   | Recommended Operating Conditions   |
|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|------------------------------------|
| Parameter                          | Symbol                             | Min                                | Typical                            | Max                                | Unit                               |
| Power Supply Voltage               | Vcc                                | 3.135                              | 3.3                                | 3.465                              | V                                  |
| Data Rate                          |                                    | 1                                  | 10.3                               | 11.3                               | Gbps                               |
| Data Speed Tolerance               | ∆DR                                | -100                               |                                    | +100                               | ppm                                |
| Link Distance with OM3 fiber       | D                                  | 0                                  |                                    | 100                                | m                                  |
| Power Consumption                  |                                    | -                                  |                                    | 1.5                                | W                                  |

| Electrical Specifications             | Electrical Specifications   | Electrical Specifications   | Electrical Specifications   | Electrical Specifications   | Electrical Specifications   | Electrical Specifications   |
|---------------------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|-----------------------------|
| Parameter                             | Symbol                      | Min                         | Typical                     | Max                         | Unit                        | Notes                       |
| Differential input impedance          | Zin                         | 90                          | 100                         | 110                         | ohm                         |                             |
| Differential Output impedance         | Zout                        | 90                          | 100                         | 110                         | ohm                         |                             |
| Differential input voltage amplitude  | ΔVin                        | 300                         |                             | 1100                        | mVp-p                       |                             |
| Differential output voltage amplitude | ΔVout                       | 400                         |                             | 800                         | mVp-p                       |                             |
| Bit Error Rate                        | BR                          |                             |                             | E-12                        |                             |                             |
| Input Logic Level High                | VIH                         | 2.0                         |                             | VCC                         | V                           |                             |
| Input Logic Level Low                 | VIL                         | 0                           |                             | 0.8                         | V                           |                             |
| Output Logic Level High               | VOH                         | VCC-0.5                     |                             | VCC                         | V                           |                             |
| Output Logic Level Low                | VOL                         | 0                           |                             | 0.4                         | V                           |                             |

## Pin Descriptions

|   Pin | Symbol   | Name/Description                     | Logic   |   Note |
|-------|----------|--------------------------------------|---------|--------|
|     1 | GND      | Ground                               |         |      1 |
|     2 | Tx2n     | Transmitter Inverted Data Input      | CML-I   |        |
|     3 | Tx2p     | Transmitter Non-Inverted Data output | CML-I   |        |
|     4 | GND      | Ground                               |         |      1 |
|     5 | Tx4n     | Transmitter Inverted Data Input      | CML-I   |        |
|     6 | Tx4p     | Transmitter Non-Inverted Data output | CML-I   |        |
|     7 | GND      | Ground                               |         |      1 |
|     8 | ModSelL  | Module Select                        | LVTLL-I |        |


|   9 | ResetL   | Module Reset                        | LVTLL-I    |    |
|-----|----------|-------------------------------------|------------|----|
|  10 | VccRx    | ﹢ 3.3V Power Supply Receiver       |            |  2 |
|  11 | SCL      | 2-Wire Serial Interface Clock       | LVCMOS-I/O |    |
|  12 | SDA      | 2-Wire Serial Interface Data        | LVCMOS-I/O |    |
|  13 | GND      | Ground                              |            |    |
|  14 | Rx3p     | Receiver Non-Inverted Data Output   | CML-O      |    |
|  15 | Rx3n     | Receiver Inverted Data Output       | CML-O      |    |
|  16 | GND      | Ground                              |            |  1 |
|  17 | Rx1p     | Receiver Non-Inverted Data Output   | CML-O      |    |
|  18 | Rx1n     | Receiver Inverted Data Output       | CML-O      |    |
|  19 | GND      | Ground                              |            |  1 |
|  20 | GND      | Ground                              |            |  1 |
|  21 | Rx2n     | Receiver Inverted Data Output       | CML-O      |    |
|  22 | Rx2p     | Receiver Non-Inverted Data Output   | CML-O      |    |
|  23 | GND      | Ground                              |            |  1 |
|  24 | Rx4n     | Receiver Inverted Data Output       | CML-O      |  1 |
|  25 | Rx4p     | Receiver Non-Inverted Data Output   | CML-O      |    |
|  26 | GND      | Ground                              |            |  1 |
|  27 | ModPrsL  | Module Present                      | LVTTL-O    |    |
|  28 | IntL     | Interrupt                           | LVTTL-O    |    |
|  29 | VccTx    | +3.3 V Power Supply transmitter     |            |  2 |
|  30 | Vcc1     | +3.3 V Power Supply                 |            |  2 |
|  31 | LPMode   | Low Power Mode                      | LVTTL-I    |    |
|  32 | GND      | Ground                              |            |  1 |
|  33 | Tx3p     | Transmitter Non-Inverted Data Input | CML-I      |    |
|  34 | Tx3n     | Transmitter Inverted Data Output    | CML-I      |    |
|  35 | GND      | Ground                              |            |  1 |
|  36 | Tx1p     | Transmitter Non-Inverted Data Input | CML-I      |    |
|  37 | Tx1n     | Transmitter Inverted Data Output    | CML-I      |    |
|  38 | GND      | Ground                              |            |  1 |

## Notes:

- 1) Module circuit ground is isolated from module chassis ground within the module. GND is the symbol for signal and supply (power) common for QSFP modules.


- 2) The connector pins are each rated for a maximum current of 500mA.

Top Side Viewedfrom Top

![Image](/AOC/AOC-40-xM/AOC-40-xM_artifacts/image_000004_c1d676bcb71933efe2d35d99c792cb225fc4a0398df3012283064c5718517f58.png)

## ModSelL Pin

The ModSelL is an input pin. When held low by the host, the module responds to 2-wire serial communication commands. The ModSelL allows the use of multiple QSFP modules on a single 2-wire interface  bus.  When  the  ModSelL  is  'High',  the  module  will  not  respond  to  any  2-wire  interface communication from the host. ModSelL has an internal pull-up in the module.

## ResetL Pin

Reset. LPMode\_Reset has an internal pull-up in the module. A low level on the ResetL pin for longer than the minimum pulse length (t\_Reset\_init) initiates a complete module reset, returning all user module settings to their default state. Module Reset Assert Time (t\_init) starts on the rising edge after the low level on the ResetL pin is released. During the execution of a reset (t\_init) the host shall disregard all status bits until the module indicates a completion of the reset interrupt. The module indicates this by posting  an  IntL  signal  with  the  Data\_Not\_Ready  bit  negated.  Note  that  on  power  up  (including  hot insertion) the module will post this completion of reset interrupt without requiring a reset.

## LPMode Pin

QSFP+ SR4operate in the low power mode (less than 1.5 W power consumption) This pin active high will decrease power consumption to less than 1W.

## ModPrsL Pin

ModPrsL is pulled up to Vcc on the host board and grounded in the module. The ModPrsL is asserted 'Low' when the module is inserted and deasserted 'High' when the module is physically absent from the host connector.

Bottom Side ViewedfromBottom

![Image](/AOC/AOC-40-xM/AOC-40-xM_artifacts/image_000005_34462c95f43a1ec834db7f18d98882161a8af1d2f5c3cc8148b7d03792abd6cb.png)

p


## ModuleTek

## IntL Pin

IntL is an output pin. When 'Low', it indicates a possible module operational fault or a status critical to the host system. The host identifies the source of the interrupt by using the 2-wire serial interface. The IntL pin is an open collector output and must be pulled up to Vcc on the host board.

## Power Supply Filtering

The host board should use the power supply filtering shown in Figure1.

Figure1. Host Board Power Supply Filtering

![Image](/AOC/AOC-40-xM/AOC-40-xM_artifacts/image_000007_1eb7e0fb2a353a0ba70a3550005d942eb249185385043cb9e11682ed5f55f8f3.png)

## Mechanical Specifications

Dimensions are in millimeters. All dimensions are ±0.1mm unless otherwise specified. (unit: mm)


ModuleTek

9868

![Image](/AOC/AOC-40-xM/AOC-40-xM_artifacts/image_000009_bc8abaa3e3b77c6f09e52cc274133aad7362be39abc6c737b7bcc42115d2bf37.png)

## ESD

This transceiver is specified as ESD threshold 1kV for Signal pads and 2kV for all others electrical input pads, tested per MIL-STD-883, Method 3015.4 /JESD22-A114-A (HBM). However, normal ESD precautions are still required during the handling of this module. This transceiver is shipped in ESD protective packaging. It should be removed from the packaging and handled only in an ESD protected environment.

## Order Information

| Part Number   | Product Description               |
|---------------|-----------------------------------|
| AOC-40-xM     | 40Gbps QSFP+ Active Optical Cable |

## Notes:

where "x" denotes cable length in meters. Examples are as follows:

x = 03 for 3m, x = 10 for 10m, x = 50 for 50m, x = A0 for 100m.