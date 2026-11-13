# Guruh Tozalovchi Telegram Bot (aiogram 3)

Telegram guruhlarida tartib saqlash, kirish-chiqish xabarlarini va reklamalarni avtomatik tozalash uchun mo'ljallangan yordamchi bot.

## 🚀 Vazifalari
1. **Kirish/Chiqish xabarlarini o'chirish**: Yangi a'zo qo'shilganda yoki guruhni tark etganda chiqadigan servis xabarlarini avtomatik tozalaydi.
2. **Reklama xabarlarini tozalash**: Veb-havolalar, `@username` havolalar va kanallardan forward qilingan postlarni o'chiradi.
3. **Adminlarni himoyalash**: Guruh egalari va administratorlarining xabarlari o'chirilmaydi.
4. **Vaqtinchalik ogohlantirish**: Qoidabuzarga berilgan ogohlantirish 5 soniyadan keyin o'zi o'chib ketadi.

---

## 🛠 Ubuntu Serverda Ishga Tushirish (Dockersiz, Systemd)

### 1. Serverda Python va Git o'rnatish
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

### 2. Loyihani yuklab olish va venv yaratish
```bash
git clone https://github.com/USERNAME/REPO_NAME.git ~/yordamchibot
cd ~/yordamchibot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. `.env` faylini sozlash
```bash
nano .env
```
Ichiga tokenni yozing:
```env
BOT_TOKEN=8835777094:AAHd-_332nvZorfrnayfgJgH2lDckPgLUX4
```

### 4. Botni 24/7 rejimda avtomatik ishlatish (Systemd)
```bash
chmod +x setup_service.sh
./setup_service.sh
```

---

## 🔄 GitHub Actions CI/CD Sozlash

GitHub repozitoriyangizning **Settings -> Secrets and variables -> Actions** bo'limida quyidagi maxfiy kalitlarni kiriting:
- `SERVER_HOST`: Ubuntu serveringiz IP manzili
- `SERVER_USER`: Serverdagi login (masalan: `ubuntu` yoki `root`)
- `SERVER_SSH_KEY`: Serverga ulanish uchun private SSH kalitingiz (`cat ~/.ssh/id_ed25519` yoki `id_rsa`)
- `SERVER_PORT`: `22` (ixtiyoriy)

Har safar `git push origin main` qilganingizda GitHub Actions serveringizga ulanib, yangi kodni oladi va botni avtomatik qayta ishga tushiradi!
