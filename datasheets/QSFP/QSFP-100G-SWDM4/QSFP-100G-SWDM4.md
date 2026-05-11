
## DATA SHEET

## QSFP-100G-SWDM4

100G QSFP28 SWDM4 MMF 850nm~940nm 150m on OM5 LC

## Product Specifications

The ModuleTek QSFP-100G-SWDM4 transceiver modules are designed for use in 100G Ethernet links over duplex multimode fiber. Four channels/lanes in the 850940nm region @ 25.78Gbps to transport the Ethernet signal. Digital diagnostics functions are available via an I2C interface, as specified by the QSFP28 MSA.

## Feature

- Compliant with QSFP28 MSA
- Compliant with SWDM MSA
- Compliant with IEEE802.3bm CAUI-4
- Hot-pluggable QSFP28 form factor
- 4x25Gb/s 850mm VCSEL-based transmitter
- Supports 103.1Gbps aggregate bit rate
- Power dissipation&lt;3.5W
- Maximum link length of 150m on OM5 multimode

## Fiber

- Case temperature range of 0 ° C to 70 ° C
- Duplex LC receptacles
- CAUI-4 electrical interface
- RoHS compliant

## Applications

- 100G Ethernet over Duplex MMF


## 1. Absolute Maximum Ratings

| Parameter         | Symbol   | Min   | Max   | Units   |
|-------------------|----------|-------|-------|---------|
| StorageTempRange  | Ts       | -40   | +85   | ℃       |
| Supply Voltage    | Vcc      | -0.5  | 3.6   | V       |
| Relative Humidity | RH       | 15%   | 85%   |         |

## 2 . Operating Conditions

| Parameter                 | Symbol   |   Min |    Max | Units   |
|---------------------------|----------|-------|--------|---------|
| Case Temp-Operating       | Tcase    |  0    |  70    | ℃       |
| Supply Voltage            | Vcc      |  3.14 |   3.46 | V       |
| PowerConsumption          | P        |       |   3.5  | W       |
| Link Distance on OM3Fiber |          |       |  75    | M       |
| Link Distance on OM4Fiber |          |       | 100    | M       |
| Link Distance on OM5Fiber |          |       | 150    | M       |


## 3. Optical Characteristics

| Transmitter Parameter                                                                     | Lane                    | Min                           | Typical                       | Max                           | Unit                          | Note   |
|-------------------------------------------------------------------------------------------|-------------------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|--------|
| Signaling rate, each lane                                                                 | 25.78125 ± 100ppm       | 25.78125 ± 100ppm             | 25.78125 ± 100ppm             | 25.78125 ± 100ppm             | Gb/s                          |        |
| Lane Wavelength Range                                                                     | Lane0 Lane1 Lane2 Lane3 | 844 874 904 934               |                               | 858 888 918 948               | nm                            |        |
| Modulation Format                                                                         | NRZ                     | NRZ                           | NRZ                           | NRZ                           | NRZ                           | NRZ    |
| Difference in launch power between anytwo lanes                                           |                         |                               |                               | 4.5                           | dBm                           |        |
| RMSSpectral width                                                                         |                         |                               |                               | 0.59                          | nm                            | 1      |
| Optical Modulation Amplitude (OMA), each lane                                             |                         | -5.5                          |                               | 3                             | dBm                           | 2      |
| Average Launch Power per Lane @TXOffState                                                 |                         |                               |                               | -30                           | dBm                           |        |
| Launch Power in OMAminusTDEC                                                              | Lane0 Lane1 Lane2 Lane3 | -7 -7 -7.4 -7.7               |                               |                               | dBm                           |        |
| Transmitter and Dispersion EyeClosure                                                     | Lane0 Lane1 Lane2 Lane3 |                               |                               | 4 4 4.4 4.8                   | dB                            | 3      |
| Extinction Ratio                                                                          |                         | 2                             |                               |                               | dB                            |        |
| Optical Return LossTolerance                                                              |                         |                               |                               | 12                            | dB                            |        |
| Encircled Flux                                                                            |                         | ≥86% at 19um ≤30% at 4.5um    | ≥86% at 19um ≤30% at 4.5um    | ≥86% at 19um ≤30% at 4.5um    | ≥86% at 19um ≤30% at 4.5um    | 4      |
| Transmitter eye mask definition {X1, X2, X3,Y1, Y2, Y3} Hit ratio 1.5x10-3 hits persample |                         | {0.3,0.38,0.45,0.35,0.41,0.5} | {0.3,0.38,0.45,0.35,0.41,0.5} | {0.3,0.38,0.45,0.35,0.41,0.5} | {0.3,0.38,0.45,0.35,0.41,0.5} |        |

## Notes:

1. RMS spectral width is the standard deviation of the spectrum.
2. The normative lowest value of OMA for a compliant transmitter is 'Launch power in OMA minus TDEC, each lane (min)' plus the actual value of 'TDEC', but with a value of at least 'OMA, each lane (min)'.
3. TDEC is calculated from the measured TDECm using the methods in 3.6. TDECm is measured following the method in IEEE 802.3 clause 95.8.5 using a 12.6 GHz bandwidth reference receiver for all lanes.
4. If measured into type A1a.2 or type A1a.3 50 um fiber in accordance with IEC 61280-1-4.


| Receiver Parameter                              | Lane                                            | Min                                             | Typical                                         | Max                                             | Unit                                            |                                                 |
|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|
| Signaling rate, each lane                       | 25.78125 ± 100ppm                               | 25.78125 ± 100ppm                               | 25.78125 ± 100ppm                               | 25.78125 ± 100ppm                               | Gb/s                                            |                                                 |
| Lane Wavelength Range                           | Lane0 Lane1 Lane2 Lane3                         | 844 874 904 934                                 |                                                 | 858 888 918 948                                 | nm                                              |                                                 |
| Modulation Format                               | NRZ                                             | NRZ                                             | NRZ                                             | NRZ                                             |                                                 |                                                 |
| DamageThreshold                                 |                                                 | 4.4                                             |                                                 |                                                 | dBm                                             |                                                 |
| Average Receive Power, eachlane                 | Lane0 Lane1 Lane2 Lane3                         | -9.5 -9.4 -9.4 -9.4                             |                                                 | 3.4                                             | dBm                                             |                                                 |
| Receiver Power, each lane(OMA)                  |                                                 |                                                 |                                                 | 3                                               | dBm                                             |                                                 |
| Receiver Reflectance                            |                                                 |                                                 |                                                 | -12                                             | dB                                              |                                                 |
| unStressed ReceiverSensitivity(OMA)             | Lane0 Lane1 Lane2 Lane3                         |                                                 |                                                 | -8.2 -8.4 -8.6 -8.8                             | dBm                                             |                                                 |
| RX_Los_Assert                                   |                                                 | -30                                             |                                                 |                                                 | dBm                                             |                                                 |
| RX_Los_De-ASSERT                                |                                                 |                                                 |                                                 | -12                                             | dBm                                             |                                                 |
| RX_Los_Hysteresis                               |                                                 | 0.5                                             |                                                 |                                                 | dBm                                             |                                                 |
| 1.unstressed sensitivity at BER of 5E-5(preFEC) | 1.unstressed sensitivity at BER of 5E-5(preFEC) | 1.unstressed sensitivity at BER of 5E-5(preFEC) | 1.unstressed sensitivity at BER of 5E-5(preFEC) | 1.unstressed sensitivity at BER of 5E-5(preFEC) | 1.unstressed sensitivity at BER of 5E-5(preFEC) | 1.unstressed sensitivity at BER of 5E-5(preFEC) |

## 4. Digital Diagnostic Monitoring Specifications

| Parameters                  | Unit   | Specification   |
|-----------------------------|--------|-----------------|
| Temperature Monitor         | ° C    | ± 3             |
| Voltage Monitor             | V      | ± 5%            |
| I_bias Monitor              | mA     | ± 10%           |
| Received Power (Rx) Monitor | dB     | ± 3.0           |
| Transmit Power (Tx) Monitor | dB     | ± 3.0           |


## 5. Electrical Characteristics

| Transmitter electrical input signal characteristics(TP1)   | Min                | Typical            | Max                | Unit   |
|------------------------------------------------------------|--------------------|--------------------|--------------------|--------|
| Signaling rate per lane (range)                            | 25.78125 ± 100 ppm | 25.78125 ± 100 ppm | 25.78125 ± 100 ppm | GBd    |
| Differential input return loss                             | Equation (83E - 5) |                    |                    | dB     |
| Differential to common mode input return loss              | Equation (83E - 6) |                    |                    | dB     |
| Differential termination mismatch                          |                    |                    | 10                 | %      |
| Module stressed input test                                 | See 83E3.4.1       |                    |                    |        |
| Differential pk-pk input voltage tolerance                 | 900                |                    |                    | mV     |
| DC common modevoltage                                      | -350               |                    | 2850               | mV     |
| Single ended voltage tolerance range                       | -0.4               |                    | 3.3                | V      |
| Receiver electrical output signal characteristics(TP4)     | Min                | Typical            | Max                | Unit   |
| Signaling rate per lane (range)                            | 25.78125 ± 100 ppm | 25.78125 ± 100 ppm | 25.78125 ± 100 ppm | GBd    |
| AC common-mode output voltage (RMS)                        |                    |                    | 17.5               | mV     |
| Differential output voltage                                |                    |                    | 900                | mV     |
| Eye width                                                  | 0.57               |                    |                    | UI     |
| Eye height, differential                                   | 228                |                    |                    | mV     |
| Vertical eye closure                                       |                    |                    | 5.5                | dB     |
| Differential output return loss                            | Equation (83E - 2) |                    |                    | dB     |
| Commonto differential mode conversion return loss          | Equation (83E - 3) |                    |                    | dB     |
| Differential termination mismatch                          |                    |                    | 10                 | %      |
| Transition time (20% to 80%)                               | 12                 |                    |                    | ps     |
| DC common modevoltage                                      | -350               |                    | 2850               | mV     |


## 6. QSFP28 Connector and Pinout Description

The electrical interface to the transceiver is a 38 pins edge connector. The 38 pins provide high speed data, low speed monitoring and control signals, I2C communication, power and ground connectivity. The top and bottom views of the connector are provided below, as well as a table outlining the contact numbering, symbol and fulldescription.

Figure 1. QSFP28-compliant 38-pin connector

![Image](/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4_artifacts/image_000006_641e2739d616721297be15bf39375a5d867ce30935f749a16d272fb0499cb98e.png)


|   Pin | Symbol   | Name/Description                                 |   NOTE |
|-------|----------|--------------------------------------------------|--------|
|     1 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|     2 | Tx2n     | Transmitter Inverted Data Input                  |        |
|     3 | Tx2p     | Transmitter Non-Inverted Data output             |        |
|     4 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|     5 | Tx4n     | Transmitter Inverted Data Input                  |        |
|     6 | Tx4p     | Transmitter Non-Inverted Data output             |        |
|     7 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|     8 | ModSelL  | Module Select                                    |        |
|     9 | ResetL   | Module Reset                                     |        |
|    10 | VccRx    | 3.3V Power Supply Receiver                       |      2 |
|    11 | SCL      | 2-Wire serial Interface Clock                    |        |
|    12 | SDA      | 2-Wire serial Interface Data                     |        |
|    13 | GND      | Transmitter Ground (Common with Receiver Ground) |        |
|    14 | Rx3p     | Receiver Non-Inverted Data Output                |        |
|    15 | Rx3n     | Receiver Inverted Data Output                    |        |
|    16 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    17 | Rx1p     | Receiver Non-Inverted Data Output                |        |
|    18 | Rx1n     | Receiver Inverted Data Output                    |        |
|    19 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    20 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    21 | Rx2n     | Receiver Inverted Data Output                    |        |
|    22 | Rx2p     | Receiver Non-Inverted Data Output                |        |
|    23 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    24 | Rx4n     | Receiver Inverted Data Output                    |        |
|    25 | Rx4p     | Receiver Non-Inverted Data Output                |        |
|    26 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    27 | ModPrsl  | Module Present                                   |        |
|    28 | IntL     | Interrupt                                        |        |
|    29 | VccTx    | 3.3V power supply transmitter                    |      2 |
|    30 | Vcc1     | 3.3V power supply                                |      2 |
|    31 | LPMode   | Low Power Mode ， not connect                    |        |
|    32 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    33 | Tx3p     | Transmitter Non-Inverted Data Input              |        |
|    34 | Tx3n     | Transmitter Inverted Data Output                 |        |
|    35 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |
|    36 | Tx1p     | Transmitter Non-Inverted Data Input              |        |
|    37 | Tx1n     | Transmitter Inverted Data Output                 |        |
|    38 | GND      | Transmitter Ground (Common with Receiver Ground) |      1 |

Notes: 1. GND is the symbol for signal and supply (power) common for QSFP28 modules. All are common within the QSFP28 module and all module voltages are referenced to this potential unless otherwise noted. Connect these directly to the host board signal common ground plane.

2. VccRx, Vcc1 and VccTx are the receiving and transmission power suppliers and shall be applied concurrently. Recommended host board power supply filtering is shown below. Vcc Rx, Vcc1 and Vcc Tx may be internally connected within the QSFP28 transceiver module in any combination. The connector pins are each rated for a maximum current of 1000mA.


## 7. Memory map

## Compatible with SFF-8636

## 8. Mechanical Dimensions

Unit:  mm

Pull tab color:  Gray ,Pantone 424U

Figure 2. Mechanical dimensions

![Image](/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4_artifacts/image_000009_4657950a5892b293dc9e151d4e88280e6a1d93ec5c7bf1c401824d5903f6de5d.png)

![Image](/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4_artifacts/image_000010_0fc08c2d270e8c8e77d7d665d57c1301dc7fee7de64850975f2801d99a98a6b2.png)