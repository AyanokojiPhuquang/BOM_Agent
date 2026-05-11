
## DATA SHEET

## MODULETEK: QSFP-100G-LR

100G QSFP28 LR Optical Transceiver

## QSFP-100G-LR Overview

ModuleTek's QSFP-100G-LR QSFP28 LR optical transceivers are based on 100G Ethernet IEEE 802.3bm standard. QSFP28 LR offers 4 independent transmit and receive channels, each capable of 25G for an aggregate bandwidth of 100G.

## Product Features

- Supports 100GBASE-LR/100GE/OTU4
- Lane bit rate 103.125~111.8Gb/s with PAM4
- Up to 10km transmission on SMF
- 1310nm laser and PIN receiver
- 4x25.78Gb/s with NRZ electrical interface (CAUI-4)
- I2C interface with integrated Digital Diagnostic monitoring
- QSFP28 MSA package with LC duplex connector
- Single +3.3V power supply
- Maximum power consumption 4.5 W
- Operating case temperature: 0 to +70 °C;
- Compliant to 802.3cu, SFF-8636&amp;SFF-8679 standard
- Compliant to 100G Lambda MSA
- Complies with EU Directive 2015/863/EU

## Application

- 100GBASE-LR;
- 100G Ethernet;
- Data center / Cloud application.

## Order Information

Table 1- order information

| Part No.      | Data Rate   | Laser   | Fiber Type   | Distance   | Optical Interface   | Temp   | DDMI   |
|---------------|-------------|---------|--------------|------------|---------------------|--------|--------|
| QSFP-100G- LR | 100Gbps     | 1310nm  | SMF          | 10km       | SMF                 | 0~70C  | Y      |

## Absolute Maximum Ratings

Table 2-Absolute Maximum Ratings

| Parameter           | Symbol   |   Min. | Typical   |   Max. | Unit   | Notes   |
|---------------------|----------|--------|-----------|--------|--------|---------|
| Storage Temperature | T S      |    -40 | -         |    +85 | °C     |         |

| Supply Voltage              | V CC   | -0.5   | -   |   +4.0 | QSFP-100G-LR V   | Specifications   |
|-----------------------------|--------|--------|-----|--------|------------------|------------------|
| Operating Relative Humidity | RH     | -      | -   |    +85 | %                |                  |

## Recommended Operating Conditions

Table 3-Recommended Operating Conditions

| Parameter                  | Symbol   | Min.    | Typical   |   Max. | Unit   | Notes     |
|----------------------------|----------|---------|-----------|--------|--------|-----------|
| Operating Case Temperature | T C      | 0       | -         |  70    | °C     |           |
| Power Supply Voltage       | V CC     | 3.13    | 3.3       |   3.47 | V      |           |
| Power Supply Current       | I CC     | -       | -         |   1.29 | A      |           |
| Maximum Power Dissipation  | P D      | -       | -         |   4.5  | W      |           |
| Lane Bit Rate              | BR LANE  | 103.125 | 106.25    | 111.8  | Gb/s   | With PAM4 |
| Transmission Distance      | TD       | -       | -         |  10    | km     | Over SMF  |


## Optical Characteristics

Table 4-Optical Characteristics

| Transmitter                                             | Transmitter   | Transmitter                                     | Transmitter                                     | Transmitter                                     | Transmitter   | Transmitter   |
|---------------------------------------------------------|---------------|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|---------------|---------------|
| Parameter                                               | Symbol        | Min.                                            | Typical                                         | Max.                                            | Unit          | Notes         |
| Center Wavelength                                       | λ             | 1304.5                                          | 1311                                            | 1317.5                                          | nm            |               |
| Average Launch Power                                    | P TX_LANE     | -1.4                                            | -                                               | 4.5                                             | dBm           | 1             |
| OMA outer                                               | OMA           | 0.7                                             | -                                               | 4.7                                             | dBm           |               |
| Launch power in OMA outer minus TDECQ                   | OMA- TDECQ    | -0.7                                            | -                                               | -                                               | dB            | ER ≧ 4.5 dB   |
|                                                         | OMA- TDECQ    | -0.6                                            | -                                               | -                                               | dB            | ER<4.5dB      |
| Transmitter and dispersion eye closure for PAM4 (TDECQ) | TDECQ         | -                                               | -                                               | 3.5                                             | dB            |               |
| Average Output Power (Laser Turn off)                   | P OUT-OFF     | -                                               | -                                               | -15                                             | dBm           |               |
| Side Mode Suppression Ratio                             | SMSR          | 30                                              | -                                               | -                                               | dB            |               |
| Extinction Ratio                                        | ER            | 3.5                                             | -                                               | -                                               | dB            |               |
| Receiver                                                | Receiver      | Receiver                                        | Receiver                                        | Receiver                                        | Receiver      | Receiver      |
| Parameter                                               | Symbol        | Min.                                            | Typical                                         | Max.                                            | Unit          | Notes         |
| Center Wavelength                                       | λ             | 1304.5                                          | 1311                                            | 1317.5                                          | nm            |               |
| Damage threshold                                        | Pdamage       | 5.5                                             | -                                               | -                                               |               | 2             |
| Average Rx Power                                        | P RX _LANE    | -7.7                                            | -                                               | 4.5                                             | dBm           | 3             |
| Receiver power (OMA outer )                             | P OMA_LANE    | -                                               | -                                               | 4.7                                             | dBm           |               |
| Receiver sensitivity (OMA outer )                       | SEN OMA       | 100G-FR and 100G-LR Technical Spec Equation (1) | 100G-FR and 100G-LR Technical Spec Equation (1) | 100G-FR and 100G-LR Technical Spec Equation (1) | dBm           | 4             |
| Stressed receiver sensitivity (OMA outer )              | SRS OMA       | -                                               | -                                               | -4.1                                            | dBm           | 5             |

## Notes:

1. The optical power is launched into SMF.
2. The receiver shall be able to tolerate, without damage, continuous exposure to an optical input signal having this average power level. The receiver does not have to operate correctly at this input power.
3. Average receive power, each lane (min) is informative and not the principal indicator of signal strength.
4. Receiver sensitivity (OMAouter),each lane (max) is informative and is defined for a transmitter with SECQ up to 3.4 dB
5. Measured with conformance test signal at  TP3  using  the  test pattern  PRBS31Q or  scrambled idle for stressed receiver sensitivity for the BER= 2.4x10-4.

Illustration of receiver sensitivity mask for 100G-FR and LR with SECQ up to 3.4 dB

![Image](/QSFP/QSFP-100G-LR/QSFP-100G-LR_artifacts/image_000002_2311d9ef39bf174afbe214eb0450e2c3400d2a19ccfe51ed68635ef10bf645ed.png)


## ModuleTek

## Digital Diagnostics

## Table 5-Digital Diagnostics

| Parameter       | Range       | Accuracy   | Unit   | Calibration   |
|-----------------|-------------|------------|--------|---------------|
| Temperature     | 0 to 70     | ±3         | ºC     | Internal      |
| Voltage         | 0 to V CC   | 0.1        | V      | Internal      |
| Tx Bias Current | 0 to 100    | 10%        | mA     | Internal      |
| Tx Output Power | -1.4 to 4.5 | ±3         | dBm    | Internal      |
| Rx Input Power  | -7.7 to 4.5 | ±3         | dBm    | Internal      |

## Electrical Characteristics

High-Speed Signal:

Compliant to CAUI-4 (IEEE 802.3bm)

Low-Speed Signal:

Compliant to SFF-8679.

Table 6-Electrical Characteristics

| Transmitter (Module Input)                   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   | Transmitter (Module Input)   |
|----------------------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|------------------------------|
| Parameter                                    | Symbol                       | Min.                         | Typical                      | Max.                         | Unit                         | Notes                        |
| Differential Data Input Amplitude            | V IN,P-P                     | 85                           | -                            | 900                          | mVpp                         |                              |
| Differential Termination Mismatch            |                              | -                            | -                            | 10                           | %                            |                              |
| LPMode, Reset and ModSelL, V in low          | V IL                         | -0.3                         | -                            | 0.8                          | V                            |                              |
| LPMode, Reset and ModSelL, V in high         | V IH                         | 2.0                          | -                            | V CC +0.3                    | V                            |                              |
| Receiver (Module Output)                     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     | Receiver (Module Output)     |
| Differential Data Output Amplitude           | V OUT,P-P                    | 200                          | -                            | 900                          | mVpp                         |                              |
| Differential Termination Mismatch （ 1MHZ ） |                              | -                            | -                            | 10                           | %                            |                              |
| Transition time, 20% to 80%                  | Tr Tf                        | 12                           |                              |                              | ps                           |                              |
| ModPrsL and IntL, V out low                  | V OL                         | 0                            | -                            | 0.4                          | V                            |                              |
| ModPrsL and IntL, V out high                 | V OH                         | V CC -0.5                    | -                            | V CC+ 0.3                    | V                            |                              |

## Pin Definitions

Top Side Viewed From Top

![Image](/QSFP/QSFP-100G-LR/QSFP-100G-LR_artifacts/image_000004_ee325b49a4ff6a3afd6d15165ccfb74b711144190a8e0e3d77cfa5c1b2a75334.png)

Moc odule e M E e

Bottom Side Viewed From Bottom

![Image](/QSFP/QSFP-100G-LR/QSFP-100G-LR_artifacts/image_000005_512d38e832afbc66538fc923ea26237a3ba94c33d43df29247fb4f7ccf09dc66.png)


|   PIN | Logic      | Symbol       | Description                          |   Plug Seq. |   Notes |
|-------|------------|--------------|--------------------------------------|-------------|---------|
|     1 |            | GND          | Ground                               |           1 |       1 |
|     2 | CML-I      | Tx2n         | Transmitter Inverted Data Input      |           3 |         |
|     3 | CML-I      | Tx2p         | Transmitter Non-Inverted Data output |           3 |         |
|     4 |            | GND          | Ground                               |           1 |       1 |
|     5 | CML-I      | Tx4n         | Transmitter Inverted Data Input      |           3 |         |
|     6 | CML-I      | Tx4p         | Transmitter Non-Inverted Data output |           3 |         |
|     7 |            | GND          | Ground                               |           1 |       1 |
|     8 | LVTLL-I    | ModSelL      | Module Select                        |           3 |         |
|     9 | LVTLL-I    | ResetL       | Module Reset                         |           3 |         |
|    10 |            | VccRx        | ﹢ 3.3V Power Supply Receiver        |           2 |       2 |
|    11 | LVCMOS-I/O | SCL          | 2-Wire Serial Interface Clock        |           3 |         |
|    12 | LVCMOS-I/O | SDA          | 2-Wire Serial Interface Data         |           3 |         |
|    13 |            | GND          | Ground                               |           1 |         |
|    14 | CML-O      | Rx3p         | Receiver Non-Inverted Data Output    |           3 |         |
|    15 | CML-O      | Rx3n         | Receiver Inverted Data Output        |           3 |         |
|    16 |            | GND          | Ground                               |           1 |       1 |
|    17 | CML-O      | Rx1p         | Receiver Non-Inverted Data Output    |           3 |         |
|    18 | CML-O      | Rx1n         | Receiver Inverted Data Output        |           3 |         |
|    19 |            | GND          | Ground                               |           1 |       1 |
|    20 |            | GND          | Ground                               |           1 |       1 |
|    21 | CML-O      | Rx2n         | Receiver Inverted Data Output        |           3 |         |
|    22 | CML-O      | Rx2p         | Receiver Non-Inverted Data Output    |           3 |         |
|    23 |            | GND          | Ground                               |           1 |       1 |
|    24 | CML-O      | Rx4n         | Receiver Inverted Data Output        |           3 |         |
|    25 | CML-O      | Rx4p         | Receiver Non-Inverted Data Output    |           3 |         |
|    26 |            | GND          | Ground                               |           1 |       1 |
|    27 | LVTTL-O    | ModPrsL      | Module Present                       |           3 |         |
|    28 | LVTTL-O    | IntL/Rx_LOS  | Interrupt/Rx_LOS                     |           3 |         |
|    29 |            | VccTx        | +3.3 V Power Supply transmitter      |           2 |       2 |
|    30 |            | Vcc1         | +3.3 V Power Supply                  |           2 |       2 |
|    31 | LVTTL-I    | LPMode/TxDIS | Low Power Mode/Tx_Disable            |           3 |         |
|    32 |            | GND          | Ground                               |           1 |       1 |
|    33 | CML-I      | Tx3p         | Transmitter Non-Inverted Data Input  |           3 |         |
|    34 | CML-I      | Tx3n         | Transmitter Inverted Data Output     |           3 |         |
|    35 |            | GND          | Ground                               |           1 |       1 |
|    36 | CML-I      | Tx1p         | Transmitter Non-Inverted Data Input  |           3 |         |
|    37 | CML-I      | Tx1n         | Transmitter Inverted Data Output     |           3 |         |
|    38 |            | GND          | Ground                               |           1 |       1 |


## ModuleTek

Note 1: GND is the symbol for signal and supply (power) common for the QSFP28 module. All are common within the QSFP28 module and all module voltages are referenced to this potential unless otherwise noted. Connect these directly to the host board signal-common ground plane.

Note 2: Vcc Rx, Vcc1 and Vcc Tx are the receiver and transmitter power supplies and shall be applied concurrently. Requirements defined for the host side of the Host Edge Card Connector are listed in MSA. The connector pins are each rated for a maximum current of 1000 mA.

## Mechanical Dimension

![Image](/QSFP/QSFP-100G-LR/QSFP-100G-LR_artifacts/image_000008_9cd51f28ecca5acdd85784e0a2746d45cad8360d9164ec24b6184ef8f97115dd.png)

## Warnings

Handling Precautions: This device is susceptible to damage as a result of electrostatic discharge (ESD). A static free environment is highly recommended. Follow guidelines according to proper ESD procedures. Laser Safety: The Moduletek family Transceiver uses a semiconductor laser system and is a laser class1 product acc. FDA, complies with 21CFR1040. 10 and 1040.11. Also this product is a laser class 1 product acc. IEC 60825-1.