from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
import subprocess
import json
import sys
import re


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تعریف مدل درخواست ورودی
class CodeRequest(BaseModel):
    code: str
    language: str  
    version: str = None  

def detect_language_version(code: str, language: str) -> str:
    """
    تشخیص خودکار نسخه زبان برنامه‌نویسی از روی کد
    """
    if language == "python":
       
        if "async def" in code or "await" in code:
            return "3.7"  
        elif "f'" in code or 'f"' in code:
            return "3.6"  
        elif "yield from" in code:
            return "3.3"  
        else:
            return "3.0"  
            
    elif language == "php":
        
        if "??=" in code or "??" in code:
            return "8.0"  
        elif "?->" in code:
            return "7.4"  
        elif "??" in code:
            return "7.0"  
        else:
            return "7.0"  
            
    elif language == "cpp":
       
        if "concept" in code or "requires" in code:
            return "20"  
        elif "co_await" in code or "co_yield" in code:
            return "17"  
        elif "auto" in code and "decltype" in code:
            return "11"  
        else:
            return "98" 
            
    elif language == "javascript":
       
        if "??=" in code or "??" in code:
            return "2020"  
        elif "?.=" in code or "?." in code:
            return "2019"  
        elif "async" in code and "await" in code:
            return "2017"  
        elif "class" in code and "extends" in code:
            return "2015"  
        else:
            return "5"  
            
    return None

def get_language_flags(language: str, version: str) -> list:
    """
    دریافت پرچم‌های مناسب برای هر زبان و نسخه
    """
    flags = []
    
    if language == "python":
        if version:
            
            flags.extend(['--py-version', version])
            
    elif language == "php":
        if version:
            
            
            pass
            
    elif language == "cpp":
        if version:
            
            if version == "20":
                flags.extend(['--std=c++20'])
            elif version == "17":
                flags.extend(['--std=c++17'])
            elif version == "11":
                flags.extend(['--std=c++11'])
            else:
                flags.extend(['--std=c++98'])
            
    elif language == "javascript":
        if version:
           
            
            pass
            
    return flags

def find_tool_path(tool_name: str, possible_paths: list) -> str:
    """
    یافتن مسیر ابزار مورد نظر در مسیرهای ممکن
    """
   
    try:
        if sys.platform == 'win32':
            result = subprocess.run(['where', tool_name], capture_output=True, text=True)
        else:
            result = subprocess.run(['which', tool_name], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass

   
    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None

def get_tool_paths():
    """
    تعریف مسیرهای ممکن برای هر ابزار
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return {
        'phpstan': [
            os.path.join(base_dir, 'vendor', 'bin', 'phpstan'),
            os.path.join(base_dir, 'vendor', 'bin', 'phpstan.bat'),
            'phpstan'
        ],
        'pylint': [
            'pylint',
            os.path.join(base_dir, 'venv', 'Scripts', 'pylint.exe'),
            os.path.join(base_dir, 'venv', 'bin', 'pylint')
        ],
        'cppcheck': [
            'cppcheck',
            r'C:\Program Files\Cppcheck\cppcheck.exe',
            r'C:\Program Files (x86)\Cppcheck\cppcheck.exe',
            '/usr/bin/cppcheck',
            '/usr/local/bin/cppcheck'
        ],
        'eslint': [
            'eslint',
            os.path.join(os.environ.get('APPDATA', ''), 'npm', 'eslint.cmd'),
            os.path.join(os.environ.get('APPDATA', ''), 'npm', 'node_modules', 'eslint', 'bin', 'eslint.js'),
            os.path.join(base_dir, 'node_modules', '.bin', 'eslint'),
            os.path.join(base_dir, 'node_modules', '.bin', 'eslint.cmd'),
            os.path.join(base_dir, 'node_modules', 'eslint', 'bin', 'eslint.js')
        ]
    }

def analyze_with_phpstan(code: str, version: str = None) -> dict:
    tool_paths = get_tool_paths()
    phpstan_path = find_tool_path('phpstan', tool_paths['phpstan'])
    
    if not phpstan_path:
        return {
            "issues": [],
            "error": "PHPStan یافت نشد. لطفاً مطمئن شوید که PHPStan نصب شده است."
        }

 
    if not version:
        version = detect_language_version(code, "php")

   
    version_flags = get_language_flags("php", version)

    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
        print(f"فایل موقت ایجاد شد در: {temp_file_path}")

    try:
        
        print(f"مسیر PHPStan: {phpstan_path}")
        print(f"مسیر فایل کد: {temp_file_path}")

    
        cmd = ['php', phpstan_path, 'analyse', '--error-format=json', '--configuration=phpstan.neon']
        if version_flags: 
            cmd.extend(version_flags)
        cmd.append(temp_file_path)

        print(f"دستور اجرایی: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print(f"خروجی استاندارد: {result.stdout}")
        print(f"خروجی خطا: {result.stderr}")
        
        
        if result.stdout:
            try:
                issues = json.loads(result.stdout)
                print(f"خروجی JSON: {issues}")
                formatted_issues = []
                
                
                if 'files' in issues:
                    for file_path, file_data in issues['files'].items():
                        if 'messages' in file_data:
                            for message in file_data['messages']:
                                formatted_issues.append({
                                    'type': 'ERROR',
                                    'line': message.get('line', 0),
                                    'message': message.get('message', ''),
                                    'path': os.path.basename(temp_file_path),
                                    'symbol': message.get('identifier', '')
                                })
                
                print(f"خطاهای فرمت شده: {formatted_issues}")
                return {
                    "issues": formatted_issues,
                    "error": None
                }
            except json.JSONDecodeError as e:
                print(f"خطا در پردازش JSON: {str(e)}")
                print(f"خروجی PHPStan: {result.stdout}")
                return {
                    "issues": [],
                    "error": f"خطا در پردازش خروجی phpstan: {str(e)}"
                }
        else:
            error_msg = result.stderr if result.stderr else "هیچ خطایی یافت نشد"
            print(f"خطای PHPStan: {error_msg}")
            return {
                "issues": [],
                "error": error_msg
            }
    except Exception as e:
        print(f"خطای غیرمنتظره: {str(e)}")
        return {
            "issues": [],
            "error": f"خطای غیرمنتظره: {str(e)}"
        }
    finally:
    
        try:
            os.unlink(temp_file_path)
            print(f"فایل موقت حذف شد: {temp_file_path}")
        except Exception as e:
            print(f"خطا در حذف فایل موقت: {str(e)}")

def analyze_with_pylint(code: str, version: str = None) -> dict:
    tool_paths = get_tool_paths()
    pylint_path = find_tool_path('pylint', tool_paths['pylint'])
    
    if not pylint_path:
        return {
            "issues": [],
            "error": "Pylint یافت نشد. لطفاً مطمئن شوید که Pylint نصب شده است."
        }

    
    if not version:
        version = detect_language_version(code, "python")

    
    version_flags = get_language_flags("python", version)

    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        
        print(f"مسیر pylint: {pylint_path}")
        print(f"مسیر فایل کد: {temp_file_path}")

        
        cmd = [pylint_path, '--output-format=json', '--disable=C0111']
        if version_flags:  
            cmd.extend(version_flags)
        cmd.append(temp_file_path)

        print(f"دستور اجرایی: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        
        if result.stdout:
            try:
                issues = json.loads(result.stdout)
                
                for issue in issues:
                    issue['path'] = os.path.basename(issue['path'])
                return {
                    "issues": issues,
                    "error": None
                }
            except json.JSONDecodeError:
                return {
                    "issues": [],
                    "error": "خطا در پردازش خروجی pylint"
                }
        else:
            return {
                "issues": [],
                "error": result.stderr if result.stderr else "هیچ خطایی یافت نشد"
            }
    finally:
        
        os.unlink(temp_file_path)

def analyze_with_cppcheck(code: str, language: str, version: str = None) -> dict:
    tool_paths = get_tool_paths()
    cppcheck_path = find_tool_path('cppcheck', tool_paths['cppcheck'])
    
    if not cppcheck_path:
        return {
            "issues": [],
            "error": "Cppcheck یافت نشد. لطفاً مطمئن شوید که Cppcheck نصب شده است."
        }


    if not version:
        version = detect_language_version(code, language)

    
    version_flags = get_language_flags(language, version)

    
    file_extension = '.cpp' if language == 'cpp' else '.c'
    
    
    with tempfile.NamedTemporaryFile(mode='w', suffix=file_extension, delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code)
        temp_file_path = os.path.abspath(temp_file.name)  
        print(f"فایل موقت ایجاد شد در: {temp_file_path}")

    try:
        
        cmd = [
            cppcheck_path,
            '--xml',
            '--xml-version=2',
            '--enable=all',
            '--inconclusive'
        ]
        
        
        if language == 'cpp':
            cmd.extend(['--language=c++'])
        else:
            cmd.extend(['--language=c'])
            
        cmd.extend(version_flags)  
        cmd.append(temp_file_path)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=os.path.dirname(temp_file_path)
        )
        
        print(f"خروجی استاندارد: {result.stdout}")
        print(f"خروجی خطا: {result.stderr}")
        
        
        if result.stderr:
            try:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(result.stderr)
                formatted_issues = []
                
                
                for error in root.findall('.//error'):
                    
                    if error.get('severity') == 'information':
                        continue
                        
                    formatted_issues.append({
                        'type': 'ERROR',
                        'line': int(error.get('line', 0)),
                        'message': error.get('msg', ''),
                        'path': os.path.basename(temp_file_path),
                        'symbol': error.get('id', '')
                    })
                
                print(f"خطاهای فرمت شده: {formatted_issues}")
                return {
                    "issues": formatted_issues,
                    "error": None
                }
            except ET.ParseError as e:
                print(f"خطا در پردازش XML: {str(e)}")
                print(f"خروجی Cppcheck: {result.stderr}")
                return {
                    "issues": [],
                    "error": f"خطا در پردازش خروجی cppcheck: {str(e)}"
                }
        else:
            error_msg = result.stdout if result.stdout else "هیچ خطایی یافت نشد"
            print(f"خطای Cppcheck: {error_msg}")
            return {
                "issues": [],
                "error": error_msg
            }
    except Exception as e:
        print(f"خطای غیرمنتظره: {str(e)}")
        return {
            "issues": [],
            "error": f"خطای غیرمنتظره: {str(e)}"
        }
    finally:
        
        try:
            os.unlink(temp_file_path)
            print(f"فایل موقت حذف شد: {temp_file_path}")
        except Exception as e:
            print(f"خطا در حذف فایل موقت: {str(e)}")

def analyze_with_eslint(code: str, version: str = None) -> dict:
    tool_paths = get_tool_paths()
    eslint_path = find_tool_path('eslint', tool_paths['eslint'])
    
    if not eslint_path:
        return {
            "issues": [],
            "error": "ESLint یافت نشد. لطفاً مطمئن شوید که ESLint نصب شده است."
        }

    
    if not version:
        version = detect_language_version(code, "javascript")

    
    version_flags = get_language_flags("javascript", version)

    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
        print(f"فایل موقت ایجاد شد در: {temp_file_path}")

    try:
        
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.eslintrc.json')
        if not os.path.exists(config_path):
            print(f"فایل پیکربندی ESLint یافت نشد: {config_path}")
            return {
                "issues": [],
                "error": "فایل پیکربندی ESLint یافت نشد"
            }

       
        if sys.platform == 'win32':
            
            cmd = ['npx.cmd', 'eslint', '--format=json', '--config', config_path]
        else:
            
            cmd = ['node', eslint_path, '--format=json', '--config', config_path]

        if version_flags:  
            cmd.extend(version_flags)
        cmd.append(temp_file_path)

        print(f"دستور اجرایی: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        
        if result.stdout:
            try:
                issues = json.loads(result.stdout)
                formatted_issues = []
                
                
                for file_issues in issues:
                    for issue in file_issues.get('messages', []):
                        formatted_issues.append({
                            'type': 'ERROR' if issue.get('severity') == 2 else 'WARNING',
                            'line': issue.get('line', 0),
                            'message': issue.get('message', ''),
                            'path': os.path.basename(temp_file_path),
                            'symbol': issue.get('ruleId', '')
                        })
                
                return {
                    "issues": formatted_issues,
                    "error": None
                }
            except json.JSONDecodeError as e:
                print(f"خطا در پردازش JSON: {str(e)}")
                return {
                    "issues": [],
                    "error": f"خطا در پردازش خروجی ESLint: {str(e)}"
                }
        else:
            return {
                "issues": [],
                "error": result.stderr if result.stderr else "هیچ خطایی یافت نشد"
            }
    except Exception as e:
        print(f"خطای غیرمنتظره: {str(e)}")
        return {
            "issues": [],
            "error": f"خطای غیرمنتظره: {str(e)}"
        }
    finally:
        
        try:
            os.unlink(temp_file_path)
            print(f"فایل موقت حذف شد: {temp_file_path}")
        except Exception as e:
            print(f"خطا در حذف فایل موقت: {str(e)}")

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    try:
        
        if not request.version:
            request.version = detect_language_version(request.code, request.language)

        if request.language == "python":
            result = analyze_with_pylint(request.code, request.version)
        elif request.language == "php":
            result = analyze_with_phpstan(request.code, request.version)
        elif request.language == "javascript":
            result = analyze_with_eslint(request.code, request.version)
        else:
            result = analyze_with_cppcheck(request.code, request.language, request.version)
        
        return {"result": result}
    except Exception as e:
        print(f"خطای غیرمنتظره در تحلیل کد: {str(e)}")
        return {"result": {"error": f"خطای غیرمنتظره: {str(e)}"}}
