
## duleTek Moc

## DATA SHEET

## MODULETEK : DAC-QSFP-4SFP-40G-P-xxAWG-aa.aaM-D1C0B

QSFP to 4SFP 40G Passive Copper Cable Assembly

## Overview

ModuleTek's QSFP to 4SFP 40G passive cable is the preferred solution for 40G speed short-range data transmission with low power consumption, good stability and high cost performance.The QSFP to 4SFP passive cable is used for data transfer between a 40G QSFP port and four 10G SFP ports, providing a low-cost solution for data transfer services within and between data center racks.This product complies with the SFF-8436, QSFP+ MSA and IEEE 802.3ae standards.

## Product Features

- QSFP End: Compliant with QSFP+ MSA specifications
- SFP End: Compliant with SFP+ MSA specifications
- 4 independent duplex channels operating at 10Gbps
- Support for 2.5Gbps, 5Gbps data rates
- AC coupled inputs and outputs
- 100 Ohm differential impedance
- All-metal housing for superior EMI performance
- Single power supply 3.3V, low power consumption
- RoHS Compliant
- Operating temperature range: 0 ◦ C to 70 ◦ C

## Applications

10Gigabit Ethernet Serial Data Transmission Storage Fiber Channel

Switch, Router

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000001_dcb07d6df36240a576fa026fb51171756bf66a7ee411f075a3fef2f7dda13c22.png)


## Ordering Information

| Part Number                             | Product ID   | Description                                                     | Gauge   | Length   |
|-----------------------------------------|--------------|-----------------------------------------------------------------|---------|----------|
| DAC-QSFP-4SFP-40G-P- 30AWG-aa.aaM-D1C0B | M325807      | QSFP to 4SFP 40G Direct Attach Copper Cable Assembly, aa.aa ≤ 3 | 30AWG   | ≤ 3m     |
| DAC-QSFP-4SFP-40G-P- 28AWG-aa.aaM-D1C0B | M509807      | QSFP to 4SFP 40G Direct Attach Copper Cable Assembly, aa.aa ≤ 5 | 28AWG   | ≤ 5m     |

## Note:

1. 'P' indicates passive cable.
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
| Bit Error Rate        | BER      |        |       | 10 - 12 |        |           |
| Operating Temperature | T C      |   0    |       | 70      | ◦ C    |         1 |
| Storage Temperature   | T STO    | -40    |       | 85      | ◦ C    |         2 |
| Input Voltage         | V CC     |   3.14 |   3.3 | 3.46    | V      |           |

## Notes:

- 1.Case temperature

2.Ambient temperature

## I2C Memory Map

## QSFP END

| Lower Memory Map (A0h)   | Lower Memory Map (A0h)   | Lower Memory Map (A0h)      | Lower Memory Map (A0h)                                        | Lower Memory Map (A0h)   | Lower Memory Map (A0h)   |
|--------------------------|--------------------------|-----------------------------|---------------------------------------------------------------|--------------------------|--------------------------|
| IIC Addr                 | Size                     | Name                        | Description                                                   | Values (HEX)             | Remarks                  |
| 0                        | 1                        | Identifier                  | QSFP+                                                         | 0D                       |                          |
| 1-2                      | 2                        | Status                      | bit0:Data Not Ready; bit1:IntL; bit2: Flat mem                | 00 06                    |                          |
| 3                        | 1                        | Channel Status LOS Flag     | Latched TX/RX LOS indicator                                   | 00                       |                          |
| 4                        | 1                        | Channel Status TxFault Flag | Latched TX fault indicator                                    | 00                       |                          |
| 5                        | 1                        | Channel Status Reserved5    | Reserved                                                      | 00                       |                          |
| 6                        | 1                        | Module Monitor Temp AW Flag | Latched temperature alarm/warning and initialization complete | 00                       |                          |
| 7                        | 1                        | Module Monitor Vcc AW Flag  | Latched Vcc alarm/warning                                     | 00                       |                          |
| 8                        | 1                        | Module Monitor Reserved8    | Reserved                                                      | 00                       |                          |
| 9-10                     | 2                        | Channel Mon RxPower AW Flag | Latched Rx Power alarm/warning                                | 00 00                    |                          |
| 11-12                    | 2                        | Channel Mon TxBias AW Flag  | Latched Tx Bias alarm/warning                                 | 00 00                    |                          |
| 13-21                    | 9                        | Channel Mon Reserved13      | Reserved                                                      | 00                       |                          |
| 22-23                    | 2                        | Module Monitor Temp         | Internally measured module temperature                        | 00 00                    |                          |


| 24-25   |   2 | Module Monitor Reserved24   | Reserved                                                          | 00 00   |
|---------|-----|-----------------------------|-------------------------------------------------------------------|---------|
| 26-27   |   2 | Module Monitor Voltage      | Internally measured module supply voltage                         | 00 00   |
| 28-33   |   6 | Module Monitor Reserved28   | Reserved                                                          | 00      |
| 34-35   |   2 | Channel Mon Rx1Power        | Internally measured RX input power, channel 1                     | 00 00   |
| 36-37   |   2 | Channel Mon Rx2Power        | Internally measured RX input power, channel 2                     | 00 00   |
| 38-39   |   2 | Channel Mon Rx3Power        | Internally measured RX input power, channel 3                     | 00 00   |
| 40-41   |   2 | Channel Mon Rx4Power        | Internally measured RX input power, channel 4                     | 00 00   |
| 42-43   |   2 | Channel Mon Tx1Bias         | Internally measured TX bias, channel 1                            | 00 00   |
| 44-45   |   2 | Channel Mon Tx2Bias         | Internally measured TX bias, channel 2                            | 00 00   |
| 46-47   |   2 | Channel Mon Tx3Bias         | Internally measured TX bias, channel 3                            | 00 00   |
| 48-49   |   2 | Channel Mon Tx4Bias         | Internally measured TX bias, channel 4                            | 00 00   |
| 50-81   |  32 | Channel Mon Reserved50      | Reserved                                                          | 00      |
| 82-85   |   4 | Reserved82                  | Reserved                                                          | 00      |
| 86      |   1 | Control TxDisable           | Txn Read/write bit that allows software disable of transmitters   | 00      |
| 87      |   1 | Control Rx Rate Select      | Rx channel Software Rate Select                                   | 00      |
| 88      |   1 | Control Tx Rate Select      | Tx channel Software Rate Select                                   | 00      |
| 89      |   1 | Control Rx4 App Select      | Software Application Select per SFF-8079, Rx Channel 4 (Optional) | 00      |
| 90      |   1 | Control Rx3 App Select      | Software Application Select per SFF-8079, Rx Channel 3 (Optional) | 00      |
| 91      |   1 | Control Rx2 App Select      | Software Application Select per SFF-8079, Rx Channel 2 (Optional) | 00      |
| 92      |   1 | Control Rx1 App Select      | Software Application Select per SFF-8079, Rx Channel 1 (Optional) | 00      |


| 93                        | 1                         | Control Power              | Power set to low power mode/Override of LPMode signal setting the power mode with software   | 00                        |                           |
|---------------------------|---------------------------|----------------------------|----------------------------------------------------------------------------------------------|---------------------------|---------------------------|
| 94                        | 1                         | Control Tx4 App Select     | Software Application Select per SFF-8079, Tx Channel 4 (Optional)                            | 00                        |                           |
| 95                        | 1                         | Control Tx3 App Select     | Software Application Select per SFF-8079, Tx Channel 3 (Optional)                            | 00                        |                           |
| 96                        | 1                         | Control Tx2 App Select     | Software Application Select per SFF-8079, Tx Channel 2 (Optional)                            | 00                        |                           |
| 97                        | 1                         | Control Tx1 App Select     | Software Application Select per SFF-8079, Tx Channel 1 (Optional)                            | 00                        |                           |
| 98-99                     | 2                         | Control Reserved98         | Reserved                                                                                     | 00 00                     |                           |
| 100                       | 1                         | Mask TxRx LOS              | Masking bit for TX/RX LOS indicator                                                          | 00                        |                           |
| 101                       | 1                         | Mask TxFault               | Masking bit for TX fault indicator                                                           | 00                        |                           |
| 102                       | 1                         | Mask Reserved102           | Reserved                                                                                     | 00                        |                           |
| 103                       | 1                         | Mask Temp AW               | Masking bit for Temperature alarm/warning and initialization complete                        | 00                        |                           |
| 104                       | 1                         | Mask Vcc AW                | Masking bit for Vcc alarm/warning                                                            | 00                        |                           |
| 105-106                   | 2                         | Mask Reserved105           | Reserved                                                                                     | 00 00                     |                           |
| 107-118                   | 12                        | Reserved107                | Reserved                                                                                     | 00                        |                           |
| 119-122                   | 4                         | Password Change Entry Area | Password Change Entry Area (optional)                                                        | 00 00 00 00               |                           |
| 123-126                   | 4                         | Password Entry Area        | Password Entry Area (Optional)                                                               | 00 00 00 00               |                           |
| 127                       | 1                         | Page Select                | Page Select Byte                                                                             | 00                        |                           |
| Upper Memory Map Page 00h | Upper Memory Map Page 00h | Upper Memory Map Page 00h  | Upper Memory Map Page 00h                                                                    | Upper Memory Map Page 00h | Upper Memory Map Page 00h |
| IIC Addr                  | Size                      | Name                       | Description                                                                                  | Values (HEX)              | Remarks                   |
| 128                       | 1                         | Identifier                 | QSFP+                                                                                        | 0D                        |                           |
| 129                       | 1                         | Ext. Identifier            | Extended Identifier of Serial Module                                                         | 00                        |                           |
| 130                       | 1                         | Connector                  | No separable connector                                                                       | 23                        |                           |
| 131-138                   | 8                         | Tranceiver                 | 40GBASE-CR4                                                                                  | 08 00 00 00 00 00 00 00   |                           |


| 139     |   1 | Encoding                       | 64B66B                                                                                                       | 05                                              |
|---------|-----|--------------------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| 140     |   1 | BR, nominal                    | Nominal Bit Rate 10.3Gb/s                                                                                    | 67                                              |
| 141     |   1 | Extended RateSelect Compliance | Tags for Extended RateSelect compliance                                                                      | 00                                              |
| 142     |   1 | Length(SMF)                    | Link length supported for SMF fiber in km                                                                    | 00                                              |
| 143     |   1 | Length (E-50µm)                | Link length supported for EBW 50/125 µm fiber, units of 2 m                                                  | 00                                              |
| 144     |   1 | Length (50 µm)                 | Link length supported for 50/125 µm fiber, units of1m                                                        | 00                                              |
| 145     |   1 | Length (62.5 µm)               | Link length supported for 62.5/125 µm fiber, units of 1 m                                                    | 00                                              |
| 146     |   1 | Length (Copper)                | Link length supported for copper, units of 1m                                                                | -                                               |
| 147     |   1 | Device Tech                    | Copper cable unequalized                                                                                     | A0                                              |
| 148-163 |  16 | Vendor name                    | MODULETEK                                                                                                    | 4D 4F 44 55 4C 45 54 45 4B 20 20 20 20 20 20 20 |
| 164     |   1 | Extended Transceiver           | Extended Transceiver Codes for InfiniBand                                                                    | 00                                              |
| 165-167 |   3 | Vendor OUI                     | QSFP vendor IEEE company ID                                                                                  | 00 00 00                                        |
| 168-183 |  16 | Vendor PN                      | Part number in Order information                                                                             | -                                               |
| 184-185 |   2 | Vendor rev                     | Revision level for part number provided by vendor (ASCII)                                                    | -                                               |
| 186-187 |   2 | Wavelength                     | Nominal laser wavelength (Wavelength = value / 20 in nm)                                                     | -                                               |
| 188-189 |   2 | Wavelength Tolerance           | Guaranteed range of laser wavelength (+/- value) from Nominal wavelength.(Wavelength Tol. = value/200 in nm) | -                                               |
| 190     |   1 | Max Case Temp                  | Maximum case temperaturein degrees C(70 ◦ C )                                                                | 46                                              |
| 191     |   1 | CC BASE                        | Check code for Base ID Fields (addresses 128-190)                                                            | -                                               |


| 192-195                   | 4                         | Options                     | Rate Select, TX Disable, TX Fault, LOS, Warning indicators for: Temperature, VCC, RX power, TX Bias     | 0B 00 00 00               |                           |
|---------------------------|---------------------------|-----------------------------|---------------------------------------------------------------------------------------------------------|---------------------------|---------------------------|
| 196-211                   | 16                        | Vendor SN                   | Serial number provided by vendor                                                                        | Programmed by Factory     |                           |
| 212-219                   | 8                         | Date Code                   | Year,Month,Day                                                                                          | Programmed by Factory     |                           |
| 220                       | 1                         | Diagnostic Monitoring Type  | Indicates which types of diagnostic monitoring are implemented (if any) in the Module. Bit 1,0 Reserved | 2E                        |                           |
| 221                       | 1                         | Enhanced options            | Indicates which optional enhanced features are implemented in the Module.                               | 00                        |                           |
| 222                       | 1                         | Reserved                    | Reserved                                                                                                | -                         |                           |
| 223                       | 1                         | CC EXT                      | Check code for the Extended ID Fields (addresses 192-222)                                               | -                         |                           |
| 224-255                   | 32                        | Vendor Specific             | Vendor Specific EEPROM                                                                                  | -                         |                           |
| Upper Memory Map Page 02h | Upper Memory Map Page 02h | Upper Memory Map Page 02h   | Upper Memory Map Page 02h                                                                               | Upper Memory Map Page 02h | Upper Memory Map Page 02h |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)              | Remarks                   |
| 128-255                   | 128                       | Upper Memory Map            | User Code Area                                                                                          | -                         |                           |
| Upper Memory Map Page 8Ah | Upper Memory Map Page 8Ah | Upper Memory Map Page 8Ah   | Upper Memory Map Page 8Ah                                                                               | Upper Memory Map Page 8Ah | Upper Memory Map Page 8Ah |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)              | Remarks                   |
| 128-131                   | 4                         | Firmware Version Number[4]  | Firmware Version Number                                                                                 | -                         |                           |
| 132-135                   | 4                         | Datasheet Version Number[4] | Datasheet Version Number                                                                                | -                         |                           |
| 136                       | 1                         | Security Level              | Security Level ： 00=Normal Mode ； 01=User Mode （ level 1 ） ； 02=Factory Mode （ level 2 ） ；      | -                         |                           |
| 137-138                   | 2                         | Vcc ADC                     | Vcc ADC                                                                                                 | -                         |                           |
| 139-140                   | 2                         | Temp ADC                    | Temp ADC                                                                                                | -                         |                           |
| Upper Memory Map Page F0h | Upper Memory Map Page F0h | Upper Memory Map Page F0h   | Upper Memory Map Page F0h                                                                               | Upper Memory Map Page F0h | Upper Memory Map Page F0h |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)              | Remarks                   |
| 128-131                   | 4                         | Password1 long              | Level 1 Password                                                                                        | 00 00 10 11               |                           |

## Notes ：

1.Password entry area are write-only bits ， read out always 00000000


- 2.Module with write protection ， enter the security level 1 writeable

## SFP END

| Address A0   | Address A0   | Address A0                   | Address A0                                                                                                      | Address A0                                      | Address A0   |
|--------------|--------------|------------------------------|-----------------------------------------------------------------------------------------------------------------|-------------------------------------------------|--------------|
| IIC Addr     | Size         | Name                         | Description                                                                                                     | Values (HEX)                                    | Remarks      |
| 0            | 1            | Identifier                   | SFP or SFP+                                                                                                     | 03                                              |              |
| 1            | 1            | Ext. Identifier              | GBIC/SFP function is defined by two-wire interface ID only                                                      | 04                                              |              |
| 2            | 1            | Connector                    | Copper pigtail                                                                                                  | 21                                              |              |
| 3-10         | 8            | Transceiver                  | 1X Copper Passive/Passive Cable *8                                                                              | 01 00 00 00 00 04 00 00                         |              |
| 11           | 1            | Encoding                     | 64B/66B                                                                                                         | 06                                              |              |
| 12           | 1            | BR, Nominal                  | Nominal Bit Rate 10.0Gb/s                                                                                       | 64                                              |              |
| 13           | 1            | Rate Identifier              | Type of rate select functionality                                                                               | 00                                              |              |
| 14           | 1            | Length(SMF,km)               | Link length supported for single mode fiber, units of km                                                        | 00                                              |              |
| 15           | 1            | Length (SMF)                 | Link length supported for single mode fiber, units of 100 m                                                     | 00                                              |              |
| 16           | 1            | Length (50um)                | Link length supported for 50 um OM2 fiber, units of 10 m                                                        | 00                                              |              |
| 17           | 1            | Length (62.5um)              | Link length supported for 62.5 um OM1 fiber, units of 10 m                                                      | 00                                              |              |
| 18           | 1            | Length (OM4 or copper cable) | Link length supported for 50um OM4 fiber, units of 10m. Alternatively copper or direct attach cable, units of m | -                                               |              |
| 19           | 1            | Length (OM3)                 | Link length supported for 50 um OM3 fiber, units of 10 m                                                        | 00                                              |              |
| 20-35        | 16           | Vendor name                  | MODULETEK                                                                                                       | 4D 4F 44 55 4C 45 54 45 4B 20 20 20 20 20 20 20 |              |
| 36           | 1            | Transceiver                  | Code for electronic or optical compatibility                                                                    | 00                                              |              |
| 37-39        | 3            | Vendor OUI                   | SFP vendor IEEE company ID                                                                                      | 00 00 00                                        |              |


| 40-55          | 16             | Vendor PN                  | Part number in Order information                                                         | -                     |                |
|----------------|----------------|----------------------------|------------------------------------------------------------------------------------------|-----------------------|----------------|
| 56-59          | 4              | Vendor rev                 | Revision level for part number provided by vendor (ASCII)                                | -                     |                |
| 60-61          | 2              | Wavelength                 | Laser wavelength (Passive/Active Cable Specification Compliance)                         | 00 00                 |                |
| 62             | 1              | Unallocated                |                                                                                          | 00                    |                |
| 63             | 1              | CC BASE                    | Check code for Base ID Fields (addresses 0 to 62)                                        | -                     |                |
| 64-65          | 2              | Options                    | Indicates which optional transceiver signals are implemented                             | 00 00                 |                |
| 66             | 1              | BR, max                    | Upper bit rate margin                                                                    | 64                    |                |
| 67             | 1              | BR, min                    | Lower bit rate margin                                                                    | 00                    |                |
| 68-83          | 16             | Vendor SN                  | Serial number provided by vendor                                                         | Programmed by Factory |                |
| 84-91          | 8              | Date code                  | Year,Month,Day                                                                           | Programmed by Factory |                |
| 92             | 1              | Diagnostic Monitoring Type | Indicates which type of diagnostic monitoring is implemented (if any) in the transceiver | 00                    |                |
| 93             | 1              | Enhanced Options           | Indicates which optional enhanced features are implemented (if any) in the transceiver   | 00                    |                |
| 94             | 1              | SFF-8472 Compliance        | Indicates which revision of SFF-8472 the transceiver complies with.                      | 00                    |                |
| 95             | 1              | CC EXT                     | Check code for the Extended ID Fields (addresses 64 to 94)                               | -                     |                |
| 96-127         | 32             | Vendor Specific            | Vendor Specific EEPROM                                                                   | -                     |                |
| 128-255        | 128            | Vendor Specific            | Vendor Specific EEPROM                                                                   | -                     |                |
| Address A2 Low | Address A2 Low | Address A2 Low             | Address A2 Low                                                                           | Address A2 Low        | Address A2 Low |
| IIC Addr       | Size           | Name                       | Description                                                                              | Values (HEX)          | Remarks        |
| 0-94           | 95             | Reserved                   | Reserved                                                                                 | FF                    |                |
| 95             | 1              | Checksum                   | 0-94 Byte Checksum                                                                       | -                     |                |
| 96-121         | 26             | Reserved                   | Reserved                                                                                 | 00                    |                |


| 122                     | 1                       | Security Level               | Security Level ： 00=Normal Mode ； 01=User Mode （ Level 1 ） ； 02=Factory Mode （ Level 2 ） ；   | 00                      |                         |
|-------------------------|-------------------------|------------------------------|------------------------------------------------------------------------------------------------------|-------------------------|-------------------------|
| 123-126                 | 4                       | Password Entry               | Password Entry Area                                                                                  | 00 00 00 00             |                         |
| 127                     | 1                       | Table Selection              | Page Select Byte                                                                                     | 00                      |                         |
| Address A2 Page 00h/01h | Address A2 Page 00h/01h | Address A2 Page 00h/01h      | Address A2 Page 00h/01h                                                                              | Address A2 Page 00h/01h | Address A2 Page 00h/01h |
| IIC Addr                | Size                    | Name                         | Description                                                                                          | Values (HEX)            | Remarks                 |
| 128-255                 | 128                     | Upper Memory Map             | User Code Area                                                                                       | FF                      |                         |
| Address A2 Page 8Ah     | Address A2 Page 8Ah     | Address A2 Page 8Ah          | Address A2 Page 8Ah                                                                                  | Address A2 Page 8Ah     | Address A2 Page 8Ah     |
| IIC Addr                | Size                    | Name                         | Description                                                                                          | Values (HEX)            | Remarks                 |
| 128-131                 | 4                       | Firmware Version Number[4]   | Firmware Version Number                                                                              | -                       |                         |
| 132-135                 | 4                       | Total Running Time In Second | Total Running Time In Second                                                                         | -                       |                         |
| Address A2 Page F0h     | Address A2 Page F0h     | Address A2 Page F0h          | Address A2 Page F0h                                                                                  | Address A2 Page F0h     | Address A2 Page F0h     |
| IIC Addr                | Size                    | Name                         | Description                                                                                          | Values (HEX)            | Remarks                 |
| 128-131                 | 4                       | Password1 Long               | Level 1 Password                                                                                     | 00 00 10 11             |                         |
| 132                     | 1                       | DisableA0WP                  | 00=A0 With Write Protection ； 01=A0 Without Write Protection                                        | 00                      |                         |
| 133                     | 1                       | DisableA2T00T01WP            | 00=A2 T00T01 With Write Protection ； 01=A2 T00T01 Without Write Protection                          | 00                      |                         |

## Notes ：

1.Password entry area default 00000000 ， read out as last written value

2.Module with write protection ， enter the security level 1 writeable


## User Mode

| Module   | Level 1 Default Password   | Password Can Be Changed   | Permissions                                           |
|----------|----------------------------|---------------------------|-------------------------------------------------------|
| QSFP END | 00 00 10 11                | YES(A0 TF0)               | 1 、 Read And Write A0 T00/T02                        |
| QSFP END | 00 00 10 11                | YES(A0 TF0)               | 3 、 Read And Write A0 TF0                            |
| SFP END  | 00 00 10 11                | YES(A2 TF0)               | 1 、 Read And Write A0 、 A2 T00/T01 2 、 Read A2 T8A |
| SFP END  | 00 00 10 11                | YES(A2 TF0)               | 3 、 Read And Write A2 TF0                            |


## Typical S parameter

## 3m 30AWG typical insertion loss curve

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000013_4585587347894b1dc61ba80b85efdc9cb8b5d4aefb2c465fbccd0f02cf3e56cc.png)

## 3m 30AWG typical reflection curve

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000014_056523d1c4475385481d82d51e027e2a22b623976941944a904c536b7395f05b.png)


duleTek

Moc

## 5m 28AWG typical insertion loss curve

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000016_bef56b8de305dff8576251692c88e104e01effdf5d5d256a2cad54aa8d4ad0ea.png)

## 5m 28AWG typical reflection curve

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000017_9f0ea62886313b333c60c8bcf1f73dfa51c8ead0f75c6590184baff8d1f9ef8a.png)

## Note:

1. Insertion loss standard reference IEEE802.3ba 85.10.2 ： IL&lt;17.04dB@5.15625 GHz
2. Reflection curve standard reference IEEE802.3ba 85.10.4 ： SDDxx(dB)=12 - 2 × SQRT(f), 0.05 ≤ f &lt; 4.1GHz.
3. Reflection curve standard reference IEEE802.3ba 85.10.4 ： SDDxx(dB)=6.3 - 13 × log10(f/5.5), 4.1 ≤ f ≤ 10GHz.


duleTek

Moc

## Weight

| Parameter                | Symbol   |   Typ | Unit   |   Remarks |
|--------------------------|----------|-------|--------|-----------|
| 30AWG Product Weight     | G D30    | 245   | g/PCS  |         1 |
| 28AWG Product Weight     | G D28    | 310   | g/PCS  |         1 |
| 30AWG Cable Weight       | G C30    | 110   | g/M    |         2 |
| 28AWG Cable Weight       | G C28    | 170   | g/M    |         2 |
| SFP END Dust Cap Weight  | G S      |   0.8 | g/PCS  |           |
| QSFP END Dust Cap Weight | G Q      |   1.4 | g/PCS  |           |

## Notes ：

1.The weight of DAC-QSFP-4SFP-40G-P-xxAWG-1M-D1C0B

2.The weight of unit length cable(four sticks).For example: the weight of

DAC-QSFP-4SFP-40G-P-28AWG-5M-D1C0B is:310+170*(5-1)+0.80*4+1.40=994.6g

## Dimensions

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000019_517ba5e9a30574d07577d5c4f68d3dc0d578a31b83378b3db66e2f3d2c4276ac.png)

L1

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


## Cable Specifications

| Parameter       | Symbol   |   Min |   Typ |   Max | Unit   | Remarks   |
|-----------------|----------|-------|-------|-------|--------|-----------|
| Wire Gauge      |          |    30 |       |    28 | AWG    |           |
| Cable Impedance | Z        |    90 |   100 |   110 | Ohm    |           |

## Cable Dimension

|   Serial number |   Standard Wire Gauge (AWG) |   Cable diameter OD (mm) |   Minimum bending radius R (mm) |
|-----------------|-----------------------------|--------------------------|---------------------------------|
|               1 |                          30 |                      4.2 |                              25 |
|               2 |                          28 |                      4.7 |                              26 |

## Nominal Length

|   Serial number |   Module nominal length L1 (cm) |   Tolerance range ±(cm) |
|-----------------|---------------------------------|-------------------------|
|               1 |                             100 |                       2 |
|               2 |                             200 |                       2 |
|               3 |                             300 |                       4 |
|               4 |                             400 |                       4 |
|               5 |                             500 |                       6 |


duleTek

## QSFP Electrical Pad Layout

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000022_d540dc1764c237e3adcb22406a8deee2caf722bed13380c1f375aadca2b474a5.png)

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000023_107f6f53ac68e9608f09c05cd5d203ca6980e4c94b3e8733f53a1cf857565ffd.png)

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000024_e9d89343ce640b3008f01031bcee59df5b8907ff55a3da8ab54012369a5b6df5.png)


## SFP Electrical Pad Layout

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000026_cf5a10a5383adc3422c26dd34ae687c0b44a56ad146220f9fff7d85092d81b7a.png)

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000027_c476673ca97dbca37851268d00d7299ee56815a33b28b3ae073c9d661694d192.png)

![Image](/DAC/DAC-40-4x10-xM/DAC-40-4x10-xM_artifacts/image_000028_7cc2a9176c2304eb629d8177b95ab2a0e27fea3099a7673bcacfc29d0efbb569.png)


## QSFP Pin Assignment

|   PIN # | Symbol   | Description                                                                            |   Remarks |
|---------|----------|----------------------------------------------------------------------------------------|-----------|
|       1 | GND      | Ground                                                                                 |         5 |
|       2 | Tx2n     | Transmitter Inverted Data Input, LAN2                                                  |           |
|       3 | Tx2p     | Transmitter Non-Inverted Data Input, LAN2                                              |           |
|       4 | GND      | Ground                                                                                 |         5 |
|       5 | Tx4n     | Transmitter Inverted Data Input, LAN4                                                  |           |
|       6 | Tx4p     | Transmitter Non-Inverted Data Input, LAN4                                              |           |
|       7 | GND      | Ground                                                                                 |         5 |
|       8 | ModSelL  | Module select pin, the module responds to two-wire serial communication when low level |         1 |
|       9 | ResetL   | Module Reset                                                                           |         2 |
|      10 | V CC RX  | +3.3V Power Supply Receiver                                                            |           |
|      11 | SCL      | 2-wire serial interface clock                                                          |           |
|      12 | SDA      | 2-wire serial interface data                                                           |           |
|      13 | GND      | Ground                                                                                 |         5 |
|      14 | Rx3p     | Receiver Non-Inverted Data Output, LAN3                                                |           |
|      15 | Rx3n     | Receiver Inverted Data Output, LAN3                                                    |           |
|      16 | GND      | Ground                                                                                 |         5 |
|      17 | Rx1p     | Receiver Non-Inverted Data Output, LAN1                                                |           |
|      18 | Rx1n     | Receiver Inverted Data Output, LAN1                                                    |           |
|      19 | GND      | Ground                                                                                 |         5 |
|      20 | GND      | Ground                                                                                 |         5 |
|      21 | Rx2n     | Receiver Inverted Data Output, LAN2                                                    |           |
|      22 | Rx2p     | Receiver Non-Inverted Data Output, LAN2                                                |           |
|      23 | GND      | Ground                                                                                 |         5 |
|      24 | Rx4n     | Receiver Inverted Data Output, LAN4                                                    |           |
|      25 | Rx4p     | Receiver Non-Inverted Data Output, LAN4                                                |           |
|      26 | GND      | Ground                                                                                 |         5 |
|      27 | ModPrsL  | The module is inserted into the indicate pin and grounded in the module.               |         3 |
|      28 | IntL     | Interrupt                                                                              |         4 |
|      29 | V CC TX  | +3.3V Power Supply transmitter                                                         |           |
|      30 | V CC1    | +3.3V Power Supply                                                                     |           |
|      31 | LPMode   | Low Power Mode                                                                         |         5 |
|      32 | GND      | Ground                                                                                 |         5 |


|   33 | Tx3p   | Transmitter Non-Inverted Data Input, LAN3   |    |
|------|--------|---------------------------------------------|----|
|   34 | Tx3n   | Transmitter Inverted Data Input, LAN3       |    |
|   35 | GND    | Ground                                      |  5 |
|   36 | Tx1p   | Transmitter Non-Inverted Data Input, LAN1   |    |
|   37 | Tx1n   | Transmitter Inverted Data Input, LAN1       |    |
|   38 | GND    | Ground                                      |  5 |

## Notes:

1. ModSelL is the input pin. The module responds to 2-wire serial communication commands when it is held low by the host. ModSelL allows multiple QSFP modules to be used on a single 2-wire interface bus. If ModSelL is High, the module will not respond to any 2-wire interface communication from the host. ModSelL has internal pull-up resistors in the module
2. The module restart pin, when the low level on the ResetL pin lasts longer than the minimum pulse length, resets the module and restores all user modules to their default state. When performing reset device, the host should ignore all status bits. Until the module reset interrupt is completed, please note that during hot plugging, the module will issue this information to complete the reset interrupt without resetting
3. This pin is active high, indicating that the module is running under a low power module.The signal has no effect on the functionality of this product.
4. IntL is the output pin, which is the open collector output and must be pulled up to Vcc with a 4.7kΩ-10kΩ resistor on the motherboard. When it is low, it indicates that the module may malfunction. The host uses a 2-wire serial interface to identify the interrupt source
5. 5.Circuit ground is internally isolated from chassis ground.


## SFP Pin Assignment

|   PIN # | Symbol     | Description                                                   |   Remarks |
|---------|------------|---------------------------------------------------------------|-----------|
|       1 | V EET      | Transmitter ground (common with receiver ground)              |         1 |
|       2 | TX_FAULT   | Transmitter Fault.                                            |           |
|       3 | TX_DISABLE | Transmitter Disable. Laser output disabled on high or open    |           |
|       4 | SDA        | Data line for serial ID                                       |         2 |
|       5 | SCL        | Clock line for serial ID                                      |         2 |
|       6 | MOD_ABS    | Module Absent. Grounded within the module                     |         2 |
|       7 | RS0        | No connection required                                        |           |
|       8 | LOS        | Loss of Signal indication. Logic 0 indicates normal operation |           |
|       9 | RS1        | No connection required                                        |           |
|      10 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      11 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      12 | RD-        | Receiver Inverted DATA out. AC coupled                        |           |
|      13 | RD+        | Receiver Non-inverted DATA out. AC coupled                    |           |
|      14 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      15 | V CCR      | Receiver power supply                                         |           |
|      16 | V CCT      | Transmitter power supply                                      |           |
|      17 | V EET      | Transmitter ground (common with receiver ground)              |         1 |
|      18 | TD+        | Transmitter Non-Inverted DATA in. AC coupled                  |           |
|      19 | TD-        | Transmitter Inverted DATA in. AC coupled                      |           |
|      20 | V EET      | Transmitter ground (common with receiver ground)              |         1 |

## Notes:

1. Circuit ground is isolated from chassis ground
2. Should Be pulled up with 4.7k - 10k ohm on host board to a voltage between 2V and 3.6V

## References

1. IEEE standard 802.3ae. IEEE Standard Department, 2008.
2. IEEE standard 802.3ba. IEEE Standard Department.