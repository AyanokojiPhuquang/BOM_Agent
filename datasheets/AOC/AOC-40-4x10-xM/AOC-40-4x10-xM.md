## Datasheet:

ModuleTek: AOC-40-4x10-5M

40GBase-AOC QSFP+ to 4x 10G SFP+(Active Optical Cable 5m DOM)

## Description

The ModuleTek's AOC-40-4x10-5M breakout Active Optical Cables (AOCs) offer IT professionals a    cost-effective interconnect solution for merging 40G QSFP+ and 10G SFP+ enabled host adapters, switches and servers.

For typical applications, users can install this breakout or splitter cable between an available QSFP+ port on 40GE switch and feed up to 4 upstream SFP+ enabled 10GE switches. Each cable features a single SFF-8436 compliant QSFP+ connector rated for 41.2Gb/s on one end and 4 SFF-8431 complicant SFP+ connectors rated for 10.3Gb/s each on the other end.

## Features

- ⚫ SFF-8436 QSFP+ compliant
- ⚫ SFF-8431 SFP+ compliant
- ⚫ Hot-pluggable electrical interface
- ⚫ 850nm VCSEL transmitter
- ⚫ PIN photo-detector receiver
- ⚫ Up to 100m on OM3 MMF
- ⚫ Operating case temperature range 0°C to +70°C
- ⚫ All-metal housing for superior EMI performance
- ⚫ Low power consumption &lt; 1.5W (QSFP+) &lt; 1W (SFP+)
- ⚫ RoHS compliant (lead free)

## Applications

- ⚫ IEEE 802.3ba 40GBASE-SR4
- ⚫ IEEE 802.3ae 10GBASE-SR
- ⚫ InfiniBand SDR/DDR/QDR
- ⚫ High-Performance Computing (HPC) clusters
- ⚫ Servers, switches, storage and host card adapters


## Recommended Operating Conditions and Supply Requirements

| Parameter                              | Symbol   |     Min |   Typical | Max     | Unit   |
|----------------------------------------|----------|---------|-----------|---------|--------|
| Operating Case Temperature             | TOPC     |    0    |           | 70      | degC   |
| Power Supply Voltage                   | VCC      |    3.13 |       3.3 | 3.47    | V      |
| Data Rate                              | DR       |         |      10.3 | 11.3    | Gbps   |
| Data Speed Tolerance                   | ∆DR      | -100    |           | +100    | ppm    |
| Link Distance with OM3 fiber           | D        |    0    |           | 100     | m      |
| Control* Input Voltage High            | Vih      |    2    |           | VCC+0.3 | V      |
| Control* Input Voltage Low             | Vil      |   -0.3  |           | 0.8     | V      |
| I2C Serial Interface frequence         | fs       |         |           | 400k    | Hz     |
| Power Supply Noise                     |          |         |           | 50      | mVpp   |
| Receiver Differential Data Output Load |          |         |           | 100     | mVpp   |

## Active Cable-End Electrical Characteristics

The following characteristics are defined over the Recommended Operating Conditions unless otherwise noted. Typical values are for      Tc = 40 °C, Vcc = 3.3 V

| Parameter                                       | Symbol   | Min   | Typical   |    Max | Unit   |
|-------------------------------------------------|----------|-------|-----------|--------|--------|
| QSFP+ 40G Active Cable- End Power Consumption   |          |       |           |   1.5  | W      |
| QSFP+ 40GActive Cable- End Power Supply Current |          |       |           | 300    | mA     |
| SFP+ 10GActive Cable- End Power Consumption     |          |       |           |   0.35 | W      |
| SFP+ 10GActive Cable- End Power Supply Current  |          |       |           | 100    | mA     |

## QSFP+ AOC-end Electrical Characteristics Electrical Specifications

| Parameter                             | Symbol   |   Min |   Typical | Max   | Unit   |
|---------------------------------------|----------|-------|-----------|-------|--------|
| Differential input impedance          | Zin      |    90 |       100 | 110   | ohm    |
| Differential Output impedance         | Zout     |    90 |       100 | 110   | ohm    |
| Differential input voltage amplitude  | ΔVin     |   300 |           | 1100  | mVp-p  |
| Differential output voltage amplitude | ΔVout    |   400 |           | 800   | mVp-p  |
| Bit Error Rate                        | BR       |       |           | E-12  | E-12   |

| Input Logic Level High   | VIH   | 2.0     | VCC   | V   |
|--------------------------|-------|---------|-------|-----|
| Input Logic Level Low    | VIL   | 0       | 0.8   | V   |
| Output Logic Level High  | VOH   | VCC-0.5 | VCC   | V   |
| Output Logic Level Low   | VOL   | 0       | 0.4   | V   |

## QSFP+ AOC-end Pin Descriptions

|   PIN | Logic      | Symbol   | Name/Description                     |   Note |
|-------|------------|----------|--------------------------------------|--------|
|     1 |            | GND      | Ground                               |      1 |
|     2 | CML-I      | Tx2n     | Transmitter Inverted Data Input      |        |
|     3 | CML-I      | Tx2p     | Transmitter Non-Inverted Data output |        |
|     4 |            | GND      | Ground                               |      1 |
|     5 | CML-I      | Tx4n     | Transmitter Inverted Data Input      |        |
|     6 | CML-I      | Tx4p     | Transmitter Non-Inverted Data output |        |
|     7 |            | GND      | Ground                               |      1 |
|     8 | LVTLL-I    | ModSelL  | Module Select                        |        |
|     9 | LVTLL-I    | ResetL   | Module Reset                         |        |
|    10 |            | VccRx    | ﹢ 3.3V Power Supply Receiver        |      2 |
|    11 | LVCMOS-I/O | SCL      | 2-Wire Serial Interface Clock        |        |
|    12 | LVCMOS-I/O | SDA      | 2-Wire Serial Interface Data         |        |
|    13 |            | GND      | Ground                               |        |
|    14 | CML-O      | Rx3p     | Receiver Non-Inverted Data Output    |        |
|    15 | CML-O      | Rx3n     | Receiver Inverted Data Output        |        |
|    16 |            | GND      | Ground                               |      1 |
|    17 | CML-O      | Rx1p     | Receiver Non-Inverted Data Output    |        |
|    18 | CML-O      | Rx1n     | Receiver Inverted Data Output        |        |
|    19 |            | GND      | Ground                               |      1 |
|    20 |            | GND      | Ground                               |      1 |
|    21 | CML-O      | Rx2n     | Receiver Inverted Data Output        |        |
|    22 | CML-O      | Rx2p     | Receiver Non-Inverted Data Output    |        |
|    23 |            | GND      | Ground                               |      1 |
|    24 | CML-O      | Rx4n     | Receiver Inverted Data Output        |      1 |

|   25 | CML-O   | Rx4p    | Receiver Non-Inverted Data Output   |    |
|------|---------|---------|-------------------------------------|----|
|   26 |         | GND     | Ground                              |  1 |
|   27 | LVTTL-O | ModPrsL | Module Present                      |    |
|   28 | LVTTL-O | IntL    | Interrupt                           |    |
|   29 |         | VccTx   | +3.3 VPower Supply transmitter      |  2 |
|   30 |         | Vcc1    | +3.3 VPower Supply                  |  2 |
|   31 | LVTTL-I | LPMode  | Low Power Mode                      |    |
|   32 |         | GND     | Ground                              |  1 |
|   33 | CML-I   | Tx3p    | Transmitter Non-Inverted Data Input |    |
|   34 | CML-I   | Tx3n    | Transmitter Inverted Data Output    |    |
|   35 |         | GND     | Ground                              |  1 |
|   36 | CML-I   | Tx1p    | Transmitter Non-Inverted Data Input |    |
|   37 | CML-I   | Tx1n    | Transmitter Inverted Data Output    |    |
|   38 |         | GND     | Ground                              |  1 |

## Notes:

Module circuit ground is isolated from module chassis ground within the module. GND is the symbol for signal and supply (power) common for QSFP modules.

The connector pins are each rated for a maximum current of 500mA.


Top Side ViewedfromTop

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000002_9e6c5ed1484190321bfbabd3ad8d03460180d89ba1238f3dcffd3d6bf4585daf.png)

## ModSelL Pin

The ModSelL is an input pin. When held low by the host, the module responds to 2-wire serial communication commands. The ModSelL allows the use of multiple QSFP modules on a single 2-wire interface bus. When the ModSelL is 'High', the module will not respond to any 2-wire interface communication from the host. ModSelL has an internal pull-up in the module.

## ResetL Pin

Reset. LPMode\_Reset has an internal pull-up in the module. A low level on the ResetL pin for longer than the minimum pulse length (t\_Reset\_init) initiates a complete module reset, returning all user module settings to their default state. Module Reset Assert Time (t\_init) starts on the rising edge after the low level on the ResetL pin is released. During the execution of a reset (t\_init) the host shall disregard all status bits until the module indicates a completion of the reset interrupt. The module indicates this by posting an IntL signal with the Data\_Not\_Ready bit negated. Note that on power up (including hot insertion) the module will post this completion of reset interrupt without requiring a reset.

## LPMode Pin

QSFP+ SR4 operate in the low power mode (less than 1.5 W power consumption) This pin active high will decrease power consumption to less than 1W.

## ModPrsL Pin

C Card 四 #

Bottom Side ViewedfromBottom

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000003_a0b96fe299fe4b300e4ede7e7a22c362fa7051b7b275d0b0234d77f52887b7a2.png)

ModPrsL is pulled up to Vcc on the host board and grounded in the module. The ModPrsL is asserted 'Low' when the module is inserted and deasserted 'High' when the module is physically absent from the host connector.

## IntL Pin

IntL is an output pin. When 'Low', it indicates a possible module operational fault or a status critical to the host system. The host identifies the source of the interrupt by using the 2-wire serial interface. The IntL pin is an open collector output and must be pulled up to Vcc on the host board.

## QSFP+ AOC-end Power Supply Filtering

The host board should use the power supply filtering shown in Figure1.

Figure1. Host Board Power Supply Filtering

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000004_fb2430a901dd95b1066c3238cd85a0e509b36f9421c9cbeb8a942ccb32918dda.png)

## QSFP+ AOC-end EEPROM Serial ID Memory Contents:

Compliant to the industry standard SFF-8436 QSFP+ Specification

## SFP+ AOC-end Electrical Specifications

| Parameter                                       | Symbol   |   Min |   Typical | Max   | Unit   |
|-------------------------------------------------|----------|-------|-----------|-------|--------|
| Differential input impedance                    | Zin      |    90 |       100 | 110   | ohm    |
| Differential Output impedance                   | Zout     |    90 |       100 | 110   | ohm    |
| Differential input voltage amplitude aAmplitude | ΔVin     |   100 |           | 1800  | mVp-p  |
| Differential output voltage amplitude           | ΔVout    |   400 |           | 800   | mVp-p  |
| Bit Error Rate                                  | BR       |       |           | E-12  |        |


| Input Logic Level High   | VIH   |   2.0 |   VCC | V   |
|--------------------------|-------|-------|-------|-----|
| Input Logic Level Low    | VIL   |     0 |   0.8 | V   |

## SFP+ AOC-end Pin Descriptions

|   PIN | Symbol     | Name/Description                                                                   | Note   |
|-------|------------|------------------------------------------------------------------------------------|--------|
|     1 | VeeT       | Transmitter Signal Ground                                                          | Note 1 |
|     2 | TX_FAULT   | Transmitter Fault (LVTTL-O) - Not used. Grounded inside the module                 | Note 2 |
|     3 | TX_DISABLE | Transmitter Disable (LVTTL-I) - High or open disables the transmitter              | Note 3 |
|     4 | SDA        | Two Wire Serial Interface Data Line (LVCMOS - I/O) (same as MOD-DEF2 in INF-8074)  | Note 4 |
|     5 | SCL        | Two Wire Serial Interface Clock Line (LVCMOS - I/O) (same as MOD-DEF1 in INF-8074) | Note 4 |
|     6 | MOD_ABS    | Module Absent (Output), connected to VeeT or VeeR in the module                    | Note 5 |
|     7 | RS0        | Rate Select 0 - Not used, Presents high input impedance.                           |        |
|     8 | RX_LOS     | Receiver Loss of Signal (LVTTL-O)                                                  | Note 2 |
|     9 | RS1        | Rate Select 1 - Not used, Presents high input impedance.                           |        |
|    10 | VeeR       | Receiver Signal Ground                                                             | Note 1 |
|    11 | VeeR       | Receiver Signal Ground                                                             | Note 1 |
|    12 | RD-        | Receiver Data Out Inverted (CML-O)                                                 |        |
|    13 | RD+        | Receiver Data Out (CML-O)                                                          |        |
|    14 | VeeR       | Receiver Signal Ground                                                             |        |
|    15 | VccR       | Receiver Power + 3.3 V                                                             |        |
|    16 | VccT       | Transmitter Power + 3.3 V                                                          |        |
|    17 | VeeT       | Transmitter Signal Ground                                                          | Note 1 |


|   18 | TD+   | Transmitter Data In (CML-I)          |        |
|------|-------|--------------------------------------|--------|
|   19 | TD-   | Transmitter Data In Inverted (CML-I) |        |
|   20 | VeeT  | Transmitter Signal Ground            | Note 1 |

## Notes:

1. Module circuit ground is isolated from module chassis ground within the module. GND is the symbol for signal and supply (power) common for SFP modules.
2. This is an open collector/drain output that on the host board requires a 4.7 kΩ to 10 kΩ pullup resistor to VccHost. See Figure 2.
3. This input is internally biased high with a 4.7 kΩ to 10 kΩ pullup resistor to VccT.
4. Two-Wire Serial interface clock and data lines require an external pullup resistor dependent on the capacitance load.
5. This is a ground return that on the host board requires a 4.7 kΩ to 10 kΩ pullup resistor to VccHost.

Figure 2

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000007_0bc642bbc378550cd18ffafbc12da3c737c3e7d7425c1505dd65bfd32d142364.png)

QSFP+ AOC-end Power Supply Filtering

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000008_29508541e43d01b499de7a0055e339ec090f116c0425b15516612c06be1f075c.png)

NOTE: INDUCTORSMUSTHAVELESSTHAN1QSERIESRESISTANCETOLIMITVOLTAGEDROPTOTHESFPMODULE.

## Optical Fiber Specifications

| Parameter                | Specification                              |
|--------------------------|--------------------------------------------|
| Tight buffer color       | Blue                                       |
| Tight buffer material    | PVC                                        |
| Fiber type               | 62.5/125 (OFS) Bandwith:160 MHz.km @850 nm |
| Jacket material          | PVC                                        |
| Cable diametermm         | 3.0 ± 0.1                                  |
| Cable weight Kg/km       | 7.0                                        |
| Min. bending radiusmm    | 30                                         |
| Attenuation dB/km        | ≤ 3.5 at 850 nm ≤ 1.5 at 1300 nm           |
| Short tension N          | 120                                        |
| Operation temperature °C | -20~70                                     |

## SFP+ AOC end Mechanical Specifications

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000009_1c329d955f919d36be1dfc94e2496982857b309402465ad63dfa25e2c62f9b82.png)

57.00

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000010_db2ebe5e839aa698f311e0eb1cc3712b210935b1ad5434060189b845804f7f4e.png)

## QSFP+ AOC end Mechanical Specifications

## ModuleTek

89.86

R25.00

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000011_8e9d8d5bb2481d6d5f56bf99af1be7820f8541994847c3bdbd061ec910f0cc61.png)

![Image](/AOC/AOC-40-4x10-xM/AOC-40-4x10-xM_artifacts/image_000012_420485f97b6521abc6198c83d8c02291c1cfbe8febc24a54012e9655db073bd4.png)