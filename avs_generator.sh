#!/system/bin/sh
set -x

SCRIPT=/sdcard/liveopp_avs
LIVEOPP=/sys/kernel/liveopp
AVS=/d/prcmu/avs

VBB_MAX_OPP=`cat $AVS | grep VBB_MAX_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VBB_100_OPP=`cat $AVS | grep VBB_100_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VARM_MAX_OPP=`cat $AVS | grep VARM_MAX_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VARM_100_OPP=`cat $AVS | grep VARM_100_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VARM_50_OPP=`cat $AVS | grep VARM_50_OPP | cut -d : -f 2 | cut -d ' ' -f 2`

rm $SCRIPT
touch $SCRIPT

# VARM

echo "# VARM" >> $SCRIPT

for i in `seq 0 9`
do
step=`cat $LIVEOPP/arm_step0$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_50_OPP > $LIVEOPP/arm_step0$i" >> $SCRIPT
done

# 50 opp
for i in `seq 10 13` #up to 400 MHz
do
step=`cat $LIVEOPP/arm_step$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_50_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

# 100 opp
for i in `seq 13 21`
do
step=`cat $LIVEOPP/arm_step$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_100_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

# max opp
for i in `seq 22 23`
do
step=`cat $LIVEOPP/arm_step$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_MAX_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

# VBBX

echo "# VBBX" >> $SCRIPT

for i in `seq 0 9`
do
echo "echo vbbx=$VBB_100_OPP > $LIVEOPP/arm_step0$i" >> $SCRIPT
done

for i in `seq 10 21` # up to 800 Mhz step
do
echo "echo vbbx=$VBB_100_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

for i in `seq 22 23`
do
echo "echo vbbx=$VBB_100_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done#!/system/bin/sh
set -x

SCRIPT=/sdcard/liveopp_avs
LIVEOPP=/sys/kernel/liveopp
AVS=/d/prcmu/avs

VBB_MAX_OPP=`cat $AVS | grep VBB_MAX_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VBB_100_OPP=`cat $AVS | grep VBB_100_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VARM_MAX_OPP=`cat $AVS | grep VARM_MAX_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VARM_100_OPP=`cat $AVS | grep VARM_100_OPP | cut -d : -f 2 | cut -d ' ' -f 2`
VARM_50_OPP=`cat $AVS | grep VARM_50_OPP | cut -d : -f 2 | cut -d ' ' -f 2`

rm $SCRIPT
touch $SCRIPT

# VARM

echo "# VARM" >> $SCRIPT

for i in `seq 0 9`
do
step=`cat $LIVEOPP/arm_step0$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_50_OPP > $LIVEOPP/arm_step0$i" >> $SCRIPT
done

# 50 opp
for i in `seq 10 13` #up to 400 MHz
do
step=`cat $LIVEOPP/arm_step$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_50_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

# 100 opp
for i in `seq 13 21`
do
step=`cat $LIVEOPP/arm_step$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_100_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

# max opp
for i in `seq 22 23`
do
step=`cat $LIVEOPP/arm_step$i | grep show | cut -d : -f 2`
echo "# $step" >> $SCRIPT
echo "echo varm=$VARM_MAX_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

# VBBX

echo "# VBBX" >> $SCRIPT

for i in `seq 0 9`
do
echo "echo vbbx=$VBB_100_OPP > $LIVEOPP/arm_step0$i" >> $SCRIPT
done

for i in `seq 10 21` # up to 800 Mhz step
do
echo "echo vbbx=$VBB_100_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done

for i in `seq 22 23`
do
echo "echo vbbx=$VBB_100_OPP > $LIVEOPP/arm_step$i" >> $SCRIPT
done
