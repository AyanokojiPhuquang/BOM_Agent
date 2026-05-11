
## DATA SHEET

## MODULETEK : DAC-SFP-25G-P-xxAWG-aa.aaM-C2C2B

SFP 25Gbps Passive Direct Attach Copper Cable Assembly

## Overview

ModuleTek's 25G passive cable uses shielded high-speed differential cables,compliant with 25G Ethernet IEEE802.3by standard and SFF-8402 standard, it supports 25G transmission rate and can be backward compatible with low-rate applications.The SFP 25G passive cable is the preferred solution for 25G rate short-distance applications. It is commonly used for data transmission between data centers and cabinets or adjacent cabinets,its biggest features are low cost, ultra low power consumption (less than 0.1 watt) and high reliability.

## Product Features

- Up to 25Gb/s bi-directional data links
- Compliant with SFF-8402
- Hot-pluggable
- AC coupled inputs and outputs
- 100 Ohm differential impedance
- Enhanced EMI design
- Single power supply 3.3V
- RoHS Compliant
- Operating temperature range: 0 ◦ C to 70 ◦ C

## Applications

25GBASE Ethernet

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000001_aae51b7c331f0bbca17b829443efc170a1f2680e017fce83f0f9ae33a5d857ee.png)


## Ordering Information

| Part Number                       | Product ID   | Description                                                          | Gauge   | Length   |
|-----------------------------------|--------------|----------------------------------------------------------------------|---------|----------|
| DAC-SFP-25G-P- 30AWG-aa.aaM-C2C2B | M265803      | SFP 25G Passive Direct Attach Copper Black Cable Assembly, aa.aa ≤ 3 | 30AWG   | ≤ 3m     |
| DAC-SFP-25G-P- 28AWG-aa.aaM-C2C2B | M405803      | SFP 25G Passive Direct Attach Copper Black Cable Assembly, aa.aa ≤ 3 | 28AWG   | ≤ 3m     |
| DAC-SFP-25G-P- 26AWG-aa.aaM-C2C2B | M044503      | SFP 25G Passive Direct Attach Copper Black Cable Assembly, aa.aa ≤ 5 | 26AWG   | ≤ 5m     |

## Note:

1. 'P' indicates passive cable
2. 'aa.aa' indicates the cable length in meters.
3. The product with write protection.
4. The wire diameter of the products in the above list is the default value under different lengths. We can also provide other wire products to customers with special requirements.
5. Product ID is the short order number of our product standard model.

## For More Information:

ModuleTek Limited

Web: www.moduletek.com

Email: sales@moduletek.com


## General Specifications

| Parameter             | Symbol   |    Min |   Typ | Max     | Unit   |   Remarks |
|-----------------------|----------|--------|-------|---------|--------|-----------|
| Data Rate             | DR       |        |  25   |         | Gb/s   |         1 |
| Bit Error Rate        | BER      |        |       | 10 - 12 |        |           |
| Operating Temperature | T C      |   0    |       | 70      | ◦ C    |         2 |
| Storage Temperature   | T STO    | -40    |       | 85      | ◦ C    |         3 |
| Supply Current        | I CC     |        |       | 4       | mA     |         4 |
| Input Voltage         | V CC     |   3.14 |   3.3 | 3.46    | V      |         4 |

## Notes:

- 1.IEEE 802.3by
- 2.Case temperature
- 3.Ambient temperature
- 4.For electrical power interface

## I2C Memory Map

| Address A0   | Address A0   | Address A0      | Address A0                                                  | Address A0              | Address A0   |
|--------------|--------------|-----------------|-------------------------------------------------------------|-------------------------|--------------|
| IIC Addr     | Size         | Name            | Description                                                 | Values (HEX)            | Remarks      |
| 0            | 1            | Identifier      | SFP or SFP+                                                 | 03                      |              |
| 1            | 1            | Ext. Identifier | GBIC/SFP function is defined by two-wire interface ID only  | 04                      |              |
| 2            | 1            | Connector       | Copper pigtail                                              | 21                      |              |
| 3-10         | 8            | Transceiver     | Passive Cable                                               | 00 00 00 00 00 04 00 00 |              |
| 11           | 1            | Encoding        | Code for high speed serial encoding algorithm               | 00                      |              |
| 12           | 1            | BR, Nominal     | Nominal Bit Rate 25.5GB/s                                   | FF                      |              |
| 13           | 1            | Rate Identifier | Type of rate select functionality                           | 00                      |              |
| 14           | 1            | Length(SMF,km)  | Link length supported for single mode fiber, units of km    | 00                      |              |
| 15           | 1            | Length (SMF)    | Link length supported for single mode fiber, units of 100 m | 00                      |              |
| 16           | 1            | Length (50um)   | Link length supported for 50 um OM2 fiber, units of 10 m    | 00                      |              |


| 17    |   1 | Length (62.5um)              | Link length supported for 62.5 um OM1 fiber, units of 10 m                                                      | 00                                              |
|-------|-----|------------------------------|-----------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| 18    |   1 | Length (OM4 or copper cable) | Link length supported for 50um OM4 fiber, units of 10m. Alternatively copper or direct attach cable, units of m | 01                                              |
| 19    |   1 | Length (OM3)                 | Link length supported for 50 um OM3 fiber, units of 10 m                                                        | 00                                              |
| 20-35 |  16 | Vendor name                  | MODULETEK                                                                                                       | 4D 4F 44 55 4C 45 54 45 4B 20 20 20 20 20 20 20 |
| 36    |   1 | Transceiver                  | Code for electro nic or optical compatibility                                                                   | 0D                                              |
| 37-39 |   3 | Vendor OUI                   | SFP vendor IEEE company ID                                                                                      | 00 00 00                                        |
| 40-55 |  16 | Vendor PN                    | Part number in Order information                                                                                | -                                               |
| 56-59 |   4 | Vendor rev                   | Revision level for part number provided by vendor (ASCII)                                                       | -                                               |
| 60-61 |   2 | Wavelength                   | Laser wavelength (Passive/Active Cable Specification Compliance)                                                | 00 00                                           |
| 62    |   1 | Unallocated                  |                                                                                                                 | 00                                              |
| 63    |   1 | CC BASE                      | Check code for Base ID Fields (addresses 0 to 62)                                                               | -                                               |
| 64-65 |   2 | Options                      | Indicates which optional transceiver signals are implemented                                                    | 00 00                                           |
| 66    |   1 | BR, max                      | Upper bit rate margin                                                                                           | 64                                              |
| 67    |   1 | BR, min                      | Lower bit rate margin                                                                                           | 00                                              |
| 68-83 |  16 | Vendor SN                    | Serial number provided by vendor                                                                                | Programmed by Factory                           |
| 84-91 |   8 | Date code                    | Year,Month,Day                                                                                                  | Programmed by Factory                           |
| 92    |   1 | Diagnostic Monitoring Type   | Indicates which type of diagnostic monitoring is implemented (if any) in the transceiver                        | 00                                              |


| 93                      | 1                       | Enhanced Options             | Indicates which optional enhanced features are implemented (if any) in the transceiver             | 00                      |                         |
|-------------------------|-------------------------|------------------------------|----------------------------------------------------------------------------------------------------|-------------------------|-------------------------|
| 94                      | 1                       | SFF-8472 Compliance          | Indicates which revision of SFF-8472 the transceiver complies with.                                | 00                      |                         |
| 95                      | 1                       | CC EXT                       | Check code for the Extended ID Fields (addresses 64 to 94)                                         | -                       |                         |
| 96-127                  | 32                      | Vendor Specific              | Vendor Specific EEPROM                                                                             | -                       |                         |
| 128-255                 | 128                     | Vendor Specific              | Vendor Specific EEPROM                                                                             | -                       |                         |
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


|   132 |   1 | DisableA0WP       | 00=A0 With Write Protection ； 01=A0 Without Write Protection               |   00 |
|-------|-----|-------------------|-----------------------------------------------------------------------------|------|
|   133 |   1 | DisableA2T00T01WP | 00=A2 T00T01 With Write Protection ； 01=A2 T00T01 Without Write Protection |   00 |

## Notes ：

- 1.Password entry area default 00000000 ， read out as last written value

2.Module with write protection ， enter the security level 1 writeable

## User Mode

| Level 1 Default Password   | Password Can Be Changed   | Permissions                          |
|----------------------------|---------------------------|--------------------------------------|
| 00 00 10 11                | YES(A2 TF0)               | 1 、 Read And Write A0 、 A2 T00/T01 |
| 00 00 10 11                | YES(A2 TF0)               | 2 、 Read A2 T8A                     |
| 00 00 10 11                | YES(A2 TF0)               | 3 、 Read And Write A2 TF0           |

## Cable Specifications

| Parameter       | Symbol   |   Min |   Typ |   Max | Unit   | Remarks   |
|-----------------|----------|-------|-------|-------|--------|-----------|
| Wire Gauge      |          |    30 |       |    26 | AWG    |           |
| Cable Impedance | Z        |    90 |   100 |   110 | Ohm    |           |

## Insertion Loss Level

| Part Number              | Insertion loss level   |
|--------------------------|------------------------|
| DAC-SFP-25G-P-30AWG-1M   | CA-25G-N               |
| DAC-SFP-25G-P-30AWG-2M   | CA-25G-N               |
| DAC-SFP-25G-P-30AWG-2.5M | CA-25G-N               |
| DAC-SFP-25G-P-30AWG-3M   | CA-25G-S               |
| DAC-SFP-25G-P-28AWG-3M   | CA-25G-N               |
| DAC-SFP-25G-P-26AWG-5M   | CA-25G-L               |

## Note:

1. Cable insertion loss classification standard ： IEEE 802.3by 110-10


## Block Diagram of Transceiver

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000008_78013e97389e0934485230f004d6055fc3debfbd0155b8aef488ccb4939b54c8.png)


## Typical S parameter

## 1m 30AWG typical insertion loss curve

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000010_c7973269501a0dfc589a308a263b57ad1b8c54d43406fb3006e748f9af72ca1d.png)

## 1m 30AWG typical reflection curve

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000011_e00974f879c4db62d8ea2d3ac5a288e3267546fcd542b61ee0aed2bdee67f298.png)


duleTek

Moc

## 3m 28AWG typical insertion loss curve

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000013_6cfe71ff613ec1e828f7567f20b0d1935f44c72c72b0686d65880be250b95e26.png)

## 3 m 28AWG typical reflection curve

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000014_5205fbd74726940c39d759ac8c9bf16e8a4e5afa94b212760ffdb1bcf270d396.png)


duleTek

Moc

## 5m 26AWG typical insertion loss curve

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000016_f26011f597035366f0c4475c709e817161a503338785f51699ddffcb0533cf94.png)

## 5m 26AWG typical reflection curve

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000017_7c1181b8fe3c4015f9426ca62e44ec68249d483093e4756f081872922158bdf6.png)

## Notes:

1. Insertion loss standard reference IEEE802.3bj 92.10.2 ： IL&lt;22.48dB@12.89 GHz
2. Reflection curve standard reference IEEE802.3bj 92.10.3 ： SDDxx(dB)=16.5 - 2 × SQRT(f), 0.05 ≤ f &lt; 4.1GHz.
3. Reflection curve standard reference IEEE802.3bj 92.10.3 ： SDDxx(dB)=10.66 - 14 × log10(f/5.5),
4. 4.1 ≤ f ≤ 19GHz.


## Weight

| Parameter            | Symbol   |   Typ | Unit   |   Remarks |
|----------------------|----------|-------|--------|-----------|
| 30AWG Product Weight | G D30    |  78   | g/PCS  |         1 |
| 28AWG Product Weight | G D28    |  84   | g/PCS  |         1 |
| 26AWG Product Weight | G D26    |  90   | g/PCS  |         1 |
| 30AWG Cable Weight   | G C30    |  32   | g/M    |           |
| 28AWG Cable Weight   | G C28    |  38   | g/M    |           |
| 26AWG Cable Weight   | G C26    |  44   | g/M    |           |
| Dust Cap Weight      | G S      |   0.8 | g/PCS  |           |

## Notes ：

- 1.The weight of DAC-SFP-25G-P-xxAWG-1M-C2C2B.For example:the weight of DAC-SFP-25G-P-26AWG-5M-C2C2B is:90+44*(5-1)+0.80*2=267.6g

## Dimensions

未注尺⼨公差 ±0.2mm 单位：毫⽶

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000019_32bf99f1092b6dc624a936c750474152444f39991dc18dbf187ec1511f2a8df7.png)

## Cable Dimension

|   Serial number |   Standard Wire Gauge AWG |   Cable diameter OD (mm) |   Minimum bending radius R (mm) |
|-----------------|---------------------------|--------------------------|---------------------------------|
|               1 |                        30 |                      4.6 |                              26 |
|               2 |                        28 |                      5   |                              28 |
|               3 |                        26 |                      5.6 |                              30 |


## Length Tolerance

|   Serial number | Nominal length (m)   |   Tolerance range ±(cm) |
|-----------------|----------------------|-------------------------|
|               1 | Length ≤ 2           |                       2 |
|               2 | 2 < Length ≤ 4       |                       4 |
|               3 | 4 < Length ≤ 5       |                       6 |

## Electrical Pad Layout

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000021_f28d2107ae8eeecdeb4bf038bed17d69db703883d0c58686bd934103241705b1.png)

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000022_385732bce2ad32e23675cac0e7e7e8fabded19581842db6edd19b3dc104bec87.png)

![Image](/DAC/DAC-25-xM/DAC-25-xM_artifacts/image_000023_1627ac77355c9df43f3c991eee5e5b71ce6b87d58c6bb92b7c4c6c3e811b2c12.png)


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
|      12 | RD-        | Receiver Inverted DATA out. AC coupled                                         |           |
|      13 | RD+        | Receiver Non-inverted DATA out. AC coupled                                     |           |
|      14 | V EER      | Receiver ground (common with transmitter ground)                               |         1 |
|      15 | V CCR      | Receiver power supply                                                          |           |
|      16 | V CCT      | Transmitter power supply                                                       |           |
|      17 | V EET      | Transmitter ground (common with receiver ground)                               |         1 |
|      18 | TD+        | Transmitter Non-Inverted DATA in. AC coupled                                   |           |
|      19 | TD-        | Transmitter Inverted DATA in. AC coupled                                       |           |
|      20 | V EET      | Transmitter ground (common with receiver ground)                               |         1 |

## Notes:

1. Circuit ground is isolated from chassis ground
2. Should Be pulled up with 4.7k - 10k ohm on host board to a voltage between 2V and 3.6V

## References

1. IEEE standard 802.3by. IEEE Standard Department.
2. IEEE standard 802.3bj. IEEE Standard Department.