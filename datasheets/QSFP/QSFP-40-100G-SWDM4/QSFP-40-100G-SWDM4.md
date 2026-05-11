
## Datasheet:

ModuleTek: QSFP-40/100G-SRBD QSFP28  40/100GBASE  SWDM4  Dual  Rate  850nm  100m  OM4  DOM  Duplex  LC  MMF  Optical

Transceiver

## Description:

The 40G/100G QSFP28 SWDM4 transceiver modules are designed for use in 40G/100G Ethernet links over duplex multimode fiber. Four channels/lanes in the 850-940nm region @10.3125Gb/s / @ 25.78Gbps to transport the Ethernet signal. Digital diagnostics functions    are available via an I2C interface, as specified by the QSFP28 MSA.

## Feature

-  Compliant with QSFP28 MSA
-  Compliant with SWDM MSA
-  Compliant with IEEE802.3bm CAUI-4
-  Hot-pluggable QSFP28 form factor
-  4x25Gb/s 850nm VCSEL-based    transmitter
-  Supports 40G/100G Dual-Rate operation
-  Power dissipation&lt;3.5W
-  Maximum link length of 150m on OM5 multimode Fiber
-  Case temperature range of 0 ° C to 70 ° C
-  Duplex LC receptacles
-  CAUI-4 electrical interface
-  RoHS compliant

## Applications

-  40G Ethernet over Duplex MMF
-  100G Ethernet over Duplex MMF


## 1. Absolute Maximum Ratings

| Parameter          | Symbol   | Min   | Max   | Units   |
|--------------------|----------|-------|-------|---------|
| Storage Temp Range | Ts       | -40   | +85   | ℃       |
| Supply Voltage     | Vcc      | -0.5  | 3.6   | V       |
| Relative Humidity  | RH       | 15%   | 85%   |         |

| Parameter                         | Symbol   |   Min |    Max | Units   |
|-----------------------------------|----------|-------|--------|---------|
| Case Temp-Operating               | Tcase    |  0    |  70    | ℃       |
| Supply Voltage                    | Vcc      |  3.14 |   3.46 | V       |
| Power Consumption                 | P        |       |   3.5  | W       |
| Link Distance on OM3 Fiber (100G) |          |       |  75    | M       |
| Link Distance on OM4 Fiber (100G) |          |       | 100    | M       |
| Link Distance on OM5 Fiber (100G) |          |       | 150    | M       |
| Link Distance on OM3 Fiber (40G)  |          |       | 240    | M       |
| Link Distance on OM4 Fiber (40G)  |          |       | 350    | M       |
| Link Distance on OM5 Fiber (40G)  |          |       | 440    | M       |

![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000002_3f16cd44f8e5b724a2d2bfb4d1d3bcb53875b47c848aa41264b5dbf8c9fc0e26.png)


## 3. Optical Characteristics @25.78125Gb/s

| Transmitter Parameter                                                                       | Lane                    | Min                           | Typical                       | Max                           | Unit                          |   Note |
|---------------------------------------------------------------------------------------------|-------------------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|--------|
| Signaling rate, each lane                                                                   |                         | 25.78125±100ppm               | 25.78125±100ppm               | 25.78125±100ppm               | Gb/s                          |        |
| Lane Wavelength Range                                                                       | Lane0 Lane1 Lane2 Lane3 | 844 874 904 934               |                               | 858 888 918 948               | nm                            |        |
| Modulation Format                                                                           |                         | NRZ                           |                               |                               |                               |        |
| Difference in launch power between any two lanes                                            |                         |                               |                               | 4.5                           | dBm                           |        |
| RMS Spectral width                                                                          |                         |                               |                               | 0.59                          | nm                            |      1 |
| Optical Modulation Amplitude (OMA), each lane                                               |                         | -5.5                          |                               | 3                             | dBm                           |      2 |
| Average Launch Power per Lane @TXOff State                                                  |                         |                               |                               | -30                           | dBm                           |        |
| Launch Power in OMAminus TDEC                                                               | Lane0 Lane1 Lane2 Lane3 | -7 -7 -7.4 -7.7               |                               |                               | dBm                           |        |
| Transmitter and Dispersion Eye Closure                                                      | Lane0 Lane1 Lane2 Lane3 |                               |                               | 4 4 4.4 4.8                   | dB                            |      3 |
| Extinction Ratio                                                                            |                         | 2                             |                               |                               | dB                            |        |
| Optical Return Loss Tolerance                                                               |                         |                               |                               | 12                            | dB                            |        |
| Encircled Flux                                                                              |                         | ≥86% at 19 um ≤30% at 4.5 um  | ≥86% at 19 um ≤30% at 4.5 um  | ≥86% at 19 um ≤30% at 4.5 um  | ≥86% at 19 um ≤30% at 4.5 um  |      4 |
| Transmitter eye mask definition {X1, X2, X3, Y1, Y2, Y3} Hit ratio 1.5x10-3 hits per sample |                         | {0.3,0.38,0.45,0.35,0.41,0.5} | {0.3,0.38,0.45,0.35,0.41,0.5} | {0.3,0.38,0.45,0.35,0.41,0.5} | {0.3,0.38,0.45,0.35,0.41,0.5} |        |

## Notes:

1. RMS spectral width is the standard deviation of the spectrum.
2. The normative lowest value of OMA for a compliant transmitter is 'Launch power in OMA minus TDEC, each lane (min)' plus the actual value of 'TDEC', but with a value of at least 'OMA, each lane (min)'.
3. TDEC is calculated from the measured TDECm using the methods in 3.6. TDECm is measured following the method in IEEE 802.3 clause 95.8.5 using a 12.6 GHz bandwidth reference receiver for all lanes.
4. If measured into type A1a.2 or type A1a.3 50 um fiber in accordance with IEC 61280-1-4.


## 4. Optical Characteristics @10.3125Gb/s

![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000005_b9fe8296319fc6b356f966df87a4eaad8da33d1f257ebab5cbdf95eb6797c322.png)

| Transmitter Parameter                                                                     | Lane                    | Min                            | Typical                        | Max                            | Unit                           | Note   |
|-------------------------------------------------------------------------------------------|-------------------------|--------------------------------|--------------------------------|--------------------------------|--------------------------------|--------|
| Signaling rate, each lane                                                                 |                         | 10.3125 , 9.953±100ppm         | 10.3125 , 9.953±100ppm         | 10.3125 , 9.953±100ppm         | Gb/s                           |        |
| Lane Wavelength Range                                                                     | Lane0 Lane1 Lane2 Lane3 | 844 874 904 934                |                                | 858 888 918 948                | nm                             |        |
| Difference in launch power between any two lanes                                          |                         |                                |                                | 4.5                            | dBm                            |        |
| RMS Spectral width                                                                        |                         |                                |                                |                                |                                |        |
| @850nm                                                                                    | Lane0                   |                                |                                | 0.53                           | nm                             |        |
| @880nm,910nm,940nm Optical Modulation Amplitude (OMA), each lane                          | Lane1,2,3               | -5.5                           |                                | 0.59 3                         | dBm                            |        |
| Average Launch power per Lane                                                             |                         | -7.5                           |                                | 3                              | dBm                            |        |
| Launch Power Tx OMA-TDP                                                                   | Lane0 Lane1 Lane2 Lane3 | -6.4 -6.0 -6.5                 |                                |                                | dBm                            |        |
| Transmitter and Dispersion Eye Closure                                                    | Lane0 Lane1 Lane2 Lane3 |                                |                                | 3.7 4.0 4.5 5.0                | dB                             |        |
| Extinction Ratio                                                                          |                         | 2                              |                                |                                | dB                             |        |
| Optical Return Loss Tolerance                                                             |                         | 12                             |                                |                                | dB                             |        |
| Average Launch Power per Lane @TXOff State                                                |                         |                                |                                | -30                            | dBm                            |        |
| Encircled Flux                                                                            |                         | >=86% at 19um <=30% at 4.5um   | >=86% at 19um <=30% at 4.5um   | >=86% at 19um <=30% at 4.5um   |                                |        |
| Transmitter eye mask definition {X1, X2, X3, Y1, Y2, Y3} Hit ratio 5x10-5 hits per sample |                         | {0.23,0.34,0.43,0.27,0.35,0.4} | {0.23,0.34,0.43,0.27,0.35,0.4} | {0.23,0.34,0.43,0.27,0.35,0.4} | {0.23,0.34,0.43,0.27,0.35,0.4} |        |


![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000007_d47c1f9ee5e852356f245143f798594be000554fef218c5cb3f34b24341d4f01.png)

|                                                        | QSFP-40/100G-SWDM4   | QSFP-40/100G-SWDM4      | QSFP-40/100G-SWDM4     | QSFP-40/100G-SWDM4     | QSFP-40/100G-SWDM4   | QSFP-40/100G-SWDM4   |
|--------------------------------------------------------|----------------------|-------------------------|------------------------|------------------------|----------------------|----------------------|
| Receiver Parameter                                     | Lane                 | Min                     | Typical                | Max                    | Unit                 | Note                 |
| Signaling rate, each lane                              |                      | 10.3125 , 9.953±100ppm  | 10.3125 , 9.953±100ppm | 10.3125 , 9.953±100ppm | Gb/s                 |                      |
| Lane Wavelength Range                                  | Lane0                | 844                     |                        | 858                    | nm                   |                      |
| Lane Wavelength Range                                  | Lane1                | 874                     |                        | 888                    |                      |                      |
| Lane Wavelength Range                                  | Lane2                | 904                     |                        | 918                    |                      |                      |
| Lane Wavelength Range                                  | Lane3                | 934                     |                        | 948                    |                      |                      |
| Damage threshold, each lane                            |                      | 3.8                     |                        |                        | dBm                  |                      |
| Average Receive Power, each lane                       |                      | -12.9 -12.5 -12.2 -11.9 |                        | 2.4                    | dBm                  |                      |
| Receiver Power, each lane (OMA)                        |                      |                         |                        | 3                      | dBm                  |                      |
| Receiver sensitivity OMA, per lane                     |                      |                         |                        | -9.1                   | dB                   |                      |
| Difference in receive power between any two lanes(OMA) |                      |                         |                        | 5                      | dB                   |                      |
| RX_Los_Assert                                          |                      | -30                     |                        |                        | dBm                  |                      |
| RX_Los_De-ASSERT                                       |                      |                         |                        | -13                    | dBm                  |                      |
| RX_Los_Hysteresis                                      |                      | 0.5                     |                        |                        | dBm                  |                      |
| Return reflectance                                     |                      |                         |                        | -12                    | dB                   |                      |

## 5. Digital Diagnostic Monitoring Specifications

| Parameters                  | Unit   | Specification   |
|-----------------------------|--------|-----------------|
| Temperature Monitor         | °C     | ± 3             |
| Voltage Monitor             | V      | ±5%             |
| I_bias Monitor              | mA     | ± 10%           |
| Received Power (Rx) Monitor | dB     | ± 3.0           |
| Transmit Power (Tx) Monitor | dB     | ± 3.0           |


## 6. Electrical Characteristics

![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000009_7fa465609541b9ab9ca9dc5293bdd562aaebf825264fed9e7b5f02e2a2d47f2d.png)

| Transmitter electrical input signal characteristics(TP1)   | Min                | Typical   | Max   | Unit   |
|------------------------------------------------------------|--------------------|-----------|-------|--------|
| Signaling rate per lane (range)                            | 25.78125 ± 100 ppm |           |       | GBd    |
| Differential input return loss                             | Equation (83E-5)   |           |       | dB     |
| Differential to common mode input return loss              | Equation (83E-6)   |           |       | dB     |
| Differential termination mismatch                          |                    |           | 10    | %      |
| Module stressed input test                                 | See 83E3.4.1       |           |       |        |
| Differential pk-pk input voltage tolerance                 | 900                |           |       | mV     |
| DC common mode voltage                                     | -350               |           | 2850  | mV     |
| Single ended voltage tolerance range                       | -0.4               |           | 3.3   | V      |
| Receiver electrical output signal characteristics(TP4)     | Min                | Typical   | Max   | Unit   |
| Signaling rate per lane (range)                            | 25.78125 ± 100 ppm |           |       | GBd    |
| AC common-mode output voltage (RMS)                        |                    |           | 17.5  | mV     |
| Differential output voltage                                |                    |           | 900   | mV     |
| Eye width                                                  | 0.57               |           |       | UI     |
| Eye height, differential                                   | 228                |           |       | mV     |
| Vertical eye closure                                       |                    |           | 5.5   | dB     |
| Differential output return loss                            | Equation (83E-2)   |           |       | dB     |
| Common to differential mode conversion return loss         | Equation (83E-3)   |           |       | dB     |
| Differential termination mismatch                          |                    |           | 10    | %      |
| Transition time (20% to 80%)                               | 12                 |           |       | ps     |
| DC common mode voltage                                     | -350               |           | 2850  | mV     |


## 7. QSFP28 Connector and Pinout Description

The electrical interface to the transceiver is a 38 pins edge connector. The 38 pins provide high speed data, low speed monitoring and control signals,  I2C  communication, power and ground connectivity. The top and bottom views of the connector are provided below, as well as a table outlining the contact numbering, symbol and full description.

Figure 1. QSFP28-compliant 38-pin connector

![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000011_ce0ac5e2282ebaf2dbdb2042bbdcabc5567cd3cf475236d985479fc771431215.png)


Moduletek Limited Notes: 1. GND is the symbol for signal and supply (power) common for QSFP28 modules. All are common within  the  QSFP28  module  and  all  module  voltages  are  referenced  to  this  potential unless otherwise noted. Connect these directly to the host board signal common ground plane.

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


2. VccRx, Vcc1 and VccTx are the receiving and transmission power suppliers and shall be applied concurrently. Recommended host board power supply filtering is shown below. Vcc Rx, Vcc1 and Vcc Tx may be internally connected within the QSFP28 transceiver module in any combination. The connector pins are each rated for a maximum current of 1000mA.

## 8. Memory map

Compatible with SFF-8636

## 9. Mechanical Dimensions

Unit:    mm

Pull tab color:    Gray ,Pantone 424U

![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000014_c7e47f5cbc093690e8d7e4fa2eed0295ca96321b0c28edcc3d6f52f7faf945ed.png)

![Image](/QSFP/QSFP-40-100G-SWDM4/QSFP-40-100G-SWDM4_artifacts/image_000015_80cac1965cfbfd0961b5b3ee03a1e37f2e4d28987d84d365ebfbb7ef0692aa93.png)