import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_python_version():
    """بررسی نسخه پایتون"""
    if sys.version_info < (3, 8):
        print("خطا: نیاز به پایتون 3.8 یا بالاتر است")
        sys.exit(1)

def install_python_dependencies():
    """نصب وابستگی‌های پایتون"""
    print("در حال نصب وابستگی‌های پایتون...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pylint"])

def install_node_dependencies():
    """نصب وابستگی‌های Node.js"""
    print("در حال نصب وابستگی‌های Node.js...")
    subprocess.check_call(["npm", "install", "eslint", "--save-dev"])

def install_phpstan():
    """نصب PHPStan"""
    print("در حال نصب PHPStan...")
    if not os.path.exists("composer.json"):
        subprocess.check_call(["composer", "init", "--no-interaction"])
    subprocess.check_call(["composer", "require", "phpstan/phpstan", "--dev"])

def install_cppcheck():
    """نصب Cppcheck"""
    system = platform.system().lower()
    print(f"در حال نصب Cppcheck برای {system}...")
    
    if system == "windows":
        # دانلود و نصب Cppcheck در ویندوز
        cppcheck_url = "https://github.com/danmar/cppcheck/releases/download/2.12.1/cppcheck-2.12.1-x64-Setup.msi"
        cppcheck_installer = "cppcheck_installer.msi"
        
        try:
            import urllib.request
            print("در حال دانلود Cppcheck...")
            urllib.request.urlretrieve(cppcheck_url, cppcheck_installer)
            
            print("در حال نصب Cppcheck...")
            subprocess.check_call(["msiexec", "/i", cppcheck_installer, "/quiet"])
            
            # اضافه کردن به PATH
            install_dir = r"C:\Program Files\Cppcheck"
            if install_dir not in os.environ["PATH"]:
                os.environ["PATH"] = install_dir + os.pathsep + os.environ["PATH"]
            
            
            os.remove(cppcheck_installer)
            
        except Exception as e:
            print(f"خطا در نصب Cppcheck: {e}")
            print("لطفاً Cppcheck را به صورت دستی نصب کنید")
    
    elif system == "linux":
        # نصب Cppcheck در لینوکس
        try:
            if shutil.which("apt-get"):
                subprocess.check_call(["sudo", "apt-get", "install", "-y", "cppcheck"])
            elif shutil.which("yum"):
                subprocess.check_call(["sudo", "yum", "install", "-y", "cppcheck"])
            else:
                print("خطا: نتوانستیم Cppcheck را نصب کنیم")
                print("لطفاً Cppcheck را به صورت دستی نصب کنید")
        except Exception as e:
            print(f"خطا در نصب Cppcheck: {e}")
    
    elif system == "darwin":
        # نصب Cppcheck در macOS
        try:
            subprocess.check_call(["brew", "install", "cppcheck"])
        except Exception as e:
            print(f"خطا در نصب Cppcheck: {e}")
            print("لطفاً Cppcheck را به صورت دستی نصب کنید")

def create_config_files():
    """ایجاد فایل‌های پیکربندی"""
    print("در حال ایجاد فایل‌های پیکربندی...")
    
    
    eslint_config = {
        "env": {
            "browser": True,
            "es2021": True,
            "node": True
        },
        "extends": "eslint:recommended",
        "parserOptions": {
            "ecmaVersion": 2021,
            "sourceType": "module"
        },
        "rules": {
            "indent": ["error", 2],
            "linebreak-style": ["error", "unix"],
            "quotes": ["error", "single"],
            "semi": ["error", "always"],
            "no-unused-vars": "warn",
            "no-console": "warn"
        }
    }
    
    with open(".eslintrc.json", "w") as f:
        import json
        json.dump(eslint_config, f, indent=2)
    
    
    phpstan_config = """parameters:
    level: 5
    paths:
        - .
"""
    with open("phpstan.neon", "w") as f:
        f.write(phpstan_config)

def main():
    """تابع اصلی نصب"""
    print("شروع نصب وابستگی‌ها...")
    
    # بررسی نسخه پایتون
    check_python_version()
    

    install_python_dependencies()
    install_node_dependencies()
    install_phpstan()
    install_cppcheck()
    
    
    create_config_files()
    
    print("نصب با موفقیت انجام شد!")

if __name__ == "__main__":
    main() 