import CodeInput from './components/CodeInput';
import './App.css'
function App() {
  const handleCodeSubmit = (code) => {
    console.log('کد ارسال شده:', code);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1 className='title'>سامانه خطایابی کد</h1>
      <p className='des'>جهت انجام خطایابی کد خود  را وارد کنید و دکمه تحلیل کد را کلیک کنید همچنین میتوانید فایل خود را آپلود و یا کدهای مورد نظر را بکشید و در ورودی بیندازید.</p>
      <p className='des'>نتیجه تحلیل آسیب پذیری ها در خروجی نمایش داده میشوند و شدت خطاها بارنگ مختص ارور مشخص میشوند.</p>
      <p className='des'>جهت عملکرد بهتر خطایابی بهتر است کامنت ها همراه با کد ارسال نشوند.</p>
     
      <CodeInput onSubmit={handleCodeSubmit} />
    </div>
  );
}

export default App;
