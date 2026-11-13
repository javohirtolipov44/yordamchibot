#!/bin/bash
set -e

# Joriy papka va foydalanuvchini aniqlash
APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CURRENT_USER="$(whoami)"

echo "⚙️ Bot servisini sozlash boshlandi..."
echo "📁 Papka: $APP_DIR"
echo "👤 Foydalanuvchi: $CURRENT_USER"

# Systemd servis faylini yaratish
sudo bash -c "cat > /etc/systemd/system/yordamchibot.service <<EOF
[Unit]
Description=Yordamchi Telegram Bot
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"

# CI/CD paytida sudo parolsiz qayta ishga tushishi uchun ruxsat berish
if [ "$CURRENT_USER" != "root" ]; then
    echo "$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart yordamchibot" | sudo tee /etc/sudoers.d/yordamchibot > /dev/null
    sudo chmod 0440 /etc/sudoers.d/yordamchibot
fi

# Servisni yangilash va ishga tushirish
sudo systemctl daemon-reload
sudo systemctl enable yordamchibot
sudo systemctl restart yordamchibot

echo "✅ Bot servisi muvaffaqiyatli ishga tushirildi!"
sudo systemctl status yordamchibot --no-pager

