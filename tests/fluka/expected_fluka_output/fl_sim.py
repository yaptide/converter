expected_output = """TITLE
proton beam simulation
* default physics settings for hadron therapy
DEFAULTS                                                              HADROTHE
* beam source
BEAM           -0.07                                                  PROTON    
* beam source position
BEAMPOS          0.0       0.0    -100.0
* geometry description starts here
GEOBEGIN                                                              COMBNAME
    0    0
* box fig0
* X range -6.0, +6.0
* Y range -5.0, +5.0
* Z range -1.0, +9.0
RPP fig0 -6.0 +6.0 -5.0 +5.0 -1.0 +9.0
* box fig1
* X range -4.0, +4.0
* Y range -4.0, +4.0
* Z range +0.0, +8.0
RPP fig1 -4.0 +4.0 -4.0 +4.0 +0.0 +8.0
* cylinder fig2
* bottom center (+0.0, +0.0, -0.5), spanning vector (+0.0, +0.0, +1.0),
* radius +4.0, height +0.0 cm
* rotation angles: 0*, 0*, 0*
RCC fig2 +0.0 +0.0 -0.5 +0.0 +0.0
+1.0 +4.0
* cylinder fig3
* bottom center (+0.0, +0.0, -0.5), spanning vector (+0.0, +0.0, +1.0),
* radius +2.0, height +0.0 cm
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
RPP figworld -6.6 +6.6 -5.5 +5.5 -5.5 +5.5
* box figbound
* X range -16.6, +16.6
* Y range -15.5, +15.5
* Z range -15.5, +15.5
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