#!/bin/bash
echo "==============================="
echo :"AWS t4g.micro Cost Tracker"
echo "==============================="
HOURS=$(echo "$(cat /proc/uptime | awk '{print $1}') / 3600" | bc -l)
COST=$(echo "$HOURS * 0.0084" | BC -L)
printf "Hours running: %.2f\n" $HOURS
printf "Estimated cost: \$%.4f\n" $COST
REMAINING=$(echo "200 - $COST" | bc -l)
printf "Budget remaining: \$%.2f\n" $REMAINING
echo "==============================="
