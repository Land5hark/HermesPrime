#!/bin/bash

# Second Brain SSH Tunnel Script
# Usage: ./second-brain-connect.sh

SERVER_IP="187.77.11.213"
SERVER_USER="clawd"
LOCAL_PORT=8080
REMOTE_PORT=8080
PID_FILE="/tmp/second-brain-tunnel.pid"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🧠 Second Brain Tunnel Connector"
echo "================================"

# Check if tunnel already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Tunnel already running (PID: $OLD_PID)${NC}"
        echo "   Access at: http://localhost:$LOCAL_PORT"
        echo ""
        read -p "Kill existing tunnel and restart? (y/n): " RESTART
        if [[ $RESTART =~ ^[Yy]$ ]]; then
            kill "$OLD_PID" 2>/dev/null
            rm -f "$PID_FILE"
            echo -e "${GREEN}✓ Killed existing tunnel${NC}"
        else
            echo "Keeping existing tunnel. Exiting."
            exit 0
        fi
    else
        rm -f "$PID_FILE"
    fi
fi

# Test SSH connection first
echo ""
echo "Testing SSH connection to $SERVER_USER@$SERVER_IP..."
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes "$SERVER_USER@$SERVER_IP" exit 2>/dev/null; then
    echo -e "${RED}✗ SSH connection failed${NC}"
    echo ""
    echo "Possible issues:"
    echo "  • SSH key not set up (run: ssh-copy-id $SERVER_USER@$SERVER_IP)"
    echo "  • Wrong username (current: $SERVER_USER)"
    echo "  • Server not reachable"
    exit 1
fi

echo -e "${GREEN}✓ SSH connection successful${NC}"
echo ""

# Create the tunnel
echo "Creating SSH tunnel..."
echo "  Local:  http://localhost:$LOCAL_PORT"
echo "  Remote: $SERVER_IP:$REMOTE_PORT"
echo ""

ssh -f -N -L "$LOCAL_PORT:localhost:$REMOTE_PORT" "$SERVER_USER@$SERVER_IP" -o ServerAliveInterval=60 -o ServerAliveCountMax=3

if [ $? -eq 0 ]; then
    # Find the SSH process PID
    SSH_PID=$(pgrep -f "ssh.*-L $LOCAL_PORT:localhost:$REMOTE_PORT.*$SERVER_IP")
    if [ -n "$SSH_PID" ]; then
        echo "$SSH_PID" > "$PID_FILE"
        echo -e "${GREEN}✓ Tunnel created successfully!${NC}"
        echo ""
        echo "🌐 Open: http://localhost:$LOCAL_PORT"
        echo ""
        echo "To disconnect: kill $SSH_PID"
        echo "Or run: pkill -f 'ssh.*second-brain'"
        echo ""
        
        # Try to open browser (macOS, Linux, or WSL)
        read -p "Open browser now? (y/n): " OPEN_BROWSER
        if [[ $OPEN_BROWSER =~ ^[Yy]$ ]]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open "http://localhost:$LOCAL_PORT"
            elif command -v open &> /dev/null; then
                open "http://localhost:$LOCAL_PORT"
            elif command -v start &> /dev/null; then
                start "http://localhost:$LOCAL_PORT"
            else
                echo "Couldn't detect browser opener. Please open manually."
            fi
        fi
    else
        echo -e "${YELLOW}⚠ Tunnel may have started but couldn't find PID${NC}"
    fi
else
    echo -e "${RED}✗ Failed to create tunnel${NC}"
    exit 1
fi
