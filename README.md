# BugTracker

یک ابزار قدرتمند برای تحلیل و بررسی کد در زبان‌های برنامه‌نویسی مختلف. این ابزار به شما کمک می‌کند تا خطاهای احتمالی در کد خود را قبل از اجرا پیدا کنید.

## ویژگی‌ها

- پشتیبانی از زبان‌های مختلف:
  - Python
  - PHP
  - JavaScript
  - C/C++
- تشخیص خودکار نسخه زبان برنامه‌نویسی
- پشتیبانی از سیستم‌عامل‌های مختلف (Windows, Linux, macOS)
- رابط کاربری ساده و کاربرپسند
- گزارش‌دهی دقیق خطاها و هشدارها

## پیش‌نیازها

قبل از نصب و اجرای پروژه، مطمئن شوید که موارد زیر را نصب کرده‌اید:

### 1. پایتون

- Python 3.8 یا بالاتر
- pip (مدیر بسته‌های پایتون)

برای نصب پایتون:

- **ویندوز**: از [سایت رسمی پایتون](https://www.python.org/downloads/) دانلود و نصب کنید
- **لینوکس**:
  ```bash
  sudo apt-get update
  sudo apt-get install python3.8 python3-pip  # Ubuntu/Debian
  sudo yum install python3 python3-pip        # CentOS/RHEL
  ```
- **macOS**:
  ```bash
  brew install python@3.8
  ```

### 2. Node.js و npm

- Node.js 14 یا بالاتر
- npm 6 یا بالاتر

برای نصب Node.js:

- **ویندوز**: از [سایت رسمی Node.js](https://nodejs.org/) دانلود و نصب کنید
- **لینوکس**:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
  sudo apt-get install -y nodejs  # Ubuntu/Debian
  ```
- **macOS**:
  ```bash
  brew install node@14
  ```

### 3. Composer (برای PHP)

- Composer 2 یا بالاتر

برای نصب Composer:

- **ویندوز**: از [سایت رسمی Composer](https://getcomposer.org/download/) دانلود و نصب کنید
- **لینوکس/macOS**:
  ```bash
  php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
  php composer-setup.php
  sudo mv composer.phar /usr/local/bin/composer
  ```

### 4. دسترسی‌های مورد نیاز
 ابتدا فایل cppcheck را از وب سایت رسمی آن دانلود کنید
- **ویندوز**: دسترسی Administrator برای نصب Cppcheck
- **لینوکس**: دسترسی sudo برای نصب Cppcheck
- **macOS**: نصب Homebrew و دسترسی sudo




## نصب و راه‌اندازی

### 1. دریافت کد پروژه

```bash
git clone https://github.com/pouriyafaraji/BugTracker.git
cd BugTracker
```

### 2. نصب خودکار وابستگی‌ها

```bash
cd backend
python setup.py
```

این اسکریپت به صورت خودکار:

- وابستگی‌های پایتون را نصب می‌کند
- ESLint را برای JavaScript نصب می‌کند
- PHPStan را برای PHP نصب می‌کند
- Cppcheck را برای C/C++ نصب می‌کند
- فایل‌های پیکربندی مورد نیاز را ایجاد می‌کند

### 3. اجرای سرور

```bash
uvicorn main:app --reload
```

سرور در آدرس `http://localhost:8000` اجرا می‌شود.

سپس وارد روت پروژه شوید و وابستگی ها را با دستور npm install نصب کنید.
و سپس با دستور npm run dev فرانت پروژه در ادرس http://localhost:5431 اجرا میشود.
## استفاده از API

### تحلیل کد

- **Endpoint**: `POST /analyze`
- **پارامترها**:
  ```json
  {
    "code": "کد مورد نظر",
    "language": "python|php|javascript|cpp|c",
    "version": "نسخه زبان (اختیاری)"
  }
  ```
- **مثال**:
  ```bash
  curl -X POST "http://localhost:8000/analyze" \
       -H "Content-Type: application/json" \
       -d '{"code": "print(\"Hello\")", "language": "python"}'
  ```

## عیب‌یابی

### مشکلات رایج

1. **خطای "ابزار یافت نشد"**:

   - مطمئن شوید که تمام پیش‌نیازها نصب شده‌اند
   - در ویندوز، مطمئن شوید که مسیر نصب ابزارها به PATH اضافه شده است
   - در لینوکس/macOS، مطمئن شوید که دسترسی‌های لازم را دارید

2. **خطای "دسترسی رد شد"**:

   - در ویندوز: اسکریپت را با دسترسی Administrator اجرا کنید
   - در لینوکس/macOS: از sudo استفاده کنید

   ```bash
   sudo python setup.py
   ```

3. **خطای "اینترنت در دسترس نیست"**:

   - مطمئن شوید که به اینترنت متصل هستید
   - اگر از پراکسی استفاده می‌کنید، تنظیمات آن را بررسی کنید

4. **خطای "نسخه پایتون نامناسب"**:
   - مطمئن شوید که پایتون 3.8 یا بالاتر نصب شده است
   - در صورت نیاز، پایتون را به‌روزرسانی کنید

## مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add some amazing feature'`)
4. به Branch خود push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات بیشتر به فایل [LICENSE](LICENSE) مراجعه کنید.

## پشتیبانی

اگر با مشکلی مواجه شدید یا سوالی دارید:

1. ابتدا بخش عیب‌یابی را مطالعه کنید
2. در Issues گیت‌هاب پروژه، مشکل خود را گزارش دهید
3. برای مشارکت در بهبود پروژه، Pull Request ارسال کنید
