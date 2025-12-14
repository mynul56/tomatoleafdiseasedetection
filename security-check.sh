#!/bin/bash

# VPS Security Check Script
# Run this regularly to check for security issues

echo "======================================"
echo "   VPS Security Health Check"
echo "======================================"
echo "Date: $(date)"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Check for suspicious processes
echo -e "${YELLOW}[1] Checking for suspicious processes...${NC}"
SUSPICIOUS=$(ps aux | grep -E "mining|crypto|scan|bot|hack" | grep -v grep)
if [ -z "$SUSPICIOUS" ]; then
    echo -e "${GREEN}✓ No suspicious processes found${NC}"
else
    echo -e "${RED}⚠ ALERT: Suspicious processes detected!${NC}"
    echo "$SUSPICIOUS"
fi
echo ""

# 2. Check disk usage
echo -e "${YELLOW}[2] Checking disk usage...${NC}"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo -e "${GREEN}✓ Disk usage: ${DISK_USAGE}% (OK)${NC}"
else
    echo -e "${RED}⚠ WARNING: Disk usage: ${DISK_USAGE}% (High!)${NC}"
fi
echo ""

# 3. Check memory usage
echo -e "${YELLOW}[3] Checking memory usage...${NC}"
free -h
echo ""

# 4. Check failed login attempts
echo -e "${YELLOW}[4] Recent failed login attempts...${NC}"
FAILED=$(lastb -n 5 2>/dev/null)
if [ -z "$FAILED" ]; then
    echo -e "${GREEN}✓ No recent failed login attempts${NC}"
else
    echo -e "${YELLOW}Recent failures:${NC}"
    echo "$FAILED"
fi
echo ""

# 5. Check active connections
echo -e "${YELLOW}[5] Active network connections...${NC}"
netstat -tupln 2>/dev/null | grep ESTABLISHED | head -10
echo ""

# 6. Check backend service status
echo -e "${YELLOW}[6] Backend service status...${NC}"
if systemctl is-active --quiet tomato-backend; then
    echo -e "${GREEN}✓ Backend service is running${NC}"
else
    echo -e "${RED}⚠ WARNING: Backend service is NOT running!${NC}"
fi
echo ""

# 7. Check firewall status
echo -e "${YELLOW}[7] Firewall status...${NC}"
if sudo ufw status | grep -q "Status: active"; then
    echo -e "${GREEN}✓ Firewall is active${NC}"
else
    echo -e "${RED}⚠ WARNING: Firewall is NOT active!${NC}"
fi
echo ""

# 8. Check for updates
echo -e "${YELLOW}[8] Available updates...${NC}"
UPDATES=$(apt list --upgradable 2>/dev/null | grep -c upgradable)
if [ $UPDATES -gt 1 ]; then
    echo -e "${YELLOW}$UPDATES updates available${NC}"
else
    echo -e "${GREEN}✓ System is up to date${NC}"
fi
echo ""

# 9. Check system load
echo -e "${YELLOW}[9] System load...${NC}"
uptime
echo ""

# 10. Check for unauthorized users
echo -e "${YELLOW}[10] User accounts with shell access...${NC}"
cat /etc/passwd | grep /bin/bash | cut -d: -f1
echo ""

echo "======================================"
echo "   Security Check Complete"
echo "======================================"
echo ""
echo "Run this script regularly to monitor your VPS security!"
echo ""
