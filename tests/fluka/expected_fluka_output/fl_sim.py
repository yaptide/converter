expected_output = """TITLE
proton beam simulation
* default physics settings for hadron therapy
DEFAULTS                                                              HADROTHE
* PROTON beam of energy 0.07 GeV
* flat circular shape with max radius=3.0 cm, min radius=0.0 cm
BEAM           -0.07       0.0       0.0       3.0       0.0      -1.0PROTON
* beam position: (0.0, 0.0, -1.5) cm
* beam direction cosines in respect to x: 0.0, y: 0.0
* beam direction is positive in respect to z axis
BEAMPOS          0.0       0.0      -1.5       0.0       0.0       0.0
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
* box fig0
* X range -6.0, +6.0
* Y range -5.0, +5.0
* Z range -1.0, +9.0
* X, Y, Z side lengths: +12.0, +10.0, +10.0
RPP fig0 -6.0 +6.0 -5.0 +5.0 -1.0 +9.0
* box fig1
* X range -4.0, +4.0
* Y range -4.0, +4.0
* Z range +0.0, +8.0
* X, Y, Z side lengths: +8.0, +8.0, +8.0
RPP fig1 -4.0 +4.0 -4.0 +4.0 +0.0 +8.0
* cylinder fig2
* bottom center (+0.0, +0.0, -0.5), top center (+0.0, +0.0, +0.5)
* spanning vector (+0.0, +0.0, +1.0)
* radius +4.0, height +1.0 cm
* rotation angles: 0*, 0*, 0*
RCC fig2 +0.0 +0.0 -0.5 +0.0 +0.0
+1.0 +4.0
* cylinder fig3
* bottom center (+0.0, +0.0, -0.5), top center (+0.0, +0.0, +0.5)
* spanning vector (+0.0, +0.0, +1.0)
* radius +2.0, height +1.0 cm
* rotation angles: 0*, 0*, 0*
RCC fig3 +0.0 +0.0 -0.5 +0.0 +0.0
+1.0 +2.0
* sphere fig4
* center (+0.0, +11.8172105325468, -14.215841748815), radius +1.0
SPH fig4 +0.0 +11.8172105325468 -14.215841748815 +1.0
* box figworld
* X range -6.6, +6.6
* Y range -5.5, +5.5
* Z range -5.5, +5.5
* X, Y, Z side lengths: +13.2, +11.0, +11.0
RPP figworld -6.6 +6.6 -5.5 +5.5 -5.5 +5.5
* box figbound
* X range -16.6, +16.6
* Y range -15.5, +15.5
* Z range -15.5, +15.5
* X, Y, Z side lengths: +33.2, +31.0, +31.0
RPP figbound -16.6 +16.6 -15.5 +15.5 -15.5 +15.5
END
region0 5 +fig0 -fig1 -fig2
region1 5 +fig1
region2 5 +fig2 -fig3
region3 5 +fig3
world 5 +figworld -fig0 -fig1 -fig2 -fig3 -fig4
boundary 5 +figbound -figworld
END
GEOEND
MATERIAL         0.0                1.01                              COM00001
MATERIAL        82.0               11.36                              MAT00001
LOW-MAT     MAT00001                                                  LEAD
COMPOUND        -1.0     WATER                                        COM00001
MAT-PROP         0.0       0.0      7.53  MAT00001                 0.0
ASSIGNMA         AIR   region0
ASSIGNMA    COM00001   region1
ASSIGNMA    MAT00001   region2
ASSIGNMA         AIR   region3
ASSIGNMA       WATER     world
ASSIGNMA    BLCKHOLE  boundary
* generated scoring cards
USRBIN          10.0  ALL-PART     -21.0      0.05       5.0       6.0Fluence
USRBIN         -0.05      -5.0      -6.0       1.0     100.0     120.0&
AUXSCORE      USRBIN -100100.0                 1.0       1.0       1.0
* random number generator settings
RANDOMIZ                   137
* number of particles to simulate
START        10000.0
STOP
"""