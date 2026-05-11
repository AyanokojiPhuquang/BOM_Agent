
## DATA SHEET

## MODULETEK: AOC-SFP-100G-aaa.aaM-D3D3C

100Gb/s SFP Active Optical Cable

## Overview

AOC-SFP-100G-aaa.aaM-D3D3C active optical cables are based on 100G Ethernet IEEE 802.3 stan-  dard.  They  are  compliant  with  FC-PI-6 、 SFF-8402 、 SFF-8419 、 SFF-8432  and  SFF-8472, providing  a  fast  and  reliable  interface  for  100G  Ethernet  applications.  The  product implements the digital diagnostics required by the SFF-8472 via a 2-wire serial bus.

## Product Features

- Up to 100Gbps bi-directional data links
- Compliant with IEEE 802.3
- Compliant with FC-PI-6
- Compliant with SFF-8402
- Compliant with SFF-8419
- Compliant with SFF-8432
- Compliant with SFF-8472
- Hot-pluggable SFP footprint
- 850nm VCSEL laser transmitter and PIN receiver
- Built-in digital diagnostic functions
- Up to 100m in length
- RoHS6 Compliant
- Single power supply 3.3V
- Low power consumption (module working power &lt;0.5W@Single-end)
- Operating temperature range: 0 ◦ C to70 ◦ C(case temperature)

![Image](/AOC/AOC-100-xM/AOC-100-xM_artifacts/image_000001_a1ac516ba964c61de2d97c7db14d0724cf8be5e94a69e431d24bde46b320a4c8.png)

## Applications

- 100G Ethernet Data Center Intra-Rack and Inter-Rack links


## Ordering Information

| Part Number                 | Product ID   | Description                                            | Color on Clasp   |
|-----------------------------|--------------|--------------------------------------------------------|------------------|
| AOC-SFP-100G-aaa.aaM- D3D3C | M496804      | 100G SFP Active Optical Cable, Length 0.5 ∼ 100 meters | Blue             |

## Notes ：

1.  Product ID is the abbreviated order number of our company's product standard model
2.  Model AOC-SFP-100G-aaa.aaM-D3D3C, where aaa.aaM refers to the length of the AOC cable

## For More Information Or To Order The Above Products, Please Contact:

Email: sales@moduletek.com

ModuleTek Web: www.moduletek.com

## General Specifications

| Parameter                  | Symbol   |    Min |    Typ | Max      | Unit   |   Remarks |
|----------------------------|----------|--------|--------|----------|--------|-----------|
| Data Rate                  | DR       |        |  25.78 |          | Gb/s   |         1 |
| Bit Error Rate             | BER      |        |        | 5x10 - 5 |        |         2 |
| Operating Temperature      | T C      |   0    |        | 70       | ◦ C    |         3 |
| Storage Temperature        | T STO    | -40    |        | 85       | ◦ C    |         4 |
| Supply Current             | I CC     |        | 145    | 290      | mA     |         5 |
| Input Voltage              | V CC     |   3.15 |   3.3  | 3.46     | V      |           |
| Maximum Voltage            | V MAX    |  -0.5  |        | 4        | V      |         5 |
| Product Weight             |          |        |  51.6  |          | g/PCS  |         6 |
| Fiber Optical Cable Weight |          |        |   6.95 |          | g/M    |         7 |

## Notes:

1. IEEE 802.3
2. Measured with data rate at 100Gbps, PRBS 2 31 -1
3. Case temperature
4. Ambient temperature
5. For electrical power interface
6. The weight of AOC-SFP-100G-1M-D3D3C
7. The weight of fiber optical cable per unit length

Specifications


## Electrical Characteristics - Transmitter

V CC =3.15V to 3.46V,T C =0 ◦ C to 70 ◦ C

| Parameter                     | Symbol   | Min   |   Typ | Max        | Unit   | Remarks   |
|-------------------------------|----------|-------|-------|------------|--------|-----------|
| Input differential impedance  | R IN     |       |   100 |            | Ω      |           |
| Differential data input swing | V IN PP  | 180   |       | 1600       | mV     |           |
| Transmit Disable Voltage      | V D      | 2     |       | V CC       | V      |           |
| Transmit Enable Voltage       | V EN     | V EE  |       | V EE + 0.8 | V      |           |

## Electrical Characteristics - Receiver

V CC =3.15V to 3.46V,T C =0 ◦ C to 70 ◦ C

| Parameter                      | Symbol   | Min   |   Typ | Max        | Unit   | Remarks   |
|--------------------------------|----------|-------|-------|------------|--------|-----------|
| Differential data output swing | V OUT PP | 370   |   600 | 850        | mV     |           |
| LOS Fault                      | V LOS A  | 2     |       | V CC HOST  | V      |           |
| LOS Normal                     | V LOS D  | V EE  |       | V EE + 0.8 | V      |           |

## Digital Diagnostic Functions

AOC-SFP-100G-aaa.aaM-D3D3C supports the  2-wire  serial  communication  protocol  defined  in SFF- 8472, which accesses digital diagnostic information through a 2-wire interface with the address 0xA2.  The  digital  diagnosis  defaults  to  internal  calibration,  and  the  internal  micro-control  unit accesses  the  module  operating  parameters  in  real  time,  such  as  module  temperature,  laser  bias current, emission power, received light power and module power supply voltage. The module realizes the alarm function of SFF-8472, which sets the alarm flag bit when the specific working parameters are  out  of  the  normal  range,  and  cancels the  alarm flag bit when  the specific  working  parameters return to the normal range.

## Digital Diagnostic Threshold Range

| Parameter         | High Alarm   | High Warning   | Low Warning   | Low Alarm     |
|-------------------|--------------|----------------|---------------|---------------|
| Temperature( ◦ C) | 75.00(4B00h) | 70.00(4600h)   | 0.00(0000h)   | -5.00(FB00h)  |
| Voltage(V)        | 3.63(8DCCh)  | 3.46(8728h)    | 3.13(7A44h)   | 2.97(7404h)   |
| Bias Current(mA)  | 12.00(1770h) | 11.50(1676h)   | 2.00(03E8h)   | 1.00(01F4h)   |
| Tx Power(dBm)     | 3.40(5575h)  | 2.40(43E2h)    | -8.40(05A5h)  | -9.40(047Ch)  |
| Rx Power(dBm)     | 3.40(5575h)  | 2.40(43E2h)    | -10.30(03A5h) | -11.30(02E5h) |

Specifications


## A0h 、 A2h Write Protection

| Security Level 1 Password (Factory value)   | Security Level 1 Password (Factory value)   | Security Level 1 Password (Factory value)   |
|---------------------------------------------|---------------------------------------------|---------------------------------------------|
| Password Entry ADDr                         | Size                                        | Vaules(HEX)                                 |
| Page A2h, 7Bh-7Eh                           | 4                                           | 00 00 10 11                                 |
| Change Security Level 1 Password            | Change Security Level 1 Password            | Change Security Level 1 Password            |
| Change Password Entry ADDr                  | Size                                        | Vaules(HEX)                                 |
| Page A2h, Table F0h ， 80h-83h              | 4                                           | Programmed by User                          |

AOC-SFP-100G-aaa.aaM-D3D3C has write protection functions of A0h and A2h, and users can enter the working state of security level 1 and write to the address of module device A0h and table 00h, table 01h and table F0h of A2h. The method to enter the working state of security level 1 is to write the security level 1 password in the 7Bh-7Eh register of the module A2h address in turn. After entering the security level 1, the user can directly write the contents of the A0h device address, or by modifying the contents of the 7Fh table selection register in the A2h address, write to table 00h or table 01h or table F0h. This version module supports users to modify the password of security level 1 by writing a new security level 1 password in the 80h-83h register in the device address F0h table of module A2h.

## IIC Memory Map(Page A0 HEX, Unlisted Fields are Blank/Empty)

| IIC ADDr   |   Size | Name                             | Description                               | Vaules(HEX)                         |
|------------|--------|----------------------------------|-------------------------------------------|-------------------------------------|
| 0          |      1 | Identifier                       | SFP                                       | 03                                  |
| 1          |      1 | Ext. Identifier                  | Two-wire Interface                        | 04                                  |
| 2          |      1 | Connector                        | No separable connector                    | 23                                  |
| 3-10       |      8 | Transceiver                      | 25G Base AOC                              | 00 00 00 00 00 08 00 00             |
| 11         |      1 | Encoding                         | Not Explicitly Specified                  | 00                                  |
| 12         |      1 | BR,Nominal                       | Nominal Bit Rate 25.78Gbps                | FF                                  |
| 13         |      1 | Rate Identifier                  | Type of rate select functionality         | 00                                  |
| 14         |      1 | Length(9um)-km                   | Link Length in Thousands of Meters/SMF=NA | 00                                  |
| 15         |      1 | Length(9um)-100m                 | Link Length in Hundreds of Meters/SMF=NA  | 00                                  |
| 16         |      1 | Length(50um)-10m                 | 50-micron MMFLink Length=NA               | 00                                  |
| 17         |      1 | Length(62.5um)- 10m              | 62.5-micron MMFLink Length=NA             | 00                                  |
| 18         |      1 | Length(Active Cable or Copper)-m | Cable Length-m                            | According to the needs of customers |
| 19         |      1 | Length(Active Cable or Copper)-m | Cable Length-m                            | 00                                  |
| 20-35      |     16 | Vendor name                      | MODULETEK                                 | ASCII Format                        |
| 36         |      1 | Transceiver                      | 25G Base AOC                              | 01                                  |
| 37-39      |      3 | Vendor OUI                       | SFP Vendor IEEE Company ID                | 00 00 00                            |

Specifications


Specifications

| 40-55   |   16 | Vendor PN                  | The Part number in the Ordering Information                                                                                                                                                                                                                                                               | ASCII Format          |
|---------|------|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| 56-59   |    4 | Vendor rev                 | Programmed by Factory                                                                                                                                                                                                                                                                                     | Programmed by Factory |
| 60-61   |    2 | Wavelength                 | Unallocated                                                                                                                                                                                                                                                                                               | 00 00                 |
| 62      |    1 | Reserved                   | Unallocated                                                                                                                                                                                                                                                                                               | 00                    |
| 63      |    1 | CC_BASE                    | Check sum of bytes 0-62                                                                                                                                                                                                                                                                                   | Programmed by Factory |
| 64      |    1 | Transceiver Options        | BIT7=0 Reserved BIT6=0 Reserved BIT5=0 The module power level is 1(Less than 1.0w) BIT4=1 Paging implemented function BIT3=1 Retimer or CDR indicator BIT2=0 A uncooled laser transmitter implementation BIT1=0 The module power Level is 1(Less than 1.0w) BIT0=0 Aconventional limiting receiver output | 18                    |
| 65      |    1 | Transceiver Options        | BIT7=0 Receiver decision threshold implemented is not realized BIT6=0 Tunable wavelength lasers are not used BIT5=0 RATE_SELECT functionality is not realized BIT4=1 Have TX_DIS function BIT3=1 Have TX_Fault function BIT2=0 Loss of Signal is not realized BIT1=1 Have RX_LOS function BIT0=0 Reserved | 1A                    |
| 66      |    1 | BR,max                     | Maximum signal rate                                                                                                                                                                                                                                                                                       | 67                    |
| 67      |    1 | BR,min                     | Maximum signal rate deviation                                                                                                                                                                                                                                                                             | 00                    |
| 68-83   |   16 | Vendor SN                  | Vendor SN                                                                                                                                                                                                                                                                                                 | Programmed by Factory |
| 84-91   |    8 | Date code                  | Year,Month,Day                                                                                                                                                                                                                                                                                            | Programmed by Factory |
| 92      |    1 | Diagnostic Monitoring Type | BIT7=0 Compatible with SFF-8472 requirements BIT6=1 Realize digital diagnostic function BIT5=1 Realized internal calibration function BIT4=0 Externally calibration is not realized BIT3=1 Received power is the averaged power BIT2=0 Don't need address change BIT1=0 Reserved BIT0=0 Reserved          | 68                    |


Specifications

| 93      |   1 | Enhanced Options    | BIT7=1 Have optional Alarm/Warning flags implementes function BIT6=1 Have soft TX_DIS monitor and control functions BIT5=1 Have soft TX_Fault monitor function BIT4=1 Have soft RX_LOS monitor function BIT3=0 No software RATE_SEL monitor and control functions BIT2=0 The optional soft rate selection control funtion is not implemented by SFF-8079 BIT1=0 The optional soft rate selection control funtion is not implemented by SFF-8431 BIT0=0 Reserved   | F0                    |
|---------|-----|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| 94      |   1 | SFF-8472 Compliance | As defined by SFF8472 version 12.3                                                                                                                                                                                                                                                                                                                                                                                                                                | 08                    |
| 95      |   1 | CC_BASE             | Check sum of bytes 64-94                                                                                                                                                                                                                                                                                                                                                                                                                                          | Programmed by Factory |
| 96-127  |  32 | Vendor Specific     | Vendor SpecificEEPROM                                                                                                                                                                                                                                                                                                                                                                                                                                             | Programmed by Factory |
| 128-255 | 128 | Reserved            | Vendor Specific                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Programmed by Factory |

## IIC Memory Map(Page A2 HEX LOW, Unlisted Fields are Blank/Empty)

| IIC ADDr      | Size          | Name                 | Description              | Vaules(HEX)                   |
|---------------|---------------|----------------------|--------------------------|-------------------------------|
| Alarm/Warning | Alarm/Warning | Alarm/Warning        | Alarm/Warning            | Alarm/Warning                 |
| 00-01         | 2             | Temp High Alarm      | Temperature high alarm   | See Table Of Threshold Ranges |
| 02-03         | 2             | Temp Low Alarm       | Temperature low alarm    | See Table Of Threshold Ranges |
| 04-05         | 2             | TempHigh Warning     | Temperature high warning | See Table Of Threshold Ranges |
| 06-07         | 2             | TempLow Warning      | Temperature low warning  | See Table Of Threshold Ranges |
| 08-09         | 2             | Voltage High Alarm   | Voltage high alarm       | See Table Of Threshold Ranges |
| 10-11         | 2             | Voltage Low Alarm    | Voltage low alarm        | See Table Of Threshold Ranges |
| 12-13         | 2             | Voltage High Warning | Voltage high warning     | See Table Of Threshold Ranges |
| 14-15         | 2             | Voltage Low Warning  | Voltage low warning      | See Table Of Threshold Ranges |


Specifications

| 16-17                                                | 2                                                    | Bias High Alarm                                      | Bias current high alarm                              | See Table Of Threshold Ranges                        |
|------------------------------------------------------|------------------------------------------------------|------------------------------------------------------|------------------------------------------------------|------------------------------------------------------|
| 18-19                                                | 2                                                    | Bias Low Alarm                                       | Bias current low alarm                               | See Table Of Threshold Ranges                        |
| 20-21                                                | 2                                                    | Bias High Warning                                    | Bias current high warning                            | See Table Of Threshold Ranges                        |
| 22-23                                                | 2                                                    | Bias Low Warning                                     | Bias current low warning                             | See Table Of Threshold Ranges                        |
| 24-25                                                | 2                                                    | TXPower High Alarm                                   | TX power high alarm                                  | See Table Of Threshold Ranges                        |
| 26-27                                                | 2                                                    | TXPower Low Alarm                                    | TX power low alarm                                   | See Table Of Threshold Ranges                        |
| 28-29                                                | 2                                                    | TXPower High Warning                                 | TX power high warning                                | See Table Of Threshold Ranges                        |
| 30-31                                                | 2                                                    | TXPower Low Warning                                  | TX power low warning                                 | See Table Of Threshold Ranges                        |
| 32-33                                                | 2                                                    | RXPower High Alarm                                   | RX power high alarm                                  | See Table Of Threshold Ranges                        |
| 34-35                                                | 2                                                    | RXPower Low Alarm                                    | RX power low alarm                                   | See Table Of Threshold Ranges                        |
| 36-37                                                | 2                                                    | RXPower High Warning                                 | RX power high warning                                | See Table Of Threshold Ranges                        |
| 38-39                                                | 2                                                    | RXPower Low Warning                                  | RX power low warning                                 | See Table Of Threshold Ranges                        |
| 40-55                                                | 16                                                   | Optional A/W Thresholds                              | Unrealized                                           | -                                                    |
| Calibration Constant For External Calibration Option | Calibration Constant For External Calibration Option | Calibration Constant For External Calibration Option | Calibration Constant For External Calibration Option | Calibration Constant For External Calibration Option |
| 56-59                                                | 4                                                    | RX-PWR(4)                                            | The module only realizes internal correction funtion | 00 00 00 00                                          |
| 60-63                                                | 4                                                    | RX_PWR(3)                                            | The module only realizes internal correction funtion | 00 00 00 00                                          |
| 64-67                                                | 4                                                    | RX_PWR(2)                                            | The module only realizes internal correction funtion | 00 00 00 00                                          |
| 68-71                                                | 4                                                    | RX_PWR(1)                                            | The module only realizes internal correction funtion | 3F 80 00 00                                          |
| 72-75                                                | 4                                                    | RX_PWR(0)                                            | The module only realizes internal correction funtion | 00 00 00 00                                          |
| 76-77                                                | 2                                                    | TX_I(Slope)                                          | The module only realizes internal correction funtion | 01 00                                                |
| 78-79                                                | 2                                                    | TX_I(Offset)                                         | The module only realizes internal correction funtion | 00 00                                                |
| 80-81                                                | 2                                                    | TX_PWR(Slope)                                        | The module only realizes internal correction funtion | 01 00                                                |
| 82-83                                                | 2                                                    | TX_PWR(Offset)                                       | The module only realizes internal correction funtion | 00 00                                                |
| 84-85                                                | 2                                                    | T(Slope)                                             | The module only realizes internal correction funtion | 01 00                                                |


Specifications

| 86-87                      | 2                          | T(Offset)                  | The module only realizes internal correction funtion                                                                                                                                                                                                                      | 00 00                      |
|----------------------------|----------------------------|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| 88-89                      | 2                          | V(Slope)                   | The module only realizes internal correction funtion                                                                                                                                                                                                                      | 01 00                      |
| 90-91                      | 2                          | V(Offset)                  | The module only realizes internal correction funtion                                                                                                                                                                                                                      | 00 00                      |
| 92-94                      | 3                          | Unallocated                | -                                                                                                                                                                                                                                                                         | 00 00 00                   |
| 95                         | 1                          | Checksum                   | Byte 95 contains the low order 8 bits of the sum of bytes 0-94                                                                                                                                                                                                            | -                          |
| A/D Values And Status Bits | A/D Values And Status Bits | A/D Values And Status Bits | A/D Values And Status Bits                                                                                                                                                                                                                                                | A/D Values And Status Bits |
| 96-97                      | 2                          | Temperature MSB/LSB        | Temperature measured value                                                                                                                                                                                                                                                | Variable                   |
| 98-99                      | 2                          | Vcc MSB/LSB                | Voltage measured value                                                                                                                                                                                                                                                    | Variable                   |
| 100-101                    | 2                          | Tx Bias MSB/LSB            | Bias current measured value                                                                                                                                                                                                                                               | Variable                   |
| 102-103                    | 2                          | TX Power MSB/LSB           | Measured TX output power                                                                                                                                                                                                                                                  | Variable                   |
| 104-105                    | 2                          | RXPower MSB/LSB            | Measured RXinput power                                                                                                                                                                                                                                                    | Variable                   |
| 106-107                    | 2                          | Laser T/W MSB/LSB          | Function not implemented                                                                                                                                                                                                                                                  | 00 00                      |
| 108-109                    | 2                          | TECcurrent MSB/LSB         | Function not implemented                                                                                                                                                                                                                                                  | 00 00                      |
| 110                        | 1                          | Status/Control             | BIT7 TX_Dis Pin States BIT6 Soft TX_Dis Pin States BIT5 RS(1) Pin States BIT4 RS0 Pin States BIT3 Soft RS0 control bit BIT2 TX_Fault Pin States BIT1 Rx_LOS Pin States BIT0 Data_Ready_Bar Pin States                                                                     | Variable                   |
| 111                        | 1                          | Reserved                   | Reserved for SFF-8079                                                                                                                                                                                                                                                     | 00                         |
| 112                        | 1                          | Alarm Flags                | BIT7 Temp High Alarm BIT6 Temp Low Alarm BIT5 Vcc High Alarm BIT4 Vcc Low Alarm BIT3 TX Bias High Alarm BIT2 TX Bias Low Alarm BIT1 TX Power High Alarm BIT0 TX Power Low Alarm                                                                                           | Variable                   |
| 113                        | 1                          | Alarm Flags                | BIT7 RX Power High Alarm BIT6 RX Power Low Alarm BIT5-BIT2 Alarm bit not realized BIT1-BIT0 Reserved                                                                                                                                                                      | Variable                   |
| 114                        | 1                          | Tx InputEQ Control         | BIT7-BIT4 Hight-speed mode input equalization setting value; the default value for power-up is 3, which can be used to change the module input equalization value BIT3-BIT0 Low-speed modeinput equalization setting value; not used, the default value for power-up is 3 | 33                         |


Specifications

| 115                | 1                  | Rx Out Emphasis Control   | BIT7-BIT4 Hight-speed mode output emphasis setting value; the default value for power-up is 3, which can be used to change the module output emphasis value BIT3-BIT0 Low-speed mode output emphasis setting value; not used, the default value for power-up is 3                                                                                   | 33                             |
|--------------------|--------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|
| 116                | 1                  | Warning Flags             | BIT7 Temp High Warning BIT6 Temp Low Warning BIT5 Vcc High Warning BIT4 Vcc Low Warning BIT3TX Bias High Warning BIT2 TX Bias Low Warning BIT1TX Power High Warning BIT0 TX Power Low Warning                                                                                                                                                       | Variable                       |
| 117                | 1                  | Warning Flags             | BIT7 RX Power High Warning BIT6 RX Power Low Warning BIT5-BIT2 Warning bit not realized BIT1-BIT0 Reserved                                                                                                                                                                                                                                          | Variable                       |
| 118                | 1                  | Ext Status/Control        | BIT7-BIT4 BIT2 Reserved BIT3 Soft RS(1) control bit BIT1=0 The module power level is 1 (Less than 1.0w) BIT0=0 The module power level is 1 (Less than 1.0w)                                                                                                                                                                                         | The default for power-up is 00 |
| 119                | 1                  | Ext Status/Control        | BIT7-BIT5 Unallocated BIT4=0 Not Applicable BIT3=0 Not Applicable BIT2=0 Not Applicable BIT1 TX CDR status bit, a value of 0 indicates that the CDR is locked, whereas a value of 1 indicates loss of lock of the CDR BIT0 Rx CDR status bit, a value of 0 indicates that the CDR is locked, whereas a value of 1 indicates loss of lock of the CDR | Variable                       |
| General Use Fields | General Use Fields | General Use Fields        | General Use Fields                                                                                                                                                                                                                                                                                                                                  | General Use Fields             |
| 120-122            | 3                  | Reserved                  | Reserved                                                                                                                                                                                                                                                                                                                                            | 00 00 00                       |
| 123-126            | 4                  | Security Level Password   | Security level password input area, the written password can be displayed and the default value is 00 00 00 00                                                                                                                                                                                                                                      | 00 00 00 00                    |
| 127                | 1                  | Table Select              | Table Select                                                                                                                                                                                                                                                                                                                                        | 00                             |


## Block-Diagram-of-Transceiver

![Image](/AOC/AOC-100-xM/AOC-100-xM_artifacts/image_000011_64e7cd109a39c1583db0d7ae4661e9bafd13686cf4cc481d965c87bafef98fff.png)

## Functions Description

AOC-SFP-100G-aaa.aaM-D3D3C module is manufactured  by  advanced  COB  (Chip  on  Board) tech- nology and consists of a microcontroller, an optical engine at the transmitting end and an optical engine  at  the  receiving  end.  The  module  has  built-in  clock  and  data  recovery  functions,  and  the working rate range of the transmitter and receiver of the built-in CDR is 100Gbps. If you need another version of the rate range, you can contact us for special customization.

The microcontroller communicates with the host through a 2-wire serial communication interface, providing module control function, status reporting function and monitoring function (DOM). This product conforms to the SFF-8472 standard.

The transmitter optical engine includes a transmitter clock data recovery circuit (CDR) and a laser driver circuit (LD), a VCSEL laser, and a detection photodiode (MPD). The high-speed differential electrical signal output by the host computer is restored and shaped by the CDR, which is amplified by the laser driver to drive the VCSEL laser to produce the optical signal, and the optical signal is coupled to the optical fiber through the optical lens. The optical engine integrates a photodiode for detection, which is used for output optical power detection.

The receiving optical engine includes a photodiode (PIN), a signal amplifier (TIA/LA) and a receiver clock data recovery circuit (CDR). The optical signal in the optical fiber is coupled to the receiving photodiode (PIN) through an optical lens and converted into photocurrent. After the photocurrent signal is enhanced by the amplifier, it is sent to the CDR circuit and the clock and data signal recovery is completed. Finally, it is output to the host in the form of high-speed differential signal. The microcontroller reads the signal strength (modulation amplitude) received by the photodiode and reports the loss of the received signal if it is lower than the set threshold.

Specifications


Specifications

Both the transmitter and receiver have the function of suppression. When there is a signal input at the transmitter, the waveform displayed by the transmitted light access oscilloscope is an eye graph shape, and when there is no signal input, the waveform displayed by the transmitted light access oscilloscope is a straight line, and the actual measured optical power is lower than the normal optical power value, but not zero. When the incident light at the receiving has a signal input, the access oscilloscope shows that the waveform of the output electrical signal is an eye graph shape, and when there is no signal input, the oscilloscope shows that the waveform of the output electrical signal is a straight line.

## Optical Cable Details

| Parameter                     |   Min | Typ        |   Max | Unit   | Remarks                                          |
|-------------------------------|-------|------------|-------|--------|--------------------------------------------------|
| Jacket Material               |       | LSZH       |       |        |                                                  |
| Jacket Color                  |       | Aqua Green |       |        | Wecanprovide according to the needs of customers |
| Flammability Rating           |       | OFN        |       |        | Wecanprovide according to the needs of customers |
| Outer Diameter                |   2.8 | 3.0        |   3.2 | mm     |                                                  |
| Tensile Load(Short Term)      |       |            | 200   | N      |                                                  |
| Tensile Load(Long Term)       |       |            | 100   | N      |                                                  |
| Crush Resistance              |  10   |            |       | N/mm   | IEC 60794-1-21                                   |
| Impact Resistance             |   0.5 |            |       | N.m    | IEC 60794-1-21                                   |
| Flexing                       | 300   |            |       | Cycles | IEC 60794-1-21                                   |
| Twist Bend                    |       |            |       |        | IEC 60794-1-21                                   |
| Cable to SFP+ Plug Connection |       |            |  90   | N      |                                                  |
| Bend Radius(Short Term)       |  25   |            |       | mm     |                                                  |
| Bend Radius(Long Term)        |  30   |            |       | mm     |                                                  |


## Dimensions

![Image](/AOC/AOC-100-xM/AOC-100-xM_artifacts/image_000014_8ff041d5c1ec2293f42c7023f4d701a5c97cbbf9dc1e5e73c3fefa1a6d4f526c.png)

Bottom

ALL DIMENSIONS ARE ±0.2mm UNLESS OTHERWISE SPECIFIED UNIT: mm

## Electrical Pad Layout

Top View Of Board

![Image](/AOC/AOC-100-xM/AOC-100-xM_artifacts/image_000015_669066a687e3d46bbf6a5777d85523bbaf888c013ca2e9c50d194e1d0a271c91.png)

Top

Specifications

Bottom View Of Board

EET

TXFAULT

TXDISABLE

SDA

SCL

MOD\_ABS

RSO

LOS

RS1

V

EER

2

3

4

5

6

7

8

9

—10


## Pin Assignment

|   PIN # | Symbol     | Description                                                   |   Remarks |
|---------|------------|---------------------------------------------------------------|-----------|
|       1 | V EET      | Transmitter ground (common with receiver ground)              |         1 |
|       2 | TX FAULT   | Transmitter Fault                                             |           |
|       3 | TX DISABLE | Transmitter Disable. Laser output disabled on high or open    |         2 |
|       4 | SDA        | 2-wire Serial Interface Data Line                             |         3 |
|       5 | SCL        | 2-wire Serial Interface Clock Line                            |         3 |
|       6 | MOD ABS    | Module Absent. Grounded within the module                     |         3 |
|       7 | RS0        | No connection required                                        |           |
|       8 | LOS        | Loss of Signal indication. Logic 0 indicates normal operation |         4 |
|       9 | RS1        | No connection required                                        |         1 |
|      10 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      11 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      12 | RD -       | Receiver Inverted DATAout. ACcoupled                          |           |
|      13 | RD +       | Receiver Non-inverted DATAout. ACcoupled                      |           |
|      14 | V EER      | Receiver ground (common with transmitter ground)              |         1 |
|      15 | V CCR      | Receiver power supply                                         |           |
|      16 | V CCT      | Transmitter power supply                                      |           |
|      17 | V EET      | Transmitter ground (common with receiver ground)              |         1 |
|      18 | TD +       | Transmitter Non-Inverted DATA in. AC coupled                  |           |
|      19 | TD -       | Transmitter Inverted DATAin. ACcoupled                        |           |
|      20 | V EET      | Transmitter ground (common with receiver ground)              |         1 |

## Notes:

1. Circuit ground is isolated from chassis ground
2. Disabled: TDIS &gt; 2V or open,Enabled: TDIS &lt; 0.8V
3. Should Be pulled up with 4.7k -10k ohm on host board to a voltage between 2V and 3.6V
4. LOS is open collector output

## References

1.  IEEE standard 802.3. IEEE Standard Department, 2018
2.  FIBRE CHANNEL Physical Interface-6(FC-PI-6). Rev3.10 October 25, 2013
3.  SFF-8402 SFP+ 1X28 Gb/s Pluggable Transceiver Solution(SFP28). Rev1.1 September 13, 2014
4.  SFF-8419 SFP+ Power and Low Speed Interface. Rev1.3 June 11, 2015
5.  SFF-8432 SFP+ Module and Cage. Rev5.2a November 30, 2018
6.  SFF-8472 Management Interface for SFP+. Rev12.3 July 29, 2018

Specifications