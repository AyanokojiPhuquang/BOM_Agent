
## DATA SHEET

Product Specification

## SFP-1G-10G-SR

## 1Gbps/10Gbps SFP+ SR Dual rate Transceiver, 300m MMF Reach 850nm

## Overview

ModuleTek's SFP-1G-10G-SR Dual-Rate SFP+ optical transceivers are based on 1G and 10G Ethernet standard, which are compliant with SFF-8431, 10GBASE-SR and 1000BASE-SX and provide a quick and reliable interface for the 1G and 10G Ethernet application. The digital diagnostics functions are available via the 2-wire serial bus, as specified in SFF-8431.

## Features

- ⚫ 10G Ethernet standard
- ⚫ Electrical interface compliant to SFF-8431
- ⚫ Lane bit rate 10.3 Gb/s and 1.25Gb/s
- ⚫ 850nm VCSEL laser and PIN photo-detector
- ⚫ I2C interface with integrated Digital Diagnostic monitoring
- ⚫ Single +3.3V power supply
- ⚫ Hot Pluggable
- ⚫ Maximum link length of 300m on OM3 MMF
- ⚫ Operating case temperature

Commercial: 0°C to +70 °C

Industrial: -40°C to +85 °C

- ⚫ RoHS compliant

## Application

- ⚫ 10 Gigabit Ethernet
- ⚫ 1 ⅹ InfiniBand QDR, DDR, SDR
- ⚫ High-performance computing clusters
- ⚫ 4G and 8G Fiber Channel Applications
- ⚫ Servers, switches, storage and host card adapters;

## Absolute Maximum Ratings

Table 2-Absolute Maximum Ratings

| Parameter                   | Symbol   |   Min. | Typical   |   Max. | Unit   | Notes           |
|-----------------------------|----------|--------|-----------|--------|--------|-----------------|
| Storage Temperature         | T S      |  -40   | -         |   85   | °C     |                 |
| Supply Voltage              | V CC     |   -0.3 | -         |    3.6 | V      |                 |
| Operating Relative Humidity | RH       |    0   | -         |   85   | %      | no condensation |

## Recommended Operating Conditions

Table 3-Recommended Operating Conditions

| Parameter                  | Symbol   |   Min. | Typical   |   Max. | Unit   | Notes       |
|----------------------------|----------|--------|-----------|--------|--------|-------------|
| Operating Case Temperature | T C      |   0    | -         |  70    | °C     | TLP850M10G  |
| Operating Case Temperature | T C      | -40    | -         |  85    | °C     | TLP850M10GI |
| Power Supply Voltage       | V CC     |   3.13 | 3.3       |   3.47 | V      |             |


| Power Supply Current      | I CC   | -   | -      | 250   | MA   |          |
|---------------------------|--------|-----|--------|-------|------|----------|
| Maximum Power Dissipation | P D    | -   | -      | 0.87  | W    |          |
| Data Rate                 | DR AVE | -   | 10.312 | -     | Gb/s |          |
| Transmission Distance     | TD     |     | -      | 300   | m    | Over MMF |

## Optical Characteristics

Table 4-Optical Characteristics

| Transmitter                        | Transmitter   | Transmitter   | Transmitter   | Transmitter   | Transmitter   | Transmitter   |
|------------------------------------|---------------|---------------|---------------|---------------|---------------|---------------|
| Parameter                          | Symbol        | Min.          | Typical       | Max.          | Unit          | Notes         |
| Center Wavelength                  | λ             | 840           | 850           | 860           | nm            |               |
| RMS spectral width                 |               |               |               | 0.65          | nm            |               |
| Average Optical Power              | Pavg          | -6.5          | -             | -1            | dBm           | 1             |
| Extinction Ratio                   | ER            | 3             | -             | -             | dB            | 2             |
| Transmitter and Dispersion Penalty | TDP           | -             | -             | 3.9           | dB            |               |
| Optical Return Loss Tolerance      | ORLT          | -             | -             | 20            | dB            |               |
| Relative Intensity Noise           | Rin           |               |               | -128          | dB/Hz         |               |
| Receiver                           | Receiver      | Receiver      | Receiver      | Receiver      | Receiver      | Receiver      |
| Center Wavelength                  | λr            | 840           | 850           | 860           | nm            |               |
| Receiver Sensitivity               | Psens         |               |               | -9.9          | dBm           | 3             |
| Stressed Sensitivity in OMA        |               |               |               | -7.5          | dBm           | 3             |
| Receiver Overload                  | P IN-OL       |               | -             | 2.4           | dBm           | 3             |
| Reflectance                        | Ref           | -             | -             | -12           | dB            |               |
| LOS Assert                         | LOS A         | -30           | -             | -             | dBm           |               |
| LOS De-assert                      | LOS D         | -             | -             | -12           | dBm           |               |
| LOS Hysteresis                     | LOS H         | 0.5           | -             | 6             | dB            |               |

## Notes:

1. The optical power is launched into MMF
2. Measured with a PRBS 2 31 -1 test pattern @10.3125Gbps
3. Measured with a PRBS 2 31 -1 test pattern @10.3125Gbps,BER≤10-12.

## Electrical Characteristics

Table 5-Electrical Characteristics

| Transmitter (Module Input)                   | Transmitter (Module Input)                   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   |
|----------------------------------------------|----------------------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Parameter                                    | Parameter                                    | Symbol                       | Min.                         | Typical                      | Max.                         | Unit                         | Notes                        |
| Differential Data Input Amplitude            | Differential Data Input Amplitude            | V IN,P-P                     | 200                          | -                            | 1600                         | mVpp                         |                              |
| Differential Termination Mismatch            | Differential Termination Mismatch            |                              | -                            | -                            | 10                           | %                            |                              |
| Tx_Disable                                   | Normal Operation                             | V IL                         | -0.3                         | -                            | 0.8                          | V                            |                              |
| Tx_Disable                                   | Laser Disable                                | V IH                         | 2.0                          | -                            | V CC +0.3                    | V                            |                              |
| Receiver (Module Output)                     | Receiver (Module Output)                     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     |
| Differential Data Output Amplitude           | Differential Data Output Amplitude           | V OUT,P-P                    | 370                          | -                            | 1600                         | mVpp                         |                              |
| Differential Termination Mismatch （ 1MHZ ） | Differential Termination Mismatch （ 1MHZ ） |                              | -                            | -                            | 10                           | %                            |                              |
| Output Rise/Fall Time, 20%~80%               | Output Rise/Fall Time, 20%~80%               | T R                          | 12                           | -                            | -                            | ps                           |                              |
| Rx_LOS                                       | Normal Operation                             | V OL                         | -                            | -                            | 0.4                          | V                            |                              |
| Rx_LOS                                       | Lose Signal                                  | V OH                         | V CC -0.5                    | -                            | -                            | V                            |                              |

## Digital Diagnostics

Table 6-Digital Diagnostics

| Parameter       | Range                | Accuracy   | Unit   | Calibration   |
|-----------------|----------------------|------------|--------|---------------|
| Temperature     | 0 to 70 or -40 to 85 | ±3         | ºC     | Internal      |
| Voltage         | 0 to V CC            | 0.1        | V      | Internal      |
| Tx Bias Current | 0 to 10              | 10%        | mA     | Internal      |
| Tx Output Power | -1 to -6.5           | ±3         | dBm    | Internal      |
| Rx Power        | -1 to -9.9           | ±3         | dBm    | Internal      |

## Pin Definitions

![Image](/SFP/SFP-1G-10G-SR/SFP-1G-10G-SR_artifacts/image_000002_e42a138b798b0c4c1289e162397d6632eeb8feeffda339afc8cb510525650862.png)

|   Pin | Name       | FUNCTION                     |   Plug Seq. | Notes                                                                                                            |
|-------|------------|------------------------------|-------------|------------------------------------------------------------------------------------------------------------------|
|     1 | VeeT       | Transmitter Ground           |           1 | Note 5                                                                                                           |
|     2 | TX Fault   | Transmitter Fault Indication |           3 | Note 1                                                                                                           |
|     3 | TX Disable | Transmitter Disable          |           3 | Note 2, Module disables on high or open                                                                          |
|     4 | SDA        | Module Definition 2          |           3 | 2-wire Serial Interface Data Line.                                                                               |
|     5 | SCL        | Module Definition 1          |           3 | 2-wire Serial Interface Clock.                                                                                   |
|     6 | MOD_ABS    | Module Definition 0          |           3 | Note 3                                                                                                           |
|     7 | RS0        | RX Rate Select (LVTTL).      |           3 | Rate Select 0, optionally controls SFP+ module receiver. This pin is pulled low to VeeT with a >30K resistor..   |
|     8 | LOS        | Loss of Signal               |           3 | Note 4                                                                                                           |
|     9 | RS1        | TX Rate Select (LVTTL).      |           1 | Rate Select 1, optionally controls SFP+ module transmitter. This pin is pulled low to VeeT with a >30K resistor. |
|    10 | VeeR       | Receiver Ground              |           1 | Note 5                                                                                                           |
|    11 | VeeR       | Receiver Ground              |           1 | Note 5                                                                                                           |
|    12 | RD-        | Inv. Received Data Out       |           3 | Note 6                                                                                                           |
|    13 | RD+        | Received Data Out            |           3 | Note 6                                                                                                           |
|    14 | VeeR       | Receiver Ground              |           1 | Note 5                                                                                                           |
|    15 | VccR       | Receiver Power               |           2 | 3.3 ± 5%, Note 7                                                                                                 |
|    16 | VccT       | Transmitter Power            |           2 | 3.3 ± 5%, Note 7                                                                                                 |
|    17 | VeeT       | Transmitter Ground           |           1 | Note 5                                                                                                           |

|   18 | TD+   | Transmit Data In      |   3 | Note 8   |
|------|-------|-----------------------|-----|----------|
|   19 | TD-   | Inv. Transmit Data In |   3 | Note 8   |
|   20 | VeeT  | Transmitter Ground    |   1 | Note 5   |

## Note:

1. TX Fault is an open collector/drain output, which should be pulled up with a 4.7K - 10KΩ resistoron the host board. Pull up voltage between 2.0V and VccT/R+0.3V. When high, output indicates a laser fault of some kind. Low indicates normal operation. In the low state, the output will be pulled to &lt; 0.8V.
2. TX disable is an input that is used to shut down the transmitter optical output. It is pulled up within the module with a 4.7K - 10 KΩ resistor. Its states are: Low (0 - 0.8V): Transmitter on (&gt;0.8, &lt; 2.0V): Undefined High (2.0 - 3.465V): Transmitter Disabled Open: Transmitter Disabled
3. Module Absent, connected to VeeT or VeeR in the module.
4. LOS (Loss of Signal) is an open collector/drain output, which should be pulled up with a 4.7K - 10KΩ resistor. Pull up voltage between 2.0V and VccT/ R+0.3V. When high, this output indicates the received optical power is below the worst-case receiver sensitivity (as defined by the standard in use). Low indicates normal operation. In the low state, the output will be pulled to &lt; 0.8V.
5. The module signal ground contacts, VeeR and VeeT, should be isolated from the module case.
6. RD-/+: These are the differential receiver outputs. They are AC coupled 100Ω differential lines which should be terminated with 100Ω (differential) at the user SERDES. The AC coupling is done inside the module and is thus not required on the host board. The voltage swing on these lines will be between 350 and 700 mV differential (175 -350 mV single ended) when properly terminated.
7. VccR and VccT are the receiver and transmitter power supplies. They are defined as 3.3V ±5% at the SFP+ connector pin. Maximum supply current is 725mA. Recommended host board power supply filtering is shown below. Inductors with DC resistance of less than 1 ohm should be used in order to maintain the required voltage at the SFP+ input pin with 3.3V supply voltage. When the recommended supply-filtering network is used, hot plugging of the SFP+ transceiver module will result in an inrush current of no more than 30mA greater than the steady state value. VccR and VccT may be internally connected within the SFP+ transceiver module.
8. TD-/+: These are the differential transmitter inputs. They are AC-coupled, differential lines with 100Ω differential termination inside the module. The AC coupling is done inside the module and is thus not required on the host board. The inputs will accept differential swings of 150 - 1200 mV (75 - 600mV single-ended).

## Recommended Host Board Power Supply Circuit

![Image](/SFP/SFP-1G-10G-SR/SFP-1G-10G-SR_artifacts/image_000003_10ec5de569dce256581e0e4c0b17321b13768c886df944a36c819f032ef47dc8.png)


## Recommended interface Circuit

![Image](/SFP/SFP-1G-10G-SR/SFP-1G-10G-SR_artifacts/image_000005_9bb4220967cb22620ff31980b70e3563a3940306e2494d816670d244dbbbe1fe.png)

## Mechanical Dimension

![Image](/SFP/SFP-1G-10G-SR/SFP-1G-10G-SR_artifacts/image_000006_e42da86a40215055642d16f8b0f523b4a9ea21c618051be5697c5a87d2274be8.png)

## Warnings

Handling  Precautions: This  device  is  susceptible  to  damage  as  a  result  of  electrostatic  discharge  (ESD).        A  static  free environment is highly recommended. Follow guidelines according to proper ESD procedures.

Laser  Safety: Radiation  emitted  by  laser  devices  can  be  dangerous  to  human  eyes.  Avoid  eye  exposure  to  direct  or  indirect radiation.