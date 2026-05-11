
## DATA SHEET

## MODULETEK:SFP-10G-T

10GBASE-T SFP Copper Transceiver 10 Gigabit Ethernet

## Overview

ModuleTek's  SFP-10G-T  is  a  small  hot-pluggable  RJ45  electrical  port  module,  compliant  with  10 Giga-bit  Ethernet  standards  and  SFP  Multi-Source  Agreement  (MSA)  standards,  supporting  10G transmission rate,transfer distances up to 30 meters using Cat 6a/7 network cable, it is also backward compatible with 10M/100M/1000M/2.5G/5GBase-T applications. Low power consumption (2.3W TYP @ 10Gbps 30m), compatible with various brands of hosts, widely used in data centers and enterprise networks. Comply with certification requirements such as RoHS 2.0, Reach, CE and FCC.

The product is based on a standard RJ45 interface, compatible with traditional networks, the Ethernet transfer rates can be increased without changing existing wiring. It is a lowcost alternative to Ethernet upgrades.

## Product Features

- Supports 10GBase-T using 30m Cat 6a/7 cable
- Supports 5GBase-T using 70m Cat 5e cable
- Supports 2.5GBase-T using 100m Cat 5e cable
- Supports 10/100/1000Base-T using 100m Cat 5e cable
- Low power consumption (2.3W TYP @10Gbps 30m)
- Auto-sense MDI/MDIX
- Compliant with IEEE 802.3az
- Compliant with SFF-8431 and SFF-8432 MSA
- Compliant with RoHS 2.0, Reach, CE, FCC standards

## Applications

10 Gigabit Ethernet

![Image](/SFP/SFP-10G-T /SFP-10G-T _artifacts/image_000001_e1ae9d2b844b16d334fe7b16f7be7e32a2b7b3d83634b5b38e0323e12d8441db.png)


## Ordering Information

| Part Number                                                                                                                                                                                 | Product ID                                                                                                                                                                                  | Description                                                                                                                                                                                 | Operating Temperature Range                                                                                                                                                                 |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SFP-10G-T                                                                                                                                                                                   | M551432                                                                                                                                                                                     | 10M/100M/1000M/2.5G/5G/10GBase-T SFP+ Copper RJ-45 Connector                                                                                                                                | 0 ◦ C to 70 ◦ C                                                                                                                                                                             |
| Note: 1. Rx with auto squelch. 2. Rx_LOS report copper interface link status. 3. A0 and A2 table 00/01 with wirite protection function. 4. Operating Temperature Range is case temperature. | Note: 1. Rx with auto squelch. 2. Rx_LOS report copper interface link status. 3. A0 and A2 table 00/01 with wirite protection function. 4. Operating Temperature Range is case temperature. | Note: 1. Rx with auto squelch. 2. Rx_LOS report copper interface link status. 3. A0 and A2 table 00/01 with wirite protection function. 4. Operating Temperature Range is case temperature. | Note: 1. Rx with auto squelch. 2. Rx_LOS report copper interface link status. 3. A0 and A2 table 00/01 with wirite protection function. 4. Operating Temperature Range is case temperature. |
| For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                                                   | For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                                                   | For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                                                   | For More Information: ModuleTek Limited Web: www.moduletek.com Email: sales@moduletek.com                                                                                                   |

## General Specifications

| Parameter           | Symbol   |    Min |   Typ | Max     | Unit   |   Remarks |
|---------------------|----------|--------|-------|---------|--------|-----------|
| Data Rate           | DR       |        |  10   |         | Gb/s   |         1 |
| Bit Error Rate      | BER      |        |       | 10 - 12 |        |           |
| Storage Temperature | T STO    | -40    |       | 85      | ◦ C    |         2 |
| Supply Current      | I CC     |        | 700   | 750     | mA     |         3 |
| Input Voltage       | V CC     |   3.14 |   3.3 | 3.46    | V      |           |
| Maximum Voltage     | V MAX    |  -0.5  |       | 4       | V      |           |
| Surge Current       | I surge  |        |       | 30      | mA     |           |

## Notes:

1.  IEEE 802.3ae
2.  Ambient temperature
3.  Test at 10Gbps rate using 30m CAT 6A cable


## I2C Memory Map

| Address A0   | Address A0   | Address A0                   | Address A0                                                  | Address A0                                      | Address A0   |
|--------------|--------------|------------------------------|-------------------------------------------------------------|-------------------------------------------------|--------------|
| IIC Addr     | Size         | Name                         | Description                                                 | Values (HEX)                                    | Remarks      |
| 0            | 1            | Identifier                   | SFP or SFP+                                                 | 03                                              |              |
| 1            | 1            | Ext. Identifier              | GBIC/SFP function is defined by two-wire interface ID only  | 04                                              |              |
| 2            | 1            | Connector                    | RJ45 (Registered Jack)                                      | 22                                              |              |
| 3-10         | 8            | Transceiver                  | Code for electronic or optical compatibility                | 00 00 00 00 00 04 00 00                         |              |
| 11           | 1            | Encoding                     | 64B/66B                                                     | 06                                              |              |
| 12           | 1            | BR, Nominal                  | Nominal Bit Rate 10.3Gb/s                                   | 67                                              |              |
| 13           | 1            | Rate Identifier              | Type of rate select functionality                           | 00                                              |              |
| 14           | 1            | Length(SMF,km)               | Link length supported for single mode fiber, units of km    | 00                                              |              |
| 15           | 1            | Length (SMF)                 | Link length supported for single mode fiber, units of 100 m | 00                                              |              |
| 16           | 1            | Length (50um)                | Link length supported for 50 um OM2 fiber, units of 10m     | 00                                              |              |
| 17           | 1            | Length (62.5um)              | Link length supported for 62.5 um OM1 fiber, units of 10m   | 00                                              |              |
| 18           | 1            | Length (OM4 or copper cable) | 30m                                                         | 1E                                              |              |
| 19           | 1            | Length (OM3)                 | Link length supported for 50 um OM3 fiber, units of 10m     | 00                                              |              |
| 20-35        | 16           | Vendor name                  | MODULETEK                                                   | 4D 4F 44 55 4C 45 54 45 4B 20 20 20 20 20 20 20 |              |
| 36           | 1            | Transceiver                  | Code for electronic or optical compatibility                | 00                                              |              |
| 37-39        | 3            | Vendor OUI                   | SFP vendor IEEE company ID                                  | 00 00 00                                        |              |
| 40-55        | 16           | Vendor PN                    | Part number in Order information                            | -                                               |              |
| 56-59        | 4            | Vendor rev                   | Revision level for part number provided by vendor (ASCII)   | -                                               |              |


| 60-61          | 2              | Wavelength                 | Laser wavelength (Passive/Active Cable Specification Compliance)                                   | 00 00                 |                |
|----------------|----------------|----------------------------|----------------------------------------------------------------------------------------------------|-----------------------|----------------|
| 62             | 1              | Unallocated                |                                                                                                    | 00                    |                |
| 63             | 1              | CC BASE                    | Check code for Base ID Fields (addresses 0 to 62)                                                  | -                     |                |
| 64-65          | 2              | Options                    | Indicates which optional transceiver signals are implemented                                       | 00 00                 |                |
| 66             | 1              | BR, max                    | Upper bit rate margin                                                                              | 00                    |                |
| 67             | 1              | BR, min                    | Lower bit rate margin                                                                              | 00                    |                |
| 68-83          | 16             | Vendor SN                  | Serial number provided by vendor                                                                   | Programmed by Factory |                |
| 84-91          | 8              | Date code                  | Year,Month,Day                                                                                     | Programmed by Factory |                |
| 92             | 1              | Diagnostic Monitoring Type | Indicates which type of diagnostic monitoring is implemented (if any) in the transceiver           | 00                    |                |
| 93             | 1              | Enhanced Options           | Indicates which optional enhanced features are implemented (if any) in the transceiver             | 00                    |                |
| 94             | 1              | SFF-8472 Compliance        | Indicates which revision of SFF-8472 the transceiver complies with.                                | 00                    |                |
| 95             | 1              | CC EXT                     | Check code for the Extended ID Fields (addresses 64 to 94)                                         | -                     |                |
| 96-127         | 32             | Vendor Specific            | Vendor Specific EEPROM                                                                             | -                     |                |
| 128-255        | 128            | Vendor Specific            | Vendor Specific EEPROM                                                                             | -                     |                |
| Address A2 Low | Address A2 Low | Address A2 Low             | Address A2 Low                                                                                     | Address A2 Low        | Address A2 Low |
| IIC Addr       | Size           | Name                       | Description                                                                                        | Values (HEX)          | Remarks        |
| 0-94           | 95             | Reserved                   | Reserved                                                                                           | FF                    |                |
| 95             | 1              | Checksum                   | 0-94 Byte Checksum                                                                                 | -                     |                |
| 96-121         | 26             | Reserved                   | Reserved                                                                                           | FF                    |                |
| 122            | 1              | Security Level             | Security Level ： 00=Normal Mode ； 01=User Mode （ Level 1 ） ； 02=Factory Mode （ Level 2 ） ； | -                     |                |
| 123-126        | 4              | Password Entry             | Password Entry Area                                                                                | 00 00 00 00           |                |


| 127                     | 1                       | Table Selection              | Page Select Byte                                                            | 00                      |                         |
|-------------------------|-------------------------|------------------------------|-----------------------------------------------------------------------------|-------------------------|-------------------------|
| Address A2 Page 00h/01h | Address A2 Page 00h/01h | Address A2 Page 00h/01h      | Address A2 Page 00h/01h                                                     | Address A2 Page 00h/01h | Address A2 Page 00h/01h |
| IIC Addr                | Size                    | Name                         | Description                                                                 | Values (HEX)            | Remarks                 |
| 128-255                 | 128                     | Upper Memory Map             | User Code Area                                                              | -                       |                         |
| Address A2 Page 8Ah     | Address A2 Page 8Ah     | Address A2 Page 8Ah          | Address A2 Page 8Ah                                                         | Address A2 Page 8Ah     | Address A2 Page 8Ah     |
| IIC Addr                | Size                    | Name                         | Description                                                                 | Values (HEX)            | Remarks                 |
| 128-131                 | 4                       | Firmware Version Number[4]   | Firmware Version Number                                                     | -                       |                         |
| 132-135                 | 4                       | Total Running Time In Second | Total Running Time In Second                                                | -                       |                         |
| Address A2 Page F0h     | Address A2 Page F0h     | Address A2 Page F0h          | Address A2 Page F0h                                                         | Address A2 Page F0h     | Address A2 Page F0h     |
| IIC Addr                | Size                    | Name                         | Description                                                                 | Values (HEX)            | Remarks                 |
| 128-131                 | 4                       | Password1 Long               | Level 1 Password                                                            | 00 00 10 11             |                         |
| 132                     | 1                       | WorkingMode                  | -                                                                           | 00                      |                         |
| 133                     | 1                       | DisableA0WP                  | 00=A0 With Write Protection ； 01=A0 Without Write Protection               | 00                      |                         |
| 134                     | 1                       | DisableA2T00T01WP            | 00=A2 T00T01 With Write Protection ； 01=A2 T00T01 Without Write Protection | 00                      |                         |
| 135                     | 1                       | DisableA2DomReport           | 00=ReprtoVCC/TEMP DOM ； 01=Not Report                                      | 00                      |                         |

## Notes ：

1.  Password entry area default 00000000 ， read out as last written value

2.  Module with write protection ， enter the security level 1 writeable

## User Mode

| Module    | Level 1 Default Password   | Password Can Be Changed   | Permissions                    |
|-----------|----------------------------|---------------------------|--------------------------------|
| SFP-10G-T | 00 00 10 11                | YES(A2 TF0)               | 1 、 Read And Write A0         |
| SFP-10G-T | 00 00 10 11                | YES(A2 TF0)               | 2 、 Read And Write A2 T00/T01 |

## Notes ：

1.detail in I2C memory map


## Dimensions

Weight: 26g

![Image](/SFP/SFP-10G-T /SFP-10G-T _artifacts/image_000007_70d273377f2fb7a6d753aee7ebff0963e02d9e4fe7ef49a5f930c99a28472774.png)

![Image](/SFP/SFP-10G-T /SFP-10G-T _artifacts/image_000008_e3a12b1ff801dbf4f17cb69d5fcad6a499331a8ccf238a0df68989a3e06d59cd.png)

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


duleTek

## Electrical Pad Layout

Top of Board

![Image](/SFP/SFP-10G-T /SFP-10G-T _artifacts/image_000010_a39c48a5f99ccb0b552539beefe9cb24adad300259e4fa79e5e374b58640205f.png)

Top

2

3

4

5

6

7

8

6

10

VEET

TX\_FAULT

TX DISABLE

SDA

SCL

MOD\_ABS

RSO

LOS

RS1

VEER

BottomofBoard

Bottom


## Pin Assignment

|   PIN # | Symbol     | Description                                                    |   Remarks |
|---------|------------|----------------------------------------------------------------|-----------|
|       1 | V EET      | Transmitter ground (common with receiver ground)               |         1 |
|       2 | TX_FAULT   | Transmitter Fault. Not supported                               |           |
|       3 | TX_DISABLE | Transmitter Disable. PHY disabled on high or open              |         2 |
|       4 | SDA        | 2-wire Serial Interface Data Line                              |         3 |
|       5 | SCL        | 2-wire Serial Interface Clock Line                             |         3 |
|       6 | MOD ABS    | Module Absent. Grounded within the module                      |         3 |
|       7 | RS0        | No Connection Required                                         |           |
|       8 | LOS        | Loss of Signal indication. Logic 0 indicates normal operation. |           |
|       9 | RS1        | No Connection Required                                         |           |
|      10 | V EER      | Receiver ground (common with transmitter ground)               |         1 |
|      11 | V EER      | Receiver ground (common with transmitter ground)               |         1 |
|      12 | RD-        | Receiver Inverted DATA out. AC coupled                         |           |
|      13 | RD +       | Receiver Non-inverted DATA out. AC coupled                     |           |
|      14 | V EER      | Receiver ground (common with receiver ground)                  |         1 |
|      15 | V CCR      | Receiver power supply                                          |           |
|      16 | V CCT      | Transmitter power supply                                       |           |
|      17 | V EET      | Transmitter ground (common with receiver ground)               |         1 |
|      18 | TD +       | Transmitter Non-Inverted DATA in. AC coupled                   |           |
|      19 | TD-        | Transmitter Inverted DATA in. AC coupled                       |           |
|      20 | V EET      | Transmitter ground (common with receiver ground)               |         1 |

## Notes:

1.Circuit ground is connected to chassis ground

2.Disabled: TDIS &gt; 2Vor open, Enabled: TDIS &lt; 0.8V

- 3.Should Be pulled up with 4.7k -10k ohm on host board to a voltage between 2V and 3.6V