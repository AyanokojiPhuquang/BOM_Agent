
## DATA SHEET

## MODULETEK: SFP-GE-T

1000BASE-T SFP (Small Form Pluggable) Copper Transceiver 1.25 Gigabit Ethernet

## Overview

ModuleTek's SFP-GE-T is a small, hot-swappable RJ45 electrical port module, compliant with Gigabit Ethernet standards and SFP Multi-Source Agreement (MSA) standards,supporting 10M/100M/ 1000M transmission rate. CAT5 class network cable transmission distance of up to 100 meters, good electromagnetic compatibility, compatible with various brands of hosts, widely used in data centers and enterprise networks. Access to the PHY chip registers is via the I2C interface. It supports 1000BASE-X auto-negotiation, supports the LINK status via the RX\_LOS pin, and supports hosts with SGMII functionality. Meet the certification requirements such as RoHS.

## Product Features

- Up to 1.25Gb/s bi-directional data links
- Compliant with IEEE Std 802.3, 802.3z, IEEE 802.3u, IEEE 802.3ab
- Compliant with SFP MSA
- Hot-pluggable SFP footprint
- Support 10/100/1000BASE-T operation in host systems with SGMII interface
- RJ-45 connector
- Auto-sense MDI/MDIX
- Single power supply 3.3V
- RoHS Compliant

## Applications

1.25 Gigabit Ethernet

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000001_956fc840c89787852e50ec154dffe3f89aaadec4f37ca4dfd63ef66113954f33.png)


## Ordering Information

| Part Number   | Product ID   | Description                                                              | Operating Temperature Range   |
|---------------|--------------|--------------------------------------------------------------------------|-------------------------------|
| SFP-GE-T      | M225105      | 1000BASE-T SFP Copper RJ-45 Connector 100m Auto Negotiation default mode | 0 ○ C to 70 ○ C               |
| SFP-GE-T-I    | M225108      | 1000BASE-T SFP Copper RJ-45 Connector 100m Auto Negotiation default mode | -40 ○ C to 85 ○ C             |

## Notes:

1.  The product with write protection
2.  Module based on Marvell 88E1112 development
3.  Operating Temperature Range is case temperature
4.  The product is Master mode
5.  The product enables RX\_LOS function,which can be turned on or off according to customer needs
6.  The product does not implement receiver suppression
7.  Product ID is the short order number of our product standard model

## For More Information:

ModuleTek Limited

Web: www.moduletek.com

Email: sales@moduletek.com


## General Specifications

| Parameter           | Symbol   |    Min |    Typ | Max     | Unit   |   Remarks |
|---------------------|----------|--------|--------|---------|--------|-----------|
| Data Rate           | DR       |  10    |        | 1000    | Mb/sec |         1 |
| Cable Length        | CL       |        |        | 100     | m      |         2 |
| Bit Error Rate      | BER      |        |        | 10 - 12 |        |           |
| Storage Temperature | T STO    | -40    |        | 85      | ○ C    |         3 |
| Supply Current      | I CC     |        | 370    | 420     | mA     |           |
| Input Voltage       | V CC     |   3.15 |   3.3  | 3.45    | V      |           |
| Maximum Voltage     | V MAX    |        |        | 4       | V      |           |
| Power Consumption   | P        |        |   1.22 | 1.38    | W      |           |

## Notes:

1.  IEEE 802.3 compatible
2.  Category 5 UTP
3.  Ambient temperature

## High Speed Electrical Interface Host-SFP

| Parameter                     | Symbol   |   Min |   Typ |   Max | Unit   |   Remarks |
|-------------------------------|----------|-------|-------|-------|--------|-----------|
| Single ended Input swing      | V IN PP  |   250 |       |  1200 | mV     |           |
| Single ended output swing     | V OUT PP |   275 |       |   800 | mV     |           |
| Rise Time /Fall Time(20%-80%) | t r /t f |       |   175 |       | ps     |           |
| Tx Input impedance            | Z IN     |       |    50 |       | ohm    |         1 |
| Rx Output impedance           | Z OUT    |       |    50 |       | ohm    |         1 |

## Notes:

1. Single ended


## High Speed Electrical Interface Transmission Line-SFP

| Parameter                        | Symbol   | Min   |   Typ | Max   | Unit   |   Remarks |
|----------------------------------|----------|-------|-------|-------|--------|-----------|
| Line Frequency                   | F L      |       |   125 |       | MHz    |         1 |
| Tx Output Impedance Differential | Z OUT TX |       |   100 |       | Ohm    |         2 |
| Rx Input Impedance Differential  | Z IN RX  |       |   100 |       | Ohm    |         2 |

## Notes:

1.  5-level encoding
2.  For all frequencies between 1MHz and 125MHz

## Low Speed Electrical Signal

| Parameter      | Symbol   | Min            | Typ   | Max            | Unit   |   Remarks |
|----------------|----------|----------------|-------|----------------|--------|-----------|
| SFPOutput Low  | V OL     | 0              |       | 0.5            | V      |         1 |
| SFPOutput High | V OH     | Host_V CC -0.5 |       | Host_V CC +0.3 | V      |         1 |
| SFPInput Low   | V IL     | 0              |       | 0.8            | V      |         1 |
| SFPInput High  | V IH     | 2              |       | V CC + 0.3     | V      |         1 |

## Notes:

1. External 4.7-10k ohm pull-up resistor required

## I2C Memory Map

| Address A0   | Address A0   | Address A0      | Address A0                                                 | Address A0              | Address A0   |
|--------------|--------------|-----------------|------------------------------------------------------------|-------------------------|--------------|
| IIC Addr     | Size         | Name            | Description                                                | Values (HEX)            | Remarks      |
| 0            | 1            | Identifier      | SFP or SFP+                                                | 03                      |              |
| 1            | 1            | Ext. Identifier | GBIC/SFP function is defined by two-wire interface ID only | 04                      |              |
| 2            | 1            | Connector       | RJ45 (Registered Jack)                                     | 22                      |              |
| 3-10         | 8            | Transceiver     | 1000BASE-T                                                 | 00 00 00 08 00 00 00 00 |              |
| 11           | 1            | Encoding        | 8B/10B                                                     | 01                      |              |
| 12           | 1            | BR, Nominal     | Nominal Bit Rate 1.3Gb/s                                   | 0D                      |              |
| 13           | 1            | Rate Identifier | Type of rate select functionality                          | 00                      |              |
| 14           | 1            | Length(SMF,km)  | Link length supported for single modefiber, units ofkm     | 00                      |              |


| 15    |   1 | Length (SMF)                | Link length supported for single mode fiber, units of 100 m                              | 00                                            |
|-------|-----|-----------------------------|------------------------------------------------------------------------------------------|-----------------------------------------------|
| 16    |   1 | Length (50um)               | Link length supported for 50 umOM2fiber, units of10m                                     | 00                                            |
| 17    |   1 | Length (62.5um)             | Link length supported for 62.5 umOM1fiber, units of 10m                                  | 00                                            |
| 18    |   1 | Length (OM4or copper cable) | 100m                                                                                     | 64                                            |
| 19    |   1 | Length (OM3)                | Link length supported for 50 umOM3fiber, units of10m                                     | 00                                            |
| 20-35 |  16 | Vendor name                 | MODULETEK                                                                                | 4D4F 44 55 4C45 54 45 4B 20 20 20 20 20 20 20 |
| 36    |   1 | Transceiver                 | Code for electronic or optical compatibility                                             | 00                                            |
| 37-39 |   3 | Vendor OUI                  | SFPvendor IEEEcompany ID                                                                 | 00 00 00                                      |
| 40-55 |  16 | VendorPN                    | Part number in Order information                                                         | -                                             |
| 56-59 |   4 | Vendor rev                  | Revision level for part number provided by vendor (ASCII)                                | -                                             |
| 60-61 |   2 | Wavelength                  | Laser wavelength (Passive/Active Cable Specification Compliance)                         | 00 00                                         |
| 62    |   1 | Unallocated                 |                                                                                          | 00                                            |
| 63    |   1 | CC BASE                     | Check code for Base ID Fields (addresses 0 to 62)                                        | -                                             |
| 64-65 |   2 | Options                     | Indicates which optional transceiver signals are implemented                             | 00 00                                         |
| 66    |   1 | BR, max                     | Upper bit rate margin                                                                    | 00                                            |
| 67    |   1 | BR, min                     | Lower bit rate margin                                                                    | 00                                            |
| 68-83 |  16 | VendorSN                    | Serial number provided by vendor                                                         | Programmed by Factory                         |
| 84-91 |   8 | Date code                   | Year,Month,Day                                                                           | Programmed by Factory                         |
| 92    |   1 | Diagnostic Monitoring Type  | Indicates which type of diagnostic monitoring is implemented (if any) in the transceiver | 00                                            |


| 93                      | 1                       | Enhanced Options             | Indicates which optional enhanced features are implemented (if any) in the transceiver           | 00                      |                         |
|-------------------------|-------------------------|------------------------------|--------------------------------------------------------------------------------------------------|-------------------------|-------------------------|
| 94                      | 1                       | SFF-8472 Compliance          | Indicates which revision of SFF-8472 the transceiver complies with.                              | 00                      |                         |
| 95                      | 1                       | CC EXT                       | Check code for the Extended ID Fields (addresses 64 to 94)                                       | -                       |                         |
| 96-127                  | 32                      | Vendor Specific              | Vendor Specific EEPROM                                                                           | -                       |                         |
| 128- 255                | 128                     | Vendor Specific              | Vendor Specific EEPROM                                                                           | -                       |                         |
| Address A2Low           | Address A2Low           | Address A2Low                | Address A2Low                                                                                    | Address A2Low           | Address A2Low           |
| IIC Addr                | Size                    | Name                         | Description                                                                                      | Values (HEX)            | Remarks                 |
| 0-94                    | 95                      | Reserved                     | Reserved                                                                                         | FF                      |                         |
| 95                      | 1                       | Checksum                     | 0-94 Byte Checksum                                                                               | -                       |                         |
| 96-121                  | 26                      | Reserved                     | Reserved                                                                                         | FF                      |                         |
| 122                     | 1                       | Security Level               | Security Level ： 00=Normal Mode ； 01=User Mode （ Level 1 ）； 02=Factory Mode （ Level 2 ）； | -                       |                         |
| 123- 126                | 4                       | Password Entry               | Password Entry Area                                                                              | 00 00 00 00             |                         |
| 127                     | 1                       | Table Selection              | Page Select Byte                                                                                 | 00                      |                         |
| Address A2 Page 00h/01h | Address A2 Page 00h/01h | Address A2 Page 00h/01h      | Address A2 Page 00h/01h                                                                          | Address A2 Page 00h/01h | Address A2 Page 00h/01h |
| IIC Addr                | Size                    | Name                         | Description                                                                                      | Values (HEX)            | Remarks                 |
| 128- 255                | 128                     | Upper Memory Map             | User Code Area                                                                                   | -                       |                         |
| Address A2 Page 8Ah     | Address A2 Page 8Ah     | Address A2 Page 8Ah          | Address A2 Page 8Ah                                                                              | Address A2 Page 8Ah     | Address A2 Page 8Ah     |
| IIC Addr                | Size                    | Name                         | Description                                                                                      | Values (HEX)            | Remarks                 |
| 128- 131                | 4                       | Firmware Version Number[4]   | Firmware Version Number                                                                          | -                       |                         |
| 132- 135                | 4                       | Total Running Time In Second | Total RunningTime In Second                                                                      | -                       |                         |
| Address A2 Page F0h     | Address A2 Page F0h     | Address A2 Page F0h          | Address A2 Page F0h                                                                              | Address A2 Page F0h     | Address A2 Page F0h     |
| IIC Addr                | Size                    | Name                         | Description                                                                                      | Values (HEX)            | Remarks                 |
| 128- 131                | 4                       | Password1 Long               | Level 1 Password                                                                                 | 00 00 10 11             |                         |


|   132 |   1 | Working Mode        | 00=AUTO; 01=SGMII; 02=FULL;                                                 | -   |
|-------|-----|---------------------|-----------------------------------------------------------------------------|-----|
|   133 |   1 | Always Enable Los   | 00=Disable; 01=Enable;                                                      | -   |
|   134 |   1 | DisableA0WP         | 00=A0 With Write Protection ； 01=A0 Without Write Protection               | 00  |
|   135 |   1 | Disable A2T00T01 WP | 00=A2 T00T01 With Write Protection ； 01=A2 T00T01 Without Write Protection | 00  |
|   136 |   1 | Enable A2TF9 Access | Access 88E1112 Directly From Table F9 00=Disable; 01=Enable                 | 00  |

## Notes ：

1. Password entry area default 00000000 ， read out as last written value

2. Module with write protection ， enter the security level 1 writeable

## User Mode

| Module   |   Level 1 Default Password | Password Can Be Changed   | Permissions                          |
|----------|----------------------------|---------------------------|--------------------------------------|
| SFP-GE-T |                   00001011 | YES(A2 TF0)               | 1 、 Read And Write A0 、 A2 T00/T01 |
| SFP-GE-T |                   00001011 | YES(A2 TF0)               | 3 、 Read And Write A2 TF0           |

## Notes ：

1.  detail in I2C memory map


## Dimensions

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000009_80de069b501587e10120764436fbb17231ea4543bbd18003c6d3bd1ee9df0e26.png)

Weight: 24.5g

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000010_619668156ed12cd28b1cd26253c1dbc1be81f4353ab13261758f7da658ed5be4.png)

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


## Electrical Pad Layout

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000012_e0ea1b70c9886e1e0bd78d8741a6e079281bb98ef7f049b07334a578ad5fcac8.png)

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000013_ea23bfb8fc8afaf011d6c335a4fd0a0ac9ea8bd3683b16363e99f3789bea4df2.png)

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000014_74062a9b50a2416d849168a4fd1498ac88f6dcee9ec59deddaeb7f0b3d39566e.png)

![Image](/SFP/SFP-GE-T/SFP-GE-T_artifacts/image_000015_4bf8d9e6b136fbef1915f28d27b2672bbae141939c8d9a48a68aa1a18cb154d5.png)


## Pin Assignment

|   PIN # | Symbol      | Description                                      |   Remarks |
|---------|-------------|--------------------------------------------------|-----------|
|       1 | V EET       | Transmitter ground (common with receiver ground) |         1 |
|       2 | TX_FAULT    | Transmitter Fault. Not supported                 |           |
|       3 | TX_DISABLE  | Transmitter Disable. PHYdisabled on high or open |         2 |
|       4 | MOD_DEF(2)  | Module Definition 2. Data line for serial ID     |         3 |
|       5 | MOD_DEF(1)  | 2Module Definition 1. Clock line for serial ID   |         3 |
|       6 | MOD_DEF(0)  | Module Definition 0. Grounded within the module  |         3 |
|       7 | Rate Select | Noconnection required                            |           |
|       8 | LOS         | Loss of Signal                                   |           |
|       9 | V EER       | Receiver ground (common with transmitter ground) |         1 |
|      10 | V EER       | Receiver ground (common with transmitter ground) |         1 |
|      11 | V EER       | Receiver ground (common with transmitter ground) |         1 |
|      12 | RD-         | Receiver Inverted DATAout. ACcoupled             |           |
|      13 | RD +        | Receiver Non-inverted DATA out. AC coupled       |           |
|      14 | V EER       | Receiver ground (common with transmitter ground) |         1 |
|      15 | V CCR       | Receiver power supply                            |           |
|      16 | V CCT       | Transmitter power supply                         |           |
|      17 | V EET       | Transmitter ground (common with receiver ground) |         1 |
|      18 | TD +        | Transmitter Non-Inverted DATA in. AC coupled     |           |
|      19 | TD-         | Transmitter Inverted DATAin. ACcoupled           |           |
|      20 | V EET       | Transmitter ground (common with receiver ground) |         1 |

## Notes:

1.  Circuit ground is connected to chassis ground
2.  Disabled: TDIS &gt; 2Vor open,Enabled:TDIS &lt; 0.8V
3.  Should Be pulled up with 4.7k -10k ohm on host board to a voltage between 2V and 3.6V

## References

1. IEEE standard 802.3. IEEE Standard Department,2005.