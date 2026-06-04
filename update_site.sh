#!/bin/bash
FRONTEND_DIR="/media/vpsg16gb/Workspace1/HanaApplication/frontend"
SITE_DIR="/media/vpsg16gb/Workspace1/HanaApplication/site"

echo "Syncing frontend files to site directory..."

# Cập nhật Hana Dashboard
cp "$FRONTEND_DIR/index.html" "$SITE_DIR/index.html"
cp "$FRONTEND_DIR/index.html" "$SITE_DIR/hana.html"

# Cập nhật Parents Dashboard
cp "$FRONTEND_DIR/parents.html" "$SITE_DIR/parents.html"

# Sao chép các file phụ trợ cần thiết
cp "$FRONTEND_DIR/lessons_data.js" "$SITE_DIR/lessons_data.js"
cp "$FRONTEND_DIR/ai_evaluator.js" "$SITE_DIR/ai_evaluator.js"
cp -r "$FRONTEND_DIR/assets" "$SITE_DIR/" 2>/dev/null
cp -r "$FRONTEND_DIR/illustrations" "$SITE_DIR/" 2>/dev/null

echo "Done syncing."
