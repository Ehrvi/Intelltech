#!/bin/bash
# Manus Global Knowledge - Google Drive Sync Script
# Zero-cost bidirectional sync between local and Google Drive

set -e  # Exit on error

# Paths
LOCAL_PATH="/home/ubuntu/manus_global_knowledge"
REMOTE_PATH="manus_google_drive:Manus_Knowledge"
RCLONE_CONFIG="/home/ubuntu/.gdrive-rclone.ini"
LOG_FILE="/home/ubuntu/manus_global_knowledge/sync.log"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to sync from Google Drive to local (pull)
sync_pull() {
    log "${YELLOW}Syncing FROM Google Drive TO local...${NC}"
    
    rclone sync "$REMOTE_PATH/" "$LOCAL_PATH/" \
        --config "$RCLONE_CONFIG" \
        --fast-list \
        --verbose \
        --log-file="$LOG_FILE" \
        --log-level INFO
    
    if [ $? -eq 0 ]; then
        log "${GREEN}✅ Pull sync successful${NC}"
        return 0
    else
        log "${RED}❌ Pull sync failed${NC}"
        return 1
    fi
}

# Function to sync from local to Google Drive (push)
sync_push() {
    log "${YELLOW}Syncing FROM local TO Google Drive...${NC}"
    
    rclone sync "$LOCAL_PATH/" "$REMOTE_PATH/" \
        --config "$RCLONE_CONFIG" \
        --fast-list \
        --verbose \
        --log-file="$LOG_FILE" \
        --log-level INFO
    
    if [ $? -eq 0 ]; then
        log "${GREEN}✅ Push sync successful${NC}"
        return 0
    else
        log "${RED}❌ Push sync failed${NC}"
        return 1
    fi
}

# Function to rebuild search indices after sync
rebuild_indices() {
    log "${YELLOW}Rebuilding search indices...${NC}"
    
    python3 "$LOCAL_PATH/build_search_index.py"
    
    if [ $? -eq 0 ]; then
        log "${GREEN}✅ Search indices rebuilt${NC}"
        return 0
    else
        log "${RED}❌ Index rebuild failed${NC}"
        return 1
    fi
}

# Main script
case "$1" in
    pull)
        log "=== PULL OPERATION STARTED ==="
        sync_pull
        rebuild_indices
        log "=== PULL OPERATION COMPLETED ==="
        ;;
    push)
        log "=== PUSH OPERATION STARTED ==="
        rebuild_indices
        sync_push
        log "=== PUSH OPERATION COMPLETED ==="
        ;;
    both)
        log "=== BIDIRECTIONAL SYNC STARTED ==="
        sync_pull
        rebuild_indices
        sync_push
        log "=== BIDIRECTIONAL SYNC COMPLETED ==="
        ;;
    *)
        echo "Usage: $0 {pull|push|both}"
        echo ""
        echo "  pull  - Sync FROM Google Drive TO local (at conversation start)"
        echo "  push  - Sync FROM local TO Google Drive (after knowledge update)"
        echo "  both  - Bidirectional sync (pull, rebuild, push)"
        exit 1
        ;;
esac

exit 0
