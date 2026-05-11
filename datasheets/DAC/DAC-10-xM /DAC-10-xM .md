
## DATA SHEET

## MODULETEK : DAC-SFP-10G-P-xxAWG-aa.aaM-C2C2B

SFP 10G Passive Direct Attach Copper Cable Assembly

## Overview

ModuleTek's 10G passive cable uses shielded high-speed differential cables,compliant with 10 Gigabit Ethernet standards and SFP Multi-Source Agreement (MSA) standards, supports 10G transmission rates, and is backward compatible with 1G rates.SFP 10G passive cable is the preferred solution for short-distance applications. It is widely used for data transmission between data centers and cabinets or adjacent cabinets.  Its biggest feature is low cost, ultra-low power consumption (less than 0.1 watt) and high reliability.

## Product Features

- Up to 10 Gb/s bi-directional data links

- Compliant with 10GFC

- Compliant with SFF-8431

- AC coupled inputs and outputs

- 100 Ohm differential impedance

- Enhanced EMI design

- Single power supply 3.3V

- RoHS Compliant

- Operating temperature range: 0 ◦ C to 70 ◦ C

## Applications

10G Ethernet 10G Fiber Channel

Serial Data Transmission

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000001_e236d8cd0b74fffd6f55c32d865553ec6200e2721cbd2eef311bbfe4e9e7148f.png)


## Ordering Information

| Part Number                        | Product ID   | Description                                                                    | Gauge   | Length   |
|------------------------------------|--------------|--------------------------------------------------------------------------------|---------|----------|
| DAC-SFP-10G-P- 30AWG-aa.aaM- C2C2B | M600806      | SFP 10G Passive Direct Attach Copper Black Cable Assembly,with MCU, aa.aa ≤ 3  | 30AWG   | ≤ 3m     |
| DAC-SFP-10G-P- 28AWG-aa.aaM- C2C2B | M600827      | SFP 10G Passive Direct Attach Copper Black Cable Assembly,with MCU, aa.aa < 5  | 28AWG   | < 5m     |
| DAC-SFP-10G-P- 24AWG-aa.aaM- C2C2B | M600805      | SFP 10G Passive Direct Attach Copper Black Cable Assembly,with MCU, aa.aa ≤ 10 | 24AWG   | ≤ 15sm   |

## Note:

1. 'P' indicates passive cable.
2. 'aa.aa' indicates the cable length in meters.
3. The product has write protection.
4. The wire diameter of the products in the above list is the default value under different lengths. We can also provide other wire products to customers with special requirements.
5. Product ID is the short order number of our product standard model.

## For More Information:

ModuleTek Limited

Web: www.moduletek.com

Email: sales@moduletek.com


## General Specifications

| Parameter             | Symbol   |    Min |     Typ | Max     | Unit   |   Remarks |
|-----------------------|----------|--------|---------|---------|--------|-----------|
| Data Rate             | DR       |        | 10.3125 |         | Gb/s   |         1 |
| Bit Error Rate        | BER      |        |         | 10 - 12 |        |           |
| Operating Temperature | T C      |   0    |         | 70      | ◦ C    |         2 |
| Storage Temperature   | T STO    | -40    |         | 85      | ◦ C    |         3 |
| Input Voltage         | V CC     |   3.14 |  3.3    | 3.46    | V      |         4 |

## Notes:

1. IEEE 802.3ae
2.  Case temperature
3. Ambient temperature
4. For electrical power interface

## I2C Memory Map

| Address A0   | Address A0   | Address A0      | Address A0                                                 | Address A0              | Address A0   |
|--------------|--------------|-----------------|------------------------------------------------------------|-------------------------|--------------|
| IIC Addr     | Size         | Name            | Description                                                | Values (HEX)            | Remarks      |
| 0            | 1            | Identifier      | SFP or SFP+                                                | 03                      |              |
| 1            | 1            | Ext. Identifier | GBIC/SFP function is defined by two-wire interface ID only | 04                      |              |
| 2            | 1            | Connector       | Copper pigtail                                             | 21                      |              |
| 3-10         | 8            | Transceiver     | Passive Cable                                              | 00 00 00 00 00 04 00 00 |              |
| 11           | 1            | Encoding        | Code for high speed serial encoding algorithm              | 00                      |              |
| 12           | 1            | BR, Nominal     | Nominal Bit Rate 10.3Gb/s                                  | 67                      |              |
| 13           | 1            | Rate Identifier | Type of rate select functionality                          | 00                      |              |
| 14           | 1            | Length(SMF,km)  | Link length supported for single modefiber, units of km    | 00                      |              |
| 15           | 1            | Length (SMF)    | Link length supported for single modefiber, units of 100 m | 00                      |              |
| 16           | 1            | Length (50um)   | Link length supported for 50 um OM2 fiber, units of10m     | 00                      |              |
| 17           | 1            | Length (62.5um) | Link length supported for 62.5 umOM1fiber, units of 10m    | 00                      |              |


| 18    |   1 | Length (OM4or copper cable)   | Link length supported for 50um OM4 fiber, units of 10m. Alternatively copper or direct attach cable, units of m   | 01                                              |
|-------|-----|-------------------------------|-------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| 19    |   1 | Length (OM3)                  | Link length supported for 50 um OM3 fiber, units of10m                                                            | 00                                              |
| 20-35 |  16 | Vendor name                   | MODULETEK                                                                                                         | 4D 4F 44 55 4C 45 54 45 4B 20 20 20 20 20 20 20 |
| 36    |   1 | Transceiver                   | Code for electro nic or optical compatibility                                                                     | 0D                                              |
| 37-39 |   3 | Vendor OUI                    | SFPvendor IEEE company ID                                                                                         | 00 00 00                                        |
| 40-55 |  16 | Vendor PN                     | Part number in Order information                                                                                  | -                                               |
| 56-59 |   4 | Vendor rev                    | Revision level for part number provided by vendor (ASCII)                                                         | -                                               |
| 60-61 |   2 | Wavelength                    | Laser wavelength (Passive/Active Cable Specification Compliance)                                                  | 00 00                                           |
| 62    |   1 | Unallocated                   |                                                                                                                   | 00                                              |
| 63    |   1 | CC BASE                       | Check code for Base ID Fields (addresses 0 to 62)                                                                 | -                                               |
| 64-65 |   2 | Options                       | Indicates which optional transceiver signals are implemented                                                      | 00 00                                           |
| 66    |   1 | BR, max                       | Upper bit rate margin                                                                                             | 64                                              |
| 67    |   1 | BR, min                       | Lower bit rate margin                                                                                             | 00                                              |
| 68-83 |  16 | Vendor SN                     | Serial number provided by vendor                                                                                  | Programmed by Factory                           |
| 84-91 |   8 | Date code                     | Year,Month,Day                                                                                                    | Programmed by Factory                           |
| 92    |   1 | Diagnostic Monitoring Type    | Indicates which type of diagnostic monitoring is implemented (if any) in the transceiver                          | 00                                              |
| 93    |   1 | Enhanced Options              | Indicates which optional enhanced features are implemented (if any) in the transceiver                            | 00                                              |


| 94                      | 1                       | SFF-8472 Compliance          | Indicates which revision of SFF-8472 the transceiver complies with.                                | 00                      |                         |
|-------------------------|-------------------------|------------------------------|----------------------------------------------------------------------------------------------------|-------------------------|-------------------------|
| 95                      | 1                       | CC EXT                       | Check code for the Extended ID Fields (addresses 64 to 94)                                         | -                       |                         |
| 96-127                  | 32                      | Vendor Specific              | Vendor SpecificEEPROM                                                                              | -                       |                         |
| 128-255                 | 128                     | Vendor Specific              | Vendor SpecificEEPROM                                                                              | -                       |                         |
| Address A2 Low          | Address A2 Low          | Address A2 Low               | Address A2 Low                                                                                     | Address A2 Low          | Address A2 Low          |
| IIC Addr                | Size                    | Name                         | Description                                                                                        | Values (HEX)            | Remarks                 |
| 0-94                    | 95                      | Reserved                     | Reserved                                                                                           | FF                      |                         |
| 95                      | 1                       | Checksum                     | 0-94 Byte Checksum                                                                                 | -                       |                         |
| 96-121                  | 26                      | Reserved                     | Reserved                                                                                           | 00                      |                         |
| 122                     | 1                       | Security Level               | Security Level ： 00=Normal Mode ； 01=User Mode （ Level 1 ） ； 02=Factory Mode （ Level 2 ） ； | 00                      |                         |
| 123-126                 | 4                       | Password Entry               | Password Entry Area                                                                                | 00 00 00 00             |                         |
| 127                     | 1                       | Table Selection              | Page Select Byte                                                                                   | 00                      |                         |
| Address A2 Page 00h/01h | Address A2 Page 00h/01h | Address A2 Page 00h/01h      | Address A2 Page 00h/01h                                                                            | Address A2 Page 00h/01h | Address A2 Page 00h/01h |
| IIC Addr                | Size                    | Name                         | Description                                                                                        | Values (HEX)            | Remarks                 |
| 128-255                 | 128                     | Upper Memory Map             | User Code Area                                                                                     | FF                      |                         |
| Address A2 Page 8Ah     | Address A2 Page 8Ah     | Address A2 Page 8Ah          | Address A2 Page 8Ah                                                                                | Address A2 Page 8Ah     | Address A2 Page 8Ah     |
| IIC Addr                | Size                    | Name                         | Description                                                                                        | Values (HEX)            | Remarks                 |
| 128-131                 | 4                       | Firmware Version Number[4]   | Firmware Version Number                                                                            | -                       |                         |
| 132-135                 | 4                       | Total Running Time In Second | Total Running Time In Second                                                                       | -                       |                         |
| Address A2 Page F0h     | Address A2 Page F0h     | Address A2 Page F0h          | Address A2 Page F0h                                                                                | Address A2 Page F0h     | Address A2 Page F0h     |
| IIC Addr                | Size                    | Name                         | Description                                                                                        | Values (HEX)            | Remarks                 |
| 128-131                 | 4                       | Password1 Long               | Level 1 Password                                                                                   | 00 00 10 11             |                         |
| 132                     | 1                       | DisableA0WP                  | 00=A0 With Write Protection ； 01=A0 Without Write Protection                                      | 00                      |                         |


duleTek

| 133   | 1   | DisableA2T00T01WP   | 00=A2 T00T01 With Write Protection ； 01=A2 T00T01 Without Write Protection   | 00   |
|-------|-----|---------------------|-------------------------------------------------------------------------------|------|

## Notes ：

1.  Password entry area default 00000000 ， read out as last written value
2.  Module with write protection ， enter the security level 1 writeable

## User Mode

| Level 1 Default Password   | PasswordCanBe Changed   | Permissions                          |
|----------------------------|-------------------------|--------------------------------------|
| 00 00 10 11                | YES(A2 TF0)             | 1 、 Read And Write A0 、 A2 T00/T01 |
| 00 00 10 11                | YES(A2 TF0)             | 2 、 Read A2 T8A                     |
| 00 00 10 11                | YES(A2 TF0)             | 3 、 Read And Write A2 TF0           |

## Block Diagram of Transceiver

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000007_627ca63dd26b3894caa4f2b7ee99071d83442379db7e0e37121254189a788817.png)


## Typical S parameter

## 3m 30AWG typical insertion loss curve

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000009_0244a82635be59269041bb5d3e6e73df4286c7ac86d96c4599bbc8a9dcb1f786.png)

## 3m 30AWG typical reflection curve

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000010_36aaa98610b63005c9d9ddbdea86bc52486ba7fb9f6d55f98c01f0be06b4b3f3.png)


duleTek

## 5m 24AWG typical insertion loss curve

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000012_e72aa1f96f67edbd826e15c6d5873b797780ed72598af9a4c76f384506412348.png)

## 5m 24AWG typical reflection curve

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000013_de7defc1091be578857d4c2025f33055bd8b7810c868ab733ef4df394e8f0e4c.png)

## Note:

1. Insertion loss standard reference IEEE802.3ba 85.10.2 ： IL&lt;17.04dB@5.15625 GHz
2. Reflection curve standard reference IEEE802.3ba 85.10.4 ： SDDxx(dB)=12 - 2 × SQRT(f), 0.05 ≤ f &lt; 4.1GHz.
3. Reflection curve standard reference IEEE802.3ba 85.10.4 ： SDDxx(dB)=6.3 - 13 × log10(f/5.5), 4.1 ≤ f ≤ 10GHz.


## Weight

| Parameter            | Symbol   |   Typ | Unit   |   Remarks |
|----------------------|----------|-------|--------|-----------|
| 30AWG Product Weight | G D30    |  72   | g/PCS  |         1 |
| 28AWG Product Weight | G D28    |  88   | g/PCS  |         1 |
| 24AWG Product Weight | G D28    |  96   | g/PCS  |         1 |
| 30AWGCable Weight    | G C30    |  26   | g/M    |           |
| 28AWGCable Weight    | G C28    |  42   | g/M    |           |
| 24AWGCable Weight    | G C26    |  50   | g/M    |           |
| Dust Cap Weight      | G S      |   0.8 | g/PCS  |           |

## Notes ：

1.  The weight of DAC-SFP-10G-P-xxAWG-1M-C2C2B.For example:the weight of DAC-SFP-10G-P-24AWG-6M-C2C2B is:96+50*(6-1)+0.80*2=347.6g

## Dimensions

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000015_5f198b31144b2f4f53091be3955ed26903b8dcacf75d0e53258e55eec93ba7c3.png)

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


## Cable Specifications

| Parameter       | Symbol   |   Min |   Typ |   Max | Unit   | Remarks   |
|-----------------|----------|-------|-------|-------|--------|-----------|
| Wire Gauge      |          |    30 |       |    24 | AWG    |           |
| Cable Impedance | Z        |    90 |   100 |   110 | Ohm    |           |

## Cable Dimension

|   serial number |   Standard Wire Gauge AWG |   Cable diameterOD(mm) |   Minimum bending radius R (mm) |
|-----------------|---------------------------|------------------------|---------------------------------|
|               1 |                        30 |                    4.2 |                              25 |
|               2 |                        28 |                    4.7 |                              26 |
|               3 |                        24 |                    6   |                              28 |

## Length Tolerance

|   Serial number | Nominal length (m)   |   Tolerance range ±(cm) |
|-----------------|----------------------|-------------------------|
|               1 | Length ≤ 2           |                       2 |
|               2 | 2 < Length ≤ 4       |                       4 |
|               3 | 4 < Length ≤ 6       |                       6 |
|               4 | 6 < Length           |                       8 |


## Electrical Pad Layout

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000018_640c8ec157460cf5b41a7598f79fb8ab2fe314764deceae51121fce0c3623e64.png)

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000019_fbddc312ff372e300836a77f2bcf6f4da763244febce628f3f4c0b235b3072da.png)

![Image](/DAC/DAC-10-xM /DAC-10-xM _artifacts/image_000020_5c8564452fd1ca148c3637ca44c72d4c4bd4e23dbeff478a4434bd854c277c32.png)


## Pin Assignment

|   PIN # | Symbol     | Description                                                                    |   Remarks |
|---------|------------|--------------------------------------------------------------------------------|-----------|
|       1 | V EET      | Transmitter ground (common with receiver ground)                               |         1 |
|       2 | TX_FAULT   | Transmitter failure alarm, not used                                            |           |
|       3 | TX_DISABLE | The signal turns off the module transmitter when it is high or open, not used. |           |
|       4 | SDA        | Data line for serial ID                                                        |         2 |
|       5 | SCL        | Clock line for serial ID                                                       |         2 |
|       6 | MOD_ABS    | Module Absent. Grounded within the module                                      |         2 |
|       7 | RS0        | No connection required                                                         |           |
|       8 | LOS        | Loss of Signal indication. Logic 0 indicates normal operation                  |           |
|       9 | RS1        | No connection required                                                         |           |
|      10 | V EER      | Receiver ground (common with transmitter ground)                               |         1 |
|      11 | V EER      | Receiver ground (common with transmitter ground)                               |         1 |
|      12 | RD-        | Receiver Inverted DATAout. ACcoupled                                           |           |
|      13 | RD+        | Receiver Non-inverted DATAout. ACcoupled                                       |           |
|      14 | V EER      | Receiver ground (common with transmitter ground)                               |         1 |
|      15 | V CCR      | Receiver power supply                                                          |           |
|      16 | V CCT      | Transmitter power supply                                                       |           |
|      17 | V EET      | Transmitter ground (common with receiver ground)                               |         1 |
|      18 | TD+        | Transmitter Non-Inverted DATA in. AC coupled                                   |           |
|      19 | TD-        | Transmitter Inverted DATAin. ACcoupled                                         |           |
|      20 | V EET      | Transmitter ground (common with receiver ground)                               |         1 |

## Notes:

1. Circuit ground is isolated from chassis ground
2. Should Be pulled up with 4.7k - 10k ohm on host board to a voltage between 2V and 3.6V

## References

1. IEEE standard 802.3ae. IEEE Standard Department, 2005.
2. IEEE standard 802.3ba. IEEE Standard Department.