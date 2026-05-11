
duleTek

## DATA SHEET

## MODULETEK:AOC-SFP-10G-aaa.aaM-C1C1C

10Gb/s SFP+ Active Optical Cable

## AOC-SFP-10G-aaa.aaM-C1C1C Overview

ModuleTek's AOC-SFP-10G-aaa.aaM-C1C1C SFP+ active optical cables are based on 10 Gigabit Ethernet and SFF-8431 standard, and provide a quick and reliable interface for the 10G Ethernet application. The digital diagnostic functions are available via 2-wire serial bus specified in SFF-8472.

## Product Features

- Up to 10.5 Gb/s bi-directional data links
- Compliant with IEEE 802.3ae
- Compliant with SFF-8431
- Hot-pluggable SFP+ footprint
- 850nm VCSEL laser transmitter and PIN receiver
- Built-in digital diagnostic functions
- Up to 300m on OM3 MMF
- Low power consumption (Module work consumption &lt;1W)
- Single power supply 3.3V
- RoHS Compliant
- Operating temperature range （ Case Temperature ） ： 0 ◦ C to 70 ◦ C

## Applications

- 10G Ethernet Data Center Intra-Rack and Inter-Rack links

![Image](/AOC/AOC-10-xM/AOC-10-xM_artifacts/image_000001_8100763cb6cfbeaeb14f23fab8e206308f8e2ff4665e9c9bf3488edd5c777057.png)


## Ordering Information

| Part Number                                                                                                                                                  | Product ID                                                                                                                                                   | Description                                                                                                                                                  | Color on Clasp                                                                                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AOC-SFP-10G- aaa.aaM-C1C1C                                                                                                                                   | M253801                                                                                                                                                      | 10G SFP+ Active Optical Cable up to 300m on OM3 MMF, with DOM function                                                                                       | Blue                                                                                                                                                         |
| Notes ： 1.Product ID is the abbreviated order number of the standard model of our products 2.'aaa.aa'indicates the cable length in meter,1.00≤aaa.aa≤300.00 | Notes ： 1.Product ID is the abbreviated order number of the standard model of our products 2.'aaa.aa'indicates the cable length in meter,1.00≤aaa.aa≤300.00 | Notes ： 1.Product ID is the abbreviated order number of the standard model of our products 2.'aaa.aa'indicates the cable length in meter,1.00≤aaa.aa≤300.00 | Notes ： 1.Product ID is the abbreviated order number of the standard model of our products 2.'aaa.aa'indicates the cable length in meter,1.00≤aaa.aa≤300.00 |
| For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                    | For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                    | For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                    | For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                    |

## General Specifications

| Parameter             | Symbol   |    Min |      Typ | Max     | Unit   |   Remarks |
|-----------------------|----------|--------|----------|---------|--------|-----------|
| Data Rate             | DR       |        |  10.3125 |         | Gb/s   |         1 |
| Bit Error Rate        | BER      |        |          | 10 - 12 |        |           |
| Operating Temperature | T C      |   0    |          | 70      | ◦ C    |         2 |
| Storage Temperature   | T STO    | -40    |          | 85      | ◦ C    |         3 |
| Supply Current        | I CC     |        | 180      | 290     | mA     |         4 |
| Input Voltage         | V CC     |   3.14 |   3.3    | 3.46    | V      |           |
| Maximum Voltage       | V MAX    |  -0.5  |          | 4       | V      |         4 |

## Notes:

1. IEEE 802.3ae
2. Case temperature
3. Ambient temperature
4. For electrical power interface


## Electrical - Characteristics - Transmitter

V CC =3.14V to 3.46V,T C =0 ◦ C to 70 ◦ C

| Parameter                     | Symbol   | Min   |   Typ | Max        | Unit   |   Remarks |
|-------------------------------|----------|-------|-------|------------|--------|-----------|
| Input differential impedance  | R IN     |       |   100 |            | Ω      |         1 |
| Differential data input swing | V IN PP  | 180   |       | 700        | mV     |           |
| Transmit Disable Voltage      | V D      | 2     |       | V CC       | V      |           |
| Transmit Enable Voltage       | V EN     | V EE  |       | V EE + 0.8 | V      |           |

## Notes:

1. Non-condensing

## Electrical - Characteristics - Receiver

V CC =3.14V to 3.46V,T C =0 ◦ C to 70 ◦ C

| Parameter                       | Symbol   | Min   | Typ   | Max        | Unit   | Remarks   |
|---------------------------------|----------|-------|-------|------------|--------|-----------|
| Differential data output swing  | V OUT PP | 300   |       | 850        | mV     |           |
| Data output rise time (20%-80%) | t r      | 30    |       |            | ps     |           |
| Data output fall time(20%-80%)  | t f      | 30    |       |            | ps     |           |
| LOS Fault                       | V LOS A  | 2     |       | V CC HOST  | V      |           |
| LOS Normal                      | V LOS D  | V EE  |       | V EE + 0.5 | V      |           |


## A0H Register Description

| IIC Addr    | Size   | Name                   | Description                                                                                                         | Values(HEX)              |
|-------------|--------|------------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------|
| 0           | 1      | Identifier             | SFP+                                                                                                                | 03                       |
| 1           | 1      | Extended Identifier    | Use IIC interface                                                                                                   | 04                       |
| 2           | 1      | Connector              | Optical Pigtail                                                                                                     | 0B                       |
| 3-10        | 8      | Transceiver            | Active Cable                                                                                                        | 00 00 00 00 00 08 00 00  |
| 11          | 1      | Encoding               | 64B/66B                                                                                                             | 06                       |
| 12          | 1      | BR, Nominal            | Nominal Bit Rate 10.3Gb/s                                                                                           | 67                       |
| 13          | 1      | Rate Identifier        | Without rate selection function                                                                                     | 00                       |
| 14          | 1      | Length(9μm)-km         | Link Length / SMF = N/A                                                                                             | 00                       |
| 15          | 1      | Length (9μm)-100m      | Link Length / SMF = N/A                                                                                             | 00                       |
| 16          | 1      | Length (50μm)-10m      | 50μm MMF Link Length = 80m                                                                                          | 00                       |
| 17          | 1      | Length (62.5μm)-10m    | 62.5μm MMF Link Length = 20m                                                                                        | 00                       |
| 18          | 1      | Length (Copper)        | Copper Link Length = N/A                                                                                            | 00                       |
| 19          | 1      | Length (50μm)-10m      | 50μm MMF Link Length = 300m                                                                                         | 1E                       |
| 20-35       | 16     | Vendor name            | ModuleTek                                                                                                           | ASCII Format             |
| 36          | 1      | Transceiver            | Reserved                                                                                                            | 00                       |
| 37-39       | 3      | Vendor OUI             | Without vendor OUI                                                                                                  | 00 00 00                 |
| 40-55       | 16     | Vendor PN              | Part number in the Ordering Information                                                                             | Programmed by Factory    |
| 56-59       | 4      | Vendor Revision Number | Manufacturer product version number                                                                                 | Programmed by Factory    |
| 60-61       | 2      | Wavelength             | Laser Wavelength                                                                                                    | 03 52                    |
| 62          | 1      | Reserved               | Reserved                                                                                                            | 00 Programmed by         |
| 63          | 1      | CC_BASE                | Checksum of bytes 0-62 Indicates which optional transceiver signals are                                             | Factory                  |
| 64-65       | 2      | Transceiver Options    | implemented                                                                                                         | 00 00                    |
| 66 67       | 1      | BR, max                | NA NA                                                                                                               | 00                       |
|             | 1      | BR, min                |                                                                                                                     | 00 Programmed by Factory |
| 68-83 84-91 | 16 8   | Vendor SN Date code    | Manufacturer serial number Date code                                                                                | Programmed by            |
| 92          | 1      | Monitoring Type        | Internal calibration of DOM RxPower measurement using average optical power                                         | Factory 68               |
| 93          | 1      | Enhanced Options       | 1.Monitor Alarm and Warning of TxPower and RxPower 2.Tx_DIS Monitor and Control 3.Rx_LOS Monitor 4.Tx_FAULT Monitor | F0                       |
| 94          | 1      | Compliance             | Revision Implemented                                                                                                | 08                       |
| 95          | 1      | CC_EXT                 | Check sum of bytes 64-94                                                                                            | Programmed by Factory    |
| 96-127      | 32     | Vendor Specific        | Vendor Specific Area                                                                                                | Programmed by Factory    |
| 128-255     | 128    | Vendor Specific        | Vendor Specific Area                                                                                                | Programmed by Factory    |


## Digital Diagnostic Functions

AOC-SFP-10G-aaa.aaM-C1C1C supports the 2-wire serial communication protocol as defined in SFF8472. Digital diagnostic information is accessible over the 2-wire interface at the address 0xA2. Digital diagnostics for AOC-SFP-10G-aaa.aaM-C1C1C are internally calibrated by default. The internal micro control unit accesses the device operating parameters in real time,Such as transceiver temperature, laser bias current, transmitted optical power, received optical power and transceiver supply voltage.The module implements the alarm function of the SFF-8472,alerts the user when a particular operating parameter exceeds the factory-set normal range.

## Block-Diagram-of-Transceiver

![Image](/AOC/AOC-10-xM/AOC-10-xM_artifacts/image_000006_344be81065ad6711ba3a717335c62b6714a94ddcda6ec3cc31a5bec2576f10d5.png)

## Functions Description

The transmitter is mainly composed of a laser driver part of the intelligent transceiver chip and a TOSA (light-emitting component), the TOSA includes a 850nm VCSEL laser and a backlight photodetection chip,When the module is working, the input signal is connected to the intelligent transceiver chip, at this time, the laser driver of the intelligent transceiver chip supplies the bias current and the modulation current to the laser.The intelligent transceiver chip simultaneously uses an automatic optical power control (APC) feedback loop to maintain a constant average optical power of the laser output. The purpose is to eliminate the change of the output optical signal due to temperature changes and aging of the light source device.When the transmitter enable pin (TX\_Disable) is high (TTL logic '1'), the laser output is turned off. When TX\_Disable is low (TTL logic '0'), the laser will turn on within 1ms.When the transmitter fault signal (TX\_Fault) is reported as high,indicates a transmitter failure caused by the transmitter's bias current or transmitted optical power or laser tube temperature exceeding a preset alarm threshold. Low indicates normal operation.

The receiver is mainly composed of a limiting amplifier part of the intelligent transceiver chip and a ROSA (light-receiving component),the ROSA includes a PIN photodetector and a transimpedance amplifier chip.When the ROSA detects the incident light signal, it will be converted into a photo-generated current by the PIN photodetector. The photo-generated current is converted into an electrical signal after passing through the transimpedance amplifier. The electrical signal is further amplified by the limiting amplifier of the intelligent transceiver chip, then outputs a fixed-amplitude electrical signal to the host.When the amplitude of the electrical signal received from the incident light conversion of the opposite optical transceiver module is lower than the set threshold,the module reports that the received signal is lost,the RX\_LOS pin is high (logic '1'),which can be used to diagnose whether the physical signal is normal.The signal is operated in TTL level.The microprocessor inside the module monitors the module's operating voltage, temperature, transmitted optical power, received optical power, and laser bias current value in real time. The host acquires this information over a 2-wire serial bus.

After the module is powered on, the read value of the security level access registers 7BH ∼ 7EH of A2H is replaced with 0x00. After the content of this group of registers is updated, the read value is the last written value. The security level 1 password of this module is 0x00001011. The method to enter the security level 1 working state is to convert and write the security level 1 password in the A2H 7BH ∼ 7EH registers of the module, namely 0x00, 0x00, 0x10, 0x11. After entering the security level 1 working state, the user can directly write to the content of the A0H device address, or modify the content of the A2H 7FH table selection register to write to the contents of Table 00 or Table 01.And this version of the module does not support users to modify the security level 1 password.


## Optical Cable Details

| Parameter                     |   Min | Typ        |   Max | Unit   | Remarks                                            |
|-------------------------------|-------|------------|-------|--------|----------------------------------------------------|
| Jacket Material               |       | LSZH       |       |        |                                                    |
| Jacket Color                  |       | Aqua Green |       |        | We can provide according to the needs of customers |
| Flammability Rating           |       | OFN        |       |        | We can provide according to the needs of customers |
| Outer Diameter                |   2.8 | 3.0        |   3.2 | mm     |                                                    |
| Tensile Load(Short Term)      |       |            | 200   | N      |                                                    |
| Tensile Load(Long Term)       |       |            | 100   | N      |                                                    |
| Crush Resistance              |  10   |            |       | N/mm   | IEC 60794-1-21                                     |
| Impact Resistance             |   0.5 |            |       | N.m    | IEC 60794-1-21                                     |
| Flexing                       | 300   |            |       | Cycles | IEC 60794-1-21                                     |
| Twist Bend                    |       |            |       |        | IEC 60794-1-21                                     |
| Cable to SFP+ Plug Connection |       |            |  90   | N      |                                                    |
| Bend Radius(Short Term)       |  25   |            |       | mm     |                                                    |
| Bend Radius(Long Term)        |  30   |            |       | mm     |                                                    |


## Product Weight

The weight of AOC-SFP-10G-1M-C1C1C

：

53g/pcs

The weight of every mete of optical cable ：

6.4g/M

For example:the weight of AOC-SFP-10G-5M-C1C1C is:53 + （ 5-1 ） *6.4 = 78.6g

## Dimensions

![Image](/AOC/AOC-10-xM/AOC-10-xM_artifacts/image_000009_802577a0e1b6e2dc49e68f2bc6550c9319b417e5abc3afbac6b3744d2e5e6a3c.png)

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


## Electrical Pad Layout

![Image](/AOC/AOC-10-xM/AOC-10-xM_artifacts/image_000011_3f94da1874e81c6ba06f9757e59e21cbe2d78a7f877d2e5fafc1de5e6ef607fc.png)


## Pin Assignment

|   PIN # | Symbol     | Description                                                   |   Remarks |
|---------|------------|---------------------------------------------------------------|-----------|
|       1 | V EET      | Transmitter ground (common with receiver ground)              |         1 |
|       2 | TX_FAULT   | Transmitter Fault                                             |           |
|       3 | TX DISABLE | Transmitter Disable. Laser output disabled on high or open    |         2 |
|       4 | SDA        | 2-wire Serial Interface Data Line                             |         3 |
|       5 | SCL        | 2-wire Serial Interface Clock Line                            |         3 |
|       6 | MOD ABS    | Module Absent. Grounded within the module                     |         3 |
|       7 | RS0        | No connection required                                        |           |
|       8 | LOS        | Loss of Signal indication. Logic 0 indicates normal operation |         4 |
|       9 | RS1        | No connection required                                        |         1 |
|      10 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      11 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      12 | RD-        | Receiver Inverted DATA out. AC coupled                        |           |
|      13 | RD +       | Receiver Non-inverted DATA out. AC coupled                    |           |
|      14 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      15 | V CCR      | Receiver power supply                                         |           |
|      16 | V CCT      | Transmitter power supply                                      |           |
|      17 | V EET      | Transmitter ground (common with receiver ground)              |         1 |
|      18 | TD +       | Transmitter Non-Inverted DATA in. AC coupled                  |           |
|      19 | TD-        | Transmitter Inverted DATA in. AC coupled                      |           |
|      20 | V EET      | Transmitter ground (common with receiver ground)              |         1 |

## Notes:

1. Circuit ground is isolated from chassis ground
2. Disabled: TDIS &gt; 2V or open,Enabled: TDIS &lt; 0.8V
3. Should Be pulled up with 4.7k -10k ohm on host board to a voltage between 2V and 3.6V

4. LOS is open collector output

## References

- 1.IEEE standard 802.3ae. IEEE Standard Department,2005.

2.Enhanced 8.5 and 10 Gigabit Small Form Factor Pluggable Module ' SFP+ ' -SFF-8431.

3.Digital Diagnostics Monitoring Interface for Optical Transceivers -SFF-8472.