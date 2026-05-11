
## DATA SHEET

## MODULETEK : DAC-QSFP-40G-P-xxAWG-aa.aaM-D1D1B

QSFP 40G Passive Copper Cable Assembly

## Overview

ModuleTek's 40G passive cable uses shielded high-speed differential cables,Compliant with 40G Ethernet standard and QSFP Multi-Source Agreement (MSA) standard, it supports 40G transmission rate and can be backward compatible with various speeds. QSFP 40G passive cables are the preferred solution for short-haul applications. They are commonly used for data transmission between data centers and cabinets or adjacent cabinets. The biggest features are low cost, ultra-low power consumption (less than 0.1 watts) and high reliability.

## Product Features

- Up to 40Gb/s bi-directional data links
- Compliant with QSFP+ MSA specifications
- Fully Compliant with IEEE802.3ba
- Fully Compliant with Infiniband QDR specifications
- 4 independent duplex channels operating at 10Gbps
- Support for 2.5Gbps,5Gbps data rates
- AC coupled inputs and outputs
- 100 Ohm differential impedance
- All-metal housing for superior EMI performance
- Single power supply 3.3V, low power consumption
- RoHS Compliant
- Operating temperature range: 0 ◦ C to 70 ◦ C

## Applications

40Gigabit Ethernet Serial Data Transmission

QDR

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000001_7729c08061f6156323f038ec3f2ba9807b1da0b951981a202b85f20d4bc5eac1.png)


## Ordering Information

| Part Number                        | Product ID   | Description                        | Gauge   | Length   |
|------------------------------------|--------------|------------------------------------|---------|----------|
| DAC-QSFP-40G-P-30AWG- aa.aaM-D1D1B | M458606      | QSFP 40G Passive Cable , aa.aa ≤ 3 | 30AWG   | ≤ 3m     |
| DAC-QSFP-40G-P-28AWG- aa.aaM-D1D1B | M051506      | QSFP 40G Passive Cable, aa.aa ≤ 7  | 28AWG   | ≤ 7m     |

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
| Bit Error Rate        | BER      |        |       | 10 - 12 |        |           |
| Operating Temperature | T C      |   0    |       | 70      | ◦ C    |         1 |
| Storage Temperature   | T STO    | -40    |       | 85      | ◦ C    |         2 |
| Input Voltage         | V CC     |   3.14 |   3.3 | 3.46    | V      |           |

## Notes:

- 1.Case temperature

2.Ambient temperature

## I2C Memory Map

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


| 131-138   |   8 | Tranceiver                     | 40GBASE-CR4                                                                                                  | 08 00 00 00 00 00 00 00                         |
|-----------|-----|--------------------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| 139       |   1 | Encoding                       | (64B66B)                                                                                                     | 05                                              |
| 140       |   1 | BR, nominal                    | Nominal Bit Rate 10.3Gb/s                                                                                    | 67                                              |
| 141       |   1 | Extended RateSelect Compliance | Tags for Extended RateSelect compliance                                                                      | 00                                              |
| 142       |   1 | Length(SMF)                    | Link length supported for SMF fiber in km                                                                    | 00                                              |
| 143       |   1 | Length (E-50µm)                | Link length supported for EBW 50/125 µm fiber, units of 2 m                                                  | 00                                              |
| 144       |   1 | Length (50 µm)                 | Link length supported for 50/125 µm fiber, units of 1 m                                                      | 00                                              |
| 145       |   1 | Length (62.5 µm)               | Link length supported for 62.5/125 µm fiber, units of 1 m                                                    | 00                                              |
| 146       |   1 | Length (Copper)                | Link length supported for copper, units of 1m                                                                | -                                               |
| 147       |   1 | Device Tech                    | Copper cable unequalized                                                                                     | A0                                              |
| 148-163   |  16 | Vendor name                    | MODULETEK                                                                                                    | 4D 4F 44 55 4C 45 54 45 4B 20 20 20 20 20 20 20 |
| 164       |   1 | Extended Transceiver           | Extended Transceiver Codes for InfiniBand                                                                    | 00                                              |
| 165-167   |   3 | Vendor OUI                     | QSFP vendor IEEE company ID                                                                                  | 00 00 00                                        |
| 168-183   |  16 | Vendor PN                      | Part number in Order information                                                                             | -                                               |
| 184-185   |   2 | Vendor rev                     | Revision level for part number provided by vendor (ASCII)                                                    | -                                               |
| 186-187   |   2 | Wavelength                     | Nominal laser wavelength (Wavelength = value / 20 in nm)                                                     | -                                               |
| 188-189   |   2 | Wavelength Tolerance           | Guaranteed range of laser wavelength (+/- value) from Nominal wavelength.(Wavelength Tol. = value/200 in nm) | -                                               |
| 190       |   1 | Max Case Temp                  | Maximum Case Temperature in Degrees C.                                                                       | 46                                              |
| 191       |   1 | CC BASE                        | Check code for Base ID Fields (addresses 128-190)                                                            | -                                               |


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
| 137-138                   | 2                         | Vcc ADC                     | Vcc ADC                                                                                                 | -                         | 1                         |
| 139-140                   | 2                         | Temp ADC                    | Temp ADC                                                                                                | -                         | 1                         |
| Upper Memory Map Page F0h | Upper Memory Map Page F0h | Upper Memory Map Page F0h   | Upper Memory Map Page F0h                                                                               | Upper Memory Map Page F0h | Upper Memory Map Page F0h |
| IIC Addr                  | Size                      | Name                        | Description                                                                                             | Values (HEX)              | Remarks                   |
| 128-131                   | 4                         | Password1 long              | Level 1 Password                                                                                        | 00 00 10 11               |                           |

## Notes ：

1.Password entry area are write-only bits ， read out always 00000000

2.Page 00 and page 02 with write protection ， enter the security level 1 writeable


## User Mode

| Level 1 Default Password   | Password Can Be Changed   | Permissions                    |
|----------------------------|---------------------------|--------------------------------|
| 00 00 10 11                | YES(A0 TF0)               | 1 、 Read And Write A0 T00/T02 |
| 00 00 10 11                | YES(A0 TF0)               | 2 、 Read A0 T8A               |
| 00 00 10 11                | YES(A0 TF0)               | 3 、 Read And Write A0 TF0     |


## Typical S parameter

## 3m 30AWG typical insertion loss curve

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000010_bcf8d6c10a1774341135a70f10687df9ad41aab1df00aefbf24cb0487b85e0a9.png)

## 3m 30AWG typical reflection curve

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000011_dd6bf66608190ec978442bfa6ac50491e9a5d00f41af7c763d96d1d852d22da4.png)


duleTek

Moc

## 5m 28AWG typical insertion loss curve

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000013_093b17254e3443929515bde76a386338656e466cd30d6fdc7fc9cfa7af2940f6.png)

## 5m 28AWG typical reflection curve

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000014_897cd057ef15f60bb68e9a7969a964aefdceb4ef0bbe2db9acc494bb3fe9441e.png)

## Note:

1. Insertion loss standard reference IEEE802.3ba 85.10.2 ： IL&lt;17.04dB@5.15625 GHz
2. Reflection curve standard reference IEEE802.3ba 85.10.4 ： SDDxx(dB)=12 - 2 × SQRT(f), 0.05 ≤ f &lt; 4.1GHz.
3. Reflection curve standard reference IEEE802.3ba 85.10.4 ： SDDxx(dB)=6.3 - 13 × log10(f/5.5), 4.1 ≤ f ≤ 10GHz.


duleTek

Moc

## Weight

| Parameter            | Symbol   |   Typ | Unit   |   Remarks |
|----------------------|----------|-------|--------|-----------|
| 30AWG Product Weight | G D30    | 140   | g/PCS  |         1 |
| 28AWG Product Weight | G D28    | 160   | g/PCS  |         1 |
| 30AWG Cable Weight   | G C30    |  62   | g/M    |           |
| 28AWG Cable Weight   | G C28    |  76   | g/M    |           |
| Dust Cap Weight      | G Q      |   1.4 | g/PCS  |           |

## Notes ：

1.The weight of DAC-QSFP-40G-P-xxAWG-1M-D1D1B.For example:The weight of DAC-QSFP-40G-P-28AWG-5M-D1D1B is:160+76* （ 5-1 ） +1.40*2=466.8g.

## Dimensions

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000016_381136ef7197029c69c1095b77bff31d71eb3d23bb781aa4176e45b5055ee0e5.png)

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm


## Cable Specifications

| Parameter       | Symbol   |   Min |   Typ |   Max | Unit   | Remarks   |
|-----------------|----------|-------|-------|-------|--------|-----------|
| Wire Gauge      |          |    30 |       |    28 | AWG    |           |
| Cable Impedance | Z        |    90 |   100 |   110 | Ohm    |           |

## Cable dimension

|   serial number |   Standard Wire Gauge AWG |   Cable diameter OD (mm) |   Minimum bending radius R (mm) |
|-----------------|---------------------------|--------------------------|---------------------------------|
|               1 |                        30 |                      6.6 |                              30 |
|               2 |                        28 |                      7.5 |                              40 |

## Length tolerance

|   Serial number | Nominal length L1 (m)   |   Tolerance range ±(cm) |
|-----------------|-------------------------|-------------------------|
|               1 | L1 ≤ 2                  |                       2 |
|               2 | 2 < L1 ≤ 4              |                       4 |
|               3 | 4 < L1 ≤ 6              |                       6 |
|               4 | 6 < L1 ≤ 7              |                       8 |


duleTek

Moc

## Electrical Pad Layout

Top View

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000019_a6eeaa8809f4b2a26a9bfdd415dba3c202c0861f4108943b1ffa10862c85f6be.png)

Bottom View

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000020_5900754404a052ff92b5f7aa611e2f7fa7ec9e7d905ca7961a12b601c8c6147d.png)

![Image](/DAC/DAC-40-xM/DAC-40-xM_artifacts/image_000021_54e0aa1800fecbceb9b940b85ace11b2bf7a9609eb45cfb4b2522210b21c5d28.png)


## Pin Assignment

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
|      10 | V cc R X | +3.3V Power Supply Receiver                                                            |           |
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
|      29 | V cc T X | +3.3V Power Supply transmitter                                                         |           |
|      30 | V cc1    | +3.3V Power Supply                                                                     |           |
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
3. This pin is active high, indicating that the module is running under a low power module.
4. IntL is the output pin, which is the open collector output and must be pulled up to Vcc on the motherboard. When it is low, it indicates that the module may malfunction. The host uses a 2-wire serial interface to identify the interrupt source
5. 5.Circuit ground is internally isolated from chassis ground.

## References

1. IEEE standard 802.3ba. IEEE Standard Department.