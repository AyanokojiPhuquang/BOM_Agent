
## DATA SHEET

## MODULETEK : UMDCQ1H-Q1HPM-x

QSFP28 100G Passive Copper Cable Assembly

## UMDCQ1H-Q1HPM-x Overview

ModuleTek's QSFP28 passive cable uses shielded high-speed differential cables,Compliant with 100G Ethernet standard and QSFP28 Multi-Source Agreement (MSA) standard, it supports 100G transmission rate and can be backward compatible with various rates.QSFP28 passive cable is the  preferred solution for short-distance applications. It is widely used for data transmission between data  centers and cabinets or adjacent cabinets. Its biggest feature is low cost, ultra-low power consumption  (less than 0.1 watt) and high  reliability.

## Product Features

- Up to 100 Gb/s bi-directional data links
- Compliant with QSFP28 MSA specifications
- Fully Compliant with IEEE 802.3bj and Infiniband EDR specifications
- AC coupled inputs and outputs
- 100 Ohm differential impedance
- All-metal housing for superior EMI performance
- Single power supply 3.3V, low power consumption
- RoHS Compliant
- Operating temperature range: 0 ◦ C to 70 ◦ C

## Applications

- 100Gigabit Ethernet
- Serial Data Transmission
- Infiniband

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000001_49d29266ae81ed46978398d3ca77faee332cd954c01d1df4ab72cfdb5ddeb6c5.png)


## Ordering Information

| Part ID                            | Description                                                       | Gauge   | Length      |
|------------------------------------|-------------------------------------------------------------------|---------|-------------|
| DAC-QSFP28- QSFP28-P-30AWG- aa.aaM | QSFP28 100G Passive Direct Attach Copper CableAssembly, aa.aa ≤ 2 | 30AWG   | length ≤ 2m |
| DAC-QSFP28- QSFP28-P-28AWG- aa.aaM | QSFP28 100G Passive Direct Attach Copper CableAssembly, aa.aa ≤ 3 | 28AWG   | length ≤ 3m |
| DAC-QSFP28- QSFP28-P-26AWG- aa.aaM | QSFP28 100G Passive Direct Attach Copper CableAssembly, aa.aa ≤ 5 | 26AWG   | length ≤ 5m |

## Note:

1. 'P' indicates passive cable
2. 'aa.aa' indicates the cable length in meters.
3. The product with write protection.
4. The wire diameter of the products in the above list is the default value under different lengths. We can also provide other wire products to customers with special requirements.
5. The cable used in this product is produced by Belden Hessmann Industrial (Suzhou) Co., Ltd. (Brand: BELDEN),the cable sheath uses PVC material.
6. Product ID is the short order number of our product standard model.


## General Specifications

| Parameter             | Symbol   |    Min |   Typ | Max     | Unit   |   Remarks |
|-----------------------|----------|--------|-------|---------|--------|-----------|
| Bit Error Rate        | BER      |        |       | 10 - 12 |        |           |
| Operating Temperature | T C      |   0    |       | 70      | ◦ C    |         1 |
| Storage Temperature   | T STO    | -40    |       | 85      | ◦ C    |         2 |
| Input Voltage         | V CC     |   3.14 |   3.3 | 3.46    | V      |           |

## Notes:

1.Case temperature 2.Ambient temperature

## I2C Memory Map

| Lower Memory Map (A0h)   | Lower Memory Map (A0h)   | Lower Memory Map (A0h)      | Lower Memory Map (A0h)                                        | Lower Memory Map (A0h)   | Lower Memory Map (A0h)   |
|--------------------------|--------------------------|-----------------------------|---------------------------------------------------------------|--------------------------|--------------------------|
| IIC Addr                 | Size                     | Name                        | Description                                                   | Values (HEX)             | Remarks                  |
| 0                        | 1                        | Identifier                  | QSFP+                                                         | 0D                       |                          |
| 1-2                      | 2                        | Status                      | bit0:Data Not Ready; bit1:IntL; bit2: Flat mem                | 00 06                    |                          |
| 3                        | 1                        | Channel Status LOS Flag     | Latched TX/RX LOSindicator                                    | 00                       |                          |
| 4                        | 1                        | Channel Status TxFault Flag | Latched TX fault indicator                                    | 00                       |                          |
| 5                        | 1                        | Channel Status Reserved5    | Reserved                                                      | 00                       |                          |
| 6                        | 1                        | Module Monitor Temp AWFlag  | Latched temperature alarm/warning and initialization complete | 00                       |                          |
| 7                        | 1                        | Module Monitor Vcc AWFlag   | Latched Vcc alarm/warning                                     | 00                       |                          |
| 8                        | 1                        | Module Monitor Reserved8    | Reserved                                                      | 00                       |                          |
| 9-10                     | 2                        | Channel Mon RxPower AWFlag  | Latched Rx Power alarm/warning                                | 00 00                    |                          |
| 11-12                    | 2                        | Channel Mon TxBias AWFlag   | Latched Tx Bias alarm/warning                                 | 00 00                    |                          |
| 13-21                    | 9                        | Channel Mon Reserved13      | Reserved                                                      | 00                       |                          |
| 22-23                    | 2                        | Module Monitor Temp         | Internally measured module temperature                        | 00 00                    |                          |
| 24-25                    | 2                        | Module Monitor Reserved24   | Reserved                                                      | 00 00                    |                          |


| 26-27   |   2 | Module Monitor Voltage    | Internally measured module supply voltage                         | 00 00   |
|---------|-----|---------------------------|-------------------------------------------------------------------|---------|
| 28-33   |   6 | Module Monitor Reserved28 | Reserved                                                          | 00      |
| 34-35   |   2 | Channel Mon Rx1Power      | Internally measured RX input power, channel 1                     | 00 00   |
| 36-37   |   2 | Channel Mon Rx2Power      | Internally measured RX input power, channel 2                     | 00 00   |
| 38-39   |   2 | Channel Mon Rx3Power      | Internally measured RX input power, channel 3                     | 00 00   |
| 40-41   |   2 | Channel Mon Rx4Power      | Internally measured RX input power, channel 4                     | 00 00   |
| 42-43   |   2 | Channel Mon Tx1Bias       | Internally measured TX bias, channel 1                            | 00 00   |
| 44-45   |   2 | Channel Mon Tx2Bias       | Internally measured TX bias, channel 2                            | 00 00   |
| 46-47   |   2 | Channel Mon Tx3Bias       | Internally measured TX bias, channel 3                            | 00 00   |
| 48-49   |   2 | Channel Mon Tx4Bias       | Internally measured TX bias, channel 4                            | 00 00   |
| 50-81   |  32 | Channel Mon Reserved50    | Reserved                                                          | 00      |
| 82-85   |   4 | Reserved82                | Reserved                                                          | 00      |
| 86      |   1 | Control TxDisable         | Txn Read/write bit that allows software disable of transmitters   | 00      |
| 87      |   1 | Control Rx Rate Select    | Rx channel Software Rate Select                                   | 00      |
| 88      |   1 | Control Tx Rate Select    | Tx channel Software Rate Select                                   | 00      |
| 89      |   1 | Control Rx4 App Select    | Software Application Select per SFF-8079, Rx Channel 4 (Optional) | 00      |
| 90      |   1 | Control Rx3 App Select    | Software Application Select per SFF-8079, Rx Channel 3 (Optional) | 00      |
| 91      |   1 | Control Rx2 App Select    | Software Application Select per SFF-8079, Rx Channel 2 (Optional) | 00      |
| 92      |   1 | Control Rx1 App Select    | Software Application Select per SFF-8079, Rx Channel 1 (Optional) | 00      |


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
| 103                       | 1                         | Mask TempAW                | Masking bit for Temperature alarm/warning and initialization complete                        | 00                        |                           |
| 104                       | 1                         | Mask VccAW                 | Masking bit for Vcc alarm/warning                                                            | 00                        |                           |
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


| 139     |   1 | Encoding                       | (64B66B)                                                                                                     | 05                                             |
|---------|-----|--------------------------------|--------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| 140     |   1 | BR, nominal                    | Nominal Bit Rate 10.3Gb/s                                                                                    | 67                                             |
| 141     |   1 | Extended RateSelect Compliance | Tags for Extended RateSelect compliance                                                                      | 00                                             |
| 142     |   1 | Length(SMF)                    | Link length supported for SMF fiber in km                                                                    | 00                                             |
| 143     |   1 | Length (E-50µm)                | Link length supported for EBW 50/125 µm fiber, units of 2m                                                   | 00                                             |
| 144     |   1 | Length (50 µm)                 | Link length supported for 50/125 µm fiber, units of 1m                                                       | 00                                             |
| 145     |   1 | Length (62.5 µm)               | Link length supported for 62.5/125 µm fiber, units of1 m                                                     | 00                                             |
| 146     |   1 | Length (Copper)                | Link length supported for copper, units of1m                                                                 | -                                              |
| 147     |   1 | Device Tech                    | Copper cable unequalized                                                                                     | A0                                             |
| 148-163 |  16 | Vendorname                     | MODULETEK                                                                                                    | 4D 4F 4455 4C 45 54 45 4B 20 20 20 20 20 20 20 |
| 164     |   1 | Extended Transceiver           | Extended Transceiver Codes for InfiniBand                                                                    | 00                                             |
| 165-167 |   3 | Vendor OUI                     | QSFP vendor IEEE company ID                                                                                  | 00 00 00                                       |
| 168-183 |  16 | VendorPN                       | Part number in Order information                                                                             | -                                              |
| 184-185 |   2 | Vendor rev                     | Revision level for part number provided by vendor (ASCII)                                                    | -                                              |
| 186-187 |   2 | Wavelength                     | Nominal laser wavelength (Wavelength = value / 20 in nm)                                                     | -                                              |
| 188-189 |   2 | Wavelength Tolerance           | Guaranteed range of laser wavelength (+/- value) from Nominal wavelength.(Wavelength Tol. = value/200 in nm) | -                                              |
| 190     |   1 | Max Case Temp                  | Maximum Case Temperature in Degrees C.                                                                       | 46                                             |
| 191     |   1 | CC BASE                        | Check code for Base ID Fields (addresses 128-190)                                                            | -                                              |


| 192-195                   | 4                         | Options                     | Rate Select, TX Disable, TX Fault, LOS, Warning indicators for: Temperature, VCC, RX power, TXBias      | 0B 00 00 00                    |                           |
|---------------------------|---------------------------|-----------------------------|---------------------------------------------------------------------------------------------------------|--------------------------------|---------------------------|
| 196-211                   | 16                        | VendorSN                    | Serial number provided by vendor                                                                        | Programme d by                 |                           |
| 212-219                   | 8                         | Date Code                   | Year,Month,Day                                                                                          | Factory Programme d by Factory |                           |
| 220                       | 1                         | Diagnostic Monitoring Type  | Indicates which types of diagnostic monitoring are implemented (if any) in the Module. Bit 1,0 Reserved | 2E                             |                           |
| 221                       | 1                         | Enhanced options            | Indicates which optional enhanced features are implemented in the Module.                               | 00                             |                           |
| 222                       | 1                         | Reserved                    | Reserved                                                                                                | -                              |                           |
| 223                       | 1                         | CC EXT                      | Check code for the Extended ID Fields (addresses 192-222)                                               | -                              |                           |
| 224-255                   | 32                        | Vendor Specific             | Vendor SpecificEEPROM                                                                                   | -                              |                           |
| Upper Memory Map Page 02h | Upper Memory Map Page 02h | Upper Memory Map Page 02h   | Upper Memory Map Page 02h                                                                               | Upper Memory Map Page 02h      | Upper Memory Map Page 02h |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)                   | Remarks                   |
| 128-255                   | 128                       | Upper Memory Map            | User Code Area                                                                                          | -                              |                           |
| Upper Memory Map Page 8Ah | Upper Memory Map Page 8Ah | Upper Memory Map Page 8Ah   | Upper Memory Map Page 8Ah                                                                               | Upper Memory Map Page 8Ah      | Upper Memory Map Page 8Ah |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)                   | Remarks                   |
| 128-131                   | 4                         | Firmware Version Number[4]  | Firmware VersionNumber                                                                                  | -                              |                           |
| 132-135                   | 4                         | Datasheet Version Number[4] | Datasheet VersionNumber                                                                                 | -                              |                           |
| 136                       | 1                         | Security Level              | Security Level ： 00=Normal Mode ； 01=User Mode （ level 1 ）； 02=Factory Mode （ level 2 ）；        | -                              |                           |
| 137-138                   | 2                         | Vcc ADC                     | Vcc ADC                                                                                                 | -                              | 1                         |
| 139-140                   | 2                         | Temp ADC                    | Temp ADC                                                                                                | -                              | 1                         |
| Upper Memory Map Page F0h | Upper Memory Map Page F0h | Upper Memory Map Page F0h   | Upper Memory Map Page F0h                                                                               | Upper Memory Map Page F0h      | Upper Memory Map Page F0h |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)                   | Remarks                   |
| 128-131                   | 4                         | Password1 long              | Level 1 Password                                                                                        | 00 00 10 11                    |                           |

## Notes ：

1.Password entry area Default 00000000 ， read out as last written value

2.Page 00 and page 02 with write protection ， enter the security level 1 writeable


## User Mode

| Module        |   Level 1 Default Password | Password Can Be Changed   | Permissions                    |
|---------------|----------------------------|---------------------------|--------------------------------|
| QSFP28-QSFP28 |                   00001011 | YES(A0 TF0)               | 1 、 Read And Write A0 T00/T02 |
| QSFP28-QSFP28 |                   00001011 | YES(A0 TF0)               | 3 、 Read And Write A0 TF0     |

## Cable Specifications

| Parameter       | Symbol   | Min   |   Typ | Max   | Unit   | Remarks   |
|-----------------|----------|-------|-------|-------|--------|-----------|
| Wire Gauge      |          | 30AWG |       | 26AWG | AWG    |           |
| Cable Impedance | Z        | 90    |   100 | 110   | Ohm    |           |

## Insertion loss level

| Part Number                          | Insertion loss level   |
|--------------------------------------|------------------------|
| DAC-QSFP28-QSFP28-P-30AWG-1M-D1D1C   | CA-25G-N               |
| DAC-QSFP28-QSFP28-P-30AWG-2M-D1D1C   | CA-25G-N               |
| DAC-QSFP28-QSFP28-P-28AWG-2.5M-D1D1C | CA-25G-N               |
| DAC-QSFP28-QSFP28-P-28AWG-3M-D1D1C   | CA-25G-S               |
| DAC-QSFP28-QSFP28-P-26AWG-5M-D1D1C   | CA-25G-L               |

## Note:

1.Cable insertion loss classification standard ： IEEE 802.3by 110-10


## Typical S parameter

## 1m 30AWG typical insertion loss curve

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000010_b0df5ef735129f92301b656ba05520c3bf2db0b7b0251256b36981782d6c283a.png)

## 1m 30AWG typical reflection curve

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000011_722217541077e523128fa2d22a07837c076e676aff5b1fcd06a95beee119dfea.png)


## 3m 28AWG typical insertion loss curve

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000013_bced82ec8a0733f12df084583c8db2d0d7674512ce952ff3c73ddb4ca0afd800.png)

## 3m 28AWG typical reflection curve

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000014_c7d76f3975f3896bf88ac742e0bf211b7e2a38004727796f7fd6759ce8b36f45.png)


## 5m 26AWG typical insertion loss curve

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000016_57d3c577fec8a8faebbe99a2b6c9de933647a694dfe470ac52afb413464a0f62.png)

## 5m 26AWG typical reflection curve

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000017_26c2affd767a674743497f4e7e8c41b3613c61d814ca236c4c9d892551108f54.png)

## Note ：

1. Insertion loss standard reference IEEE802.3bj 92.10.2 ： IL&lt;22.48dB@12.89 GHz
2. Reflection curve standard reference IEEE802.3bj 92.10.3 ： SDDxx(dB)=16.5 - 2 × SQRT(f), 0.05 ≤ f &lt; 4.1GHz.
3. Reflection curve standard reference IEEE802.3bj 92.10.3 ： SDDxx(dB)=10.66 - 14 × log10(f/5.5),
4. 4.1 ≤ f ≤ 19GHz.


## Weight

| Parameter            | Symbol   |   Typ | Unit   |   Remarks |
|----------------------|----------|-------|--------|-----------|
| 30AWG Product Weight | G D30    | 145   | g/PCS  |         1 |
| 28AWG Product Weight | G D28    | 175   | g/PCS  |         1 |
| 26AWG Product Weight | G D26    | 190   | g/PCS  |         1 |
| 30AWG Cable Weight   | G C30    |  64   | g/M    |           |
| 28AWG Cable Weight   | G C28    |  94   | g/M    |           |
| 26AWG Cable Weight   | G C26    | 110   | g/M    |           |
| Dust Cap Weight      | G Q      |   1.4 | g/PCS  |           |

## Notes ：

1.The weight of DAC-QSFP28-QSFP28-P-xxAWG-1M-D1D1C.For example:The weight of DAC-QSFP28-QSFP28-P-26AWG-5M-D1D1C       is:190+110*(5-1)+1.4*2=632.8g

## Dimensions

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000019_171e382db47c2277ec2b1aa979146bea669ebce4f1f9a0328ef99e64ba4c251c.png)

ALL DIMENSIONS ARE ± 0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


## Cable dimension

|   serial number |   Standard Wire GaugeAWG |   Cable diameter OD(mm) |   Minimum bending radius R (mm) |
|-----------------|--------------------------|-------------------------|---------------------------------|
|               1 |                       30 |                     6.9 |                              35 |
|               2 |                       28 |                     8.4 |                              42 |
|               3 |                       26 |                     9.2 |                              45 |

## Length tolerance

|   Serial number | Nominal length L1 (m)   |   Tolerance range±(cm) |
|-----------------|-------------------------|------------------------|
|               1 | L1 ≤ 3                  |                      2 |
|               2 | 3 < L1 ≤ 4              |                      4 |
|               3 | 4 < L1 ≤ 5              |                      6 |


## Electrical Pad Layout

Top of Board

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000022_0c5bd35ae49fba84f3aab0e4a3b3868f4dd2276e942786c81bc2344825635a7c.png)

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000023_79f9d9eff533d85ecdea7890c711dbde11bcca232f7cd854d04a3e7d6c71034f.png)

Bottom of Board

![Image](/DAC/DAC-100-xM/DAC-100-xM_artifacts/image_000024_73497be32d3a988d104ecf0f17116efe411bc1e37c083c623e5094712cb1220e.png)


## Pin Assignment

|   PIN # | Symbol   | Description                                                                            |   Remarks |
|---------|----------|----------------------------------------------------------------------------------------|-----------|
|       1 | GND      | Ground                                                                                 |         5 |
|       2 | Tx2n     | Transmitter Inverted Data Input,LAN2                                                   |           |
|       3 | Tx2p     | Transmitter Non-Inverted Data Input,LAN2                                               |           |
|       4 | GND      | Ground                                                                                 |         5 |
|       5 | Tx4n     | Transmitter Inverted Data Input,LAN4                                                   |           |
|       6 | Tx4p     | Transmitter Non-Inverted Data Input,LAN4                                               |           |
|       7 | GND      | Ground                                                                                 |         5 |
|       8 | ModSelL  | Module select pin, the module responds to two-wire serial communication when low level |         1 |
|       9 | ResetL   | Module Reset                                                                           |         2 |
|      10 | V cc R X | +3.3V Power Supply Receiver                                                            |           |
|      11 | SCL      | 2-wire serial interface clock                                                          |           |
|      12 | SDA      | 2-wire serial interface data                                                           |           |
|      13 | GND      | Ground                                                                                 |         5 |
|      14 | Rx3p     | Receiver Non-Inverted Data Output,LAN3                                                 |           |
|      15 | Rx3n     | Receiver Inverted Data Output, LAN3                                                    |           |
|      16 | GND      | Ground                                                                                 |         5 |
|      17 | Rx1p     | Receiver Non-Inverted Data Output,LAN1                                                 |           |
|      18 | Rx1n     | Receiver Inverted Data Output, LAN1                                                    |           |
|      19 | GND      | Ground                                                                                 |         5 |
|      20 | GND      | Ground                                                                                 |         5 |
|      21 | Rx2n     | Receiver Inverted Data Output, LAN2                                                    |           |
|      22 | Rx2p     | Receiver Non-Inverted Data Output,LAN2                                                 |           |
|      23 | GND      | Ground                                                                                 |         5 |
|      24 | Rx4n     | Receiver Inverted Data Output, LAN4                                                    |           |
|      25 | Rx4p     | Receiver Non-Inverted Data Output,LAN4                                                 |           |
|      26 | GND      | Ground                                                                                 |         5 |
|      27 | ModPrsL  | The module is inserted into the indicate pin andgrounded in the module.                |         3 |
|      28 | IntL     | Interrupt                                                                              |         4 |
|      29 | V cc T X | +3.3V Power Supply transmitter                                                         |           |
|      30 | V cc1    | +3.3V Power Supply                                                                     |           |
|      31 | LPMode   | Low Power Mode                                                                         |         5 |
|      32 | GND      | Ground                                                                                 |         5 |


|   33 | Tx3p   | Transmitter Non-Inverted Data Input,LAN3   |    |
|------|--------|--------------------------------------------|----|
|   34 | Tx3n   | Transmitter Inverted Data Input,LAN3       |    |
|   35 | GND    | Ground                                     |  5 |
|   36 | Tx1p   | Transmitter Non-Inverted Data Input,LAN1   |    |
|   37 | Tx1n   | Transmitter Inverted Data Input,LAN1       |    |
|   38 | GND    | Ground                                     |  5 |

## Notes:

1. ModSelL is the input pin. The module responds to 2-wire serial communication commands when it is held low by the host. ModSelL allows multiple QSFP modules to be used on a single 2-wire interface bus. If ModSelL is High, the module will not respond to any 2-wire interface communication from the host. ModSelL has internal  pull-up resistors in the module
2. The module restart pin, when the low level on the ResetL pin lasts longer than the minimum pulse length, resets the module and restores all user modules to their default state.  When performing reset device, the host should ignore all status bits. Until the module reset interrupt is completed, please note that during hot plugging, the module will issue this information to complete the reset interrupt without resetting
3. This pin is active high, indicating that the module is running under a low power module.
4.  IntL is the output pin, which is the open collector output and must be pulled up to Vcc on the motherboard. When it is low, it indicates that the module may malfunction. The host uses a 2-wire serial interface to identify the interrupt source
5. 5.Circuit ground is internally isolated from chassis ground.

## References

1. IEEE standard 802.3bj. IEEE Standard Department.
2. IEEE standard 802.3by. IEEE Standard Department.