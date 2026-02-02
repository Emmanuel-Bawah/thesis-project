#!/bin/bash
# Network Condition Simulator for Testing
# Simulates 2G, 3G, 4G conditions using tc (traffic control)

set -e

INTERFACE="lo"  # loopback interface for testing

function setup_2g() {
    echo "Setting up 2G network simulation..."
    # 2G: ~50 Kbps, 500ms latency, 2-5% packet loss
    sudo tc qdisc add dev $INTERFACE root netem delay 500ms 50ms loss 3% rate 50kbit
    echo "✓ 2G network simulation active"
}

function setup_3g() {
    echo "Setting up 3G network simulation..."
    # 3G: ~384 Kbps, 100ms latency, 1-2% packet loss
    sudo tc qdisc add dev $INTERFACE root netem delay 100ms 20ms loss 1.5% rate 384kbit
    echo "✓ 3G network simulation active"
}

function setup_4g() {
    echo "Setting up 4G network simulation..."
    # 4G: ~10 Mbps, 50ms latency, <1% packet loss
    sudo tc qdisc add dev $INTERFACE root netem delay 50ms 10ms loss 0.5% rate 10mbit
    echo "✓ 4G network simulation active"
}

function clear_network() {
    echo "Clearing network simulation..."
    sudo tc qdisc del dev $INTERFACE root 2>/dev/null || true
    echo "✓ Network simulation cleared"
}

function show_status() {
    echo "Current network configuration:"
    sudo tc qdisc show dev $INTERFACE
}

# Main menu
case "$1" in
    2g)
        clear_network
        setup_2g
        ;;
    3g)
        clear_network
        setup_3g
        ;;
    4g)
        clear_network
        setup_4g
        ;;
    clear)
        clear_network
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {2g|3g|4g|clear|status}"
        echo ""
        echo "Examples:"
        echo "  $0 2g      # Simulate 2G network"
        echo "  $0 3g      # Simulate 3G network"
        echo "  $0 4g      # Simulate 4G network"
        echo "  $0 clear   # Remove simulation"
        echo "  $0 status  # Show current setup"
        exit 1
        ;;
esac
