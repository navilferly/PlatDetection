@echo off
echo ==== Ganti Akun Git Lokal ====
set /p username="Masukkan GitHub Username: "
set /p email="Masukkan GitHub Email: "

git config user.name "%username%"
git config user.email "%email%"

echo ===============================
echo Git sekarang menggunakan akun:
git config user.name
git config user.email
echo ===============================
pause
