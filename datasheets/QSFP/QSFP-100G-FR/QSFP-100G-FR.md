
## DATA SHEET

## MODULETEK : QSFP-100G-FR

100Gb/s QSFP28 FR Optical Transceiver

## QSFP-100G-FR Overview

MODULETEK's QSFP-100G-FR optical transceiver converts 4 input channels of 25Gb/s electrical data to 4 FR optical signals, and multiplexes them into a single channel for 100Gb/s optical transmission. Reversely, on the receiver side, the module optically demultiplexes a 100Gb/s input into 4 FR channels signals, and converts them to 4 channels output electrical data.

## Product Features

- ⚫ Uncooled 4x25Gb/s FR transmitter
- ⚫ QSFP28 MSA compliant
- ⚫ Supports 103.1Gb/s bit rate
- ⚫ Compliant with 100G FR MSA Specification
- ⚫ Duplex LC connector
- ⚫ Built-in digital diagnostic functions
- ⚫ Up to 2km on Single Mode Fiber
- ⚫ RoHS Compliant
- ⚫ Operating temperature range: 0 ℃ to 70 ℃

## Applications

- ⚫ Data Center Interconnect
- ⚫ 100G Ethernet
- ⚫ Infiniband QDR and DDR interconnects

## Ordering Information

| Description                                      |
|--------------------------------------------------|
| 100GBASE-FR QSFP28 Transceiver, LC, 2km over SMF |
| For More Information: MODULETEK Limited          |


## General Specifications

| Parameter                   | Symbol   | Min      |   Typ | Max     | Unit   |   Remarks |
|-----------------------------|----------|----------|-------|---------|--------|-----------|
| Bit Error Rate              | BER      |          |       | 10 - 12 |        |           |
| Signaling Rate each Channel |          | 25.78125 |       |         | Gb/s   |           |
| Operating Temperature       | T OP     | 0        |       | 70      | ℃      |         1 |
| Storage Temperature         | T STO    | - 40     |       | 85      | ℃      |         2 |
| Input Voltage               | V CC     | 3.14     |   3.3 | 3.46    | V      |           |

## Notes:

1. Case temperature
2. Ambient temperature

## Link Distances

| Parameter   | Fiber Type   |   Distance Range (km) |
|-------------|--------------|-----------------------|
| 100 Gb/s    | 9/125um SMF  |                     2 |

## Optical Characteristics -Transmitter

| Parameter                                 | Symbol    | Min    |       Typ | Max    | Unit   | Remarks   |
|-------------------------------------------|-----------|--------|-----------|--------|--------|-----------|
| Signaling rate, each lane (range)         |           |        |   25.7812 |        | Gb/s   |           |
| Total Average Launch Power                | P T       |        |           | 8.5    | dBm    |           |
| Average Launch Power, Each Lane           | P         | - 6.5  |           | 2.5    | dBm    |           |
| Optical Center Wavelength                 |  0       | 1264.5 | 1271      | 1277.5 | nm     |           |
| Optical Center Wavelength                 |  1       | 1284.5 | 1291      | 1297.5 | nm     |           |
| Optical Center Wavelength                 |  2       | 1304.5 | 1311      | 1317.5 | nm     |           |
| Optical Center Wavelength                 |  3       | 1324.5 | 1331      | 1337.5 | nm     |           |
| Optical Modulation Amplitude, Each Lane   | OMA       | - 4    |           | 2.5    | dBm    |           |
| Extinction Ratio                          | ER        | 3.5    |           |        | dB     |           |
| Side Mode Suppression Ratio               | SMSR      | 30     |           |        | dB     |           |
| Transmitter Dispersion Penalty            | TDP       |        |           | 3      | dB     |           |
| Optical Return Loss Tolerance             |           |        |           | 20     | dB     |           |
| Transmitter reflectance                   |           |        |           | - 12   | dB     |           |
| Launch Power of OFF Transmitter, per lane | P OUT_OFF |        |           | - 30   | dBm    |           |

## Optical Characteristics -Receiver

| Parameter                         | Symbol   |    Min |       Typ |    Max | Unit   | Remarks   |
|-----------------------------------|----------|--------|-----------|--------|--------|-----------|
| Signaling rate, each lane (range) |          |        |   25.7812 |        | Gb/s   |           |
| Optical Center Wavelength         |  0      | 1264.5 | 1271      | 1277.5 | nm     |           |
|                                   |  1      | 1284.5 | 1291      | 1297.5 | nm     |           |
|                                   |  2      | 1304.5 | 1311      | 1317.5 | nm     |           |

## ModuleTek

|                                         |  3      | 1324.5   | 1331   | 1337.5   | nm   |
|-----------------------------------------|----------|----------|--------|----------|------|
| Optical Average Input Power, each lane  | P IN     | - 11.5   |        | 2.5      | dBm  |
| Optical Modulation Amplitude, Each Lane |          |          |        | 2.5      | dBm  |
| Damage Threshold                        | P        | 3.5      |        |          | dBm  |
| Receiver Sensitivity (OMA), Each Lane   | R X_SEN1 |          |        | - 10     | dBm  |
| Receiver Reflectance                    | TR RX    |          |        | - 26     | dB   |
| LOS Assert                              | LOS A    |          | TBD    |          | dBm  |
| LOS De-Assert                           | LOS D    |          | TBD    |          | dBm  |
| LOS Hysteresis                          |          |          | TBD    |          | dB   |

## Electrical Characteristics

| Parameter         | Symbol   | Min   | Typ   |    Max | Unit   | Remarks   |
|-------------------|----------|-------|-------|--------|--------|-----------|
| Power Consumption | P        |       |       |    3.5 | W      |           |
| Supply Current    | I CC     |       |       | 1200   | A      |           |

## Block Diagram of Transceiver

![Image](/QSFP/QSFP-100G-FR/QSFP-100G-FR_artifacts/image_000002_3cf317dd88661731ec91a326fedf97ac0892dca85f7094237d0ce7479596c78f.png)

This product converts the 4-channel 25Gb/s electrical input data into CWDM optical signals (light), by a driven 4-wavelength distributed Feedback Laser array. The light is combined by the MUX parts as a 100Gb/s data, propagating out of the transmitter module from the SMF. The receiver module accepts the 100Gb/s CWDM optical signals input, and de-multiplexes it into 4 individual 25Gb/s channels with different wavelength. Each wavelength light is collected by a discrete photo diode, and then outputted as electric data after amplified by a TIA.


## Dimensions

![Image](/QSFP/QSFP-100G-FR/QSFP-100G-FR_artifacts/image_000004_65d75abf0b755624ba13d9c758fc08b4236dc5f4ce990d372a6a6a555d943aee.png)

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm

## Electrical Pad Layout

![Image](/QSFP/QSFP-100G-FR/QSFP-100G-FR_artifacts/image_000005_87cd796a0f510e0d1ba7981c464f5c9f028ffa79eb5d685cb29d4b17289f855f.png)

## Pin Assignment

|   PIN # | Symbol   | Description                         | Remarks   |
|---------|----------|-------------------------------------|-----------|
|       1 | GND      | Ground                              |           |
|       2 | Tx2n     | Transmitter Inverted Data Input     |           |
|       3 | Tx2p     | Transmitter Non-Inverted Data Input |           |

|   4 | GND      | Ground                              |
|-----|----------|-------------------------------------|
|   5 | Tx4n     | Transmitter Inverted Data Input     |
|   6 | Tx4p     | Transmitter Non-Inverted Data Input |
|   7 | GND      | Ground                              |
|   8 | ModSelL  | Module Select                       |
|   9 | ResetL   | Module Reset                        |
|  10 | V cc R X | +3.3V Power Supply Receiver         |
|  11 | SCL      | 2-wire serial interface clock       |
|  12 | SDA      | 2-wire serial interface data        |
|  13 | GND      | Ground                              |
|  14 | Rx3p     | Receiver Non-Inverted Data Output   |
|  15 | Rx3n     | Receiver Inverted Data Output       |
|  16 | GND      | Ground                              |
|  17 | Rx1p     | Receiver Non-Inverted Data Output   |
|  18 | Rx1n     | Receiver Inverted Data Output       |
|  19 | GND      | Ground                              |
|  20 | GND      | Ground                              |
|  21 | Rx2n     | Receiver Inverted Data Output       |
|  22 | Rx2p     | Receiver Non-Inverted Data Output   |
|  23 | GND      | Ground                              |
|  24 | Rx4n     | Receiver Inverted Data Output       |
|  25 | Rx4p     | Receiver Non-Inverted Data Output   |
|  26 | GND      | Ground                              |
|  27 | ModPrsL  | Module Present                      |
|  28 | IntL     | Interrupt                           |
|  29 | V cc T X | +3.3V Power Supply transmitter      |
|  30 | V cc1    | +3.3V Power Supply                  |
|  31 | LPMode   | Low Power Mode                      |
|  32 | GND      | Ground                              |
|  33 | Tx3p     | Transmitter Non-Inverted Data Input |
|  34 | Tx3n     | Transmitter Inverted Data Input     |
|  35 | GND      | Ground                              |
|  36 | Tx1p     | Transmitter Non-Inverted Data Input |
|  37 | Tx1n     | Transmitter Inverted Data Input     |
|  38 | GND      | Ground                              |

## References

1. 100G FR MSA Specification

2. QSFP28 MSA