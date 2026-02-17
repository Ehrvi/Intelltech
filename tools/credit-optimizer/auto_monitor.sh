#!/bin/bash
# Automatic Monitoring for Manus Credit Optimization
# Generates reports and tracks savings

REPORT_DIR="/home/ubuntu/manus_global_knowledge/reports"
LOG_DIR="/home/ubuntu/manus_global_knowledge/logs"

# Create directories if they don't exist
mkdir -p "$REPORT_DIR"
mkdir -p "$LOG_DIR"

# Generate daily report
generate_daily_report() {
    DATE=$(date +%Y%m%d)
    REPORT_FILE="$REPORT_DIR/manus_optimization_daily_$DATE.txt"
    
    python3 /home/ubuntu/manus_global_knowledge/core/manus_optimization_dashboard.py daily > "$REPORT_FILE" 2>&1
    
    echo "Daily report generated: $REPORT_FILE"
}

# Generate weekly report (on Mondays)
generate_weekly_report() {
    if [ "$(date +%u)" -eq 1 ]; then
        DATE=$(date +%Y%m%d)
        REPORT_FILE="$REPORT_DIR/manus_optimization_weekly_$DATE.txt"
        
        python3 /home/ubuntu/manus_global_knowledge/core/manus_optimization_dashboard.py weekly > "$REPORT_FILE" 2>&1
        
        echo "Weekly report generated: $REPORT_FILE"
    fi
}

# Log current stats
log_stats() {
    DATE=$(date +%Y-%m-%d_%H-%M-%S)
    LOG_FILE="$LOG_DIR/stats_$DATE.json"
    
    python3 -c "
import sys
sys.path.insert(0, '/home/ubuntu/manus_global_knowledge/core')
from manus_credit_optimizer import get_optimizer
import json

optimizer = get_optimizer()
stats = optimizer.get_optimization_stats()

with open('$LOG_FILE', 'w') as f:
    json.dump(stats, f, indent=2)
" 2>/dev/null
    
    if [ -f "$LOG_FILE" ]; then
        echo "Stats logged: $LOG_FILE"
    fi
}

# Main
case "${1:-daily}" in
    daily)
        generate_daily_report
        ;;
    weekly)
        generate_weekly_report
        ;;
    log)
        log_stats
        ;;
    all)
        generate_daily_report
        generate_weekly_report
        log_stats
        ;;
    *)
        echo "Usage: $0 {daily|weekly|log|all}"
        exit 1
        ;;
esac
