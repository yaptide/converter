expected_output = """TITLE
proton beam simulation
* default physics settings for hadron therapy
GLOBAL    SDUM=DEPRBODY
DEFAULTS                                                              HADROTHE
* beam source
BEAM           -0.15                                                  PROTON    
* beam source position
BEAMPOS          0.0       0.0    -100.0
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
BOX fig0 -0.5 +0.0 +0.0 +1.0 +0.0 +0.0
+0.0 +1.0 +0.0 +0.0 +0.0 +1.0
RCC fig1 +2.02445317445455 +1.48772578487513 -0.4566366084694 +0.2310936510909 -0.3354515697503
+0.9132732169387 +1.0
SPH fig2 +3.32 +3.16 +0.0 +2.96
BOX figworld +0.0 +0.0 +10.5 +0.0 +0.0 +0.0
+0.0 +0.0 +0.0 +0.0 +0.0 +0.0
BOX figbound -1.0 +0.0 +10.5 +2.0 +0.0 +0.0
+0.0 +2.0 +0.0 +0.0 +0.0 +2.0
END
region0 5 +fig0 +fig1
region1 5 +fig2 -fig1
world 5 +figworld -fig0 -fig1 -fig2
boundary 5 +figbound -figworld
END
GEOEND
ASSIGNMA    BLCKHOLE   Z_BBODY
ASSIGNMA         AIR     Z_AIR
ASSIGNMA       WATER  Z_TARGET
* scoring NEUTRON on mesh z
USRBIN           0.0   NEUTRON       -21       0.5       0.5       5.0n_z
USRBIN          -0.5      -0.5       0.0         1         1       500&
* scoring NEUTRON on mesh yz
USRBIN           0.0   NEUTRON       -22       0.1       5.0       5.0n_yz
USRBIN          -0.1      -5.0       0.0         1       500       500&
* scoring NEUTRON on mesh xy
USRBIN           0.0   NEUTRON       -23       5.0       5.0       2.9n_xy
USRBIN          -5.0      -5.0       2.8       500       500         1&
* scoring NEUTRON on mesh zx
USRBIN           0.0   NEUTRON       -24       5.0       0.1       5.0n_zx
USRBIN          -5.0      -0.1       0.0       500         1       500&
* scoring ENERGY on mesh z
USRBIN           0.0    ENERGY       -25       0.5       0.5       5.0en_z
USRBIN          -0.5      -0.5       0.0         1         1       500&
* scoring ENERGY on mesh yz
USRBIN           0.0    ENERGY       -26       0.1       5.0       5.0en_yz
USRBIN          -0.1      -5.0       0.0         1       500       500&
* scoring ENERGY on mesh xy
USRBIN           0.0    ENERGY       -27       5.0       5.0       2.9en_xy
USRBIN          -5.0      -5.0       2.8       500       500         1&
* scoring ENERGY on mesh zx
USRBIN           0.0    ENERGY       -28       5.0       0.1       5.0en_zx
USRBIN          -5.0      -0.1       0.0       500         1       500&
* random number generator settings
RANDOMIZ                   137
* number of particles to simulate
START        10000.0                                                            
STOP
"""