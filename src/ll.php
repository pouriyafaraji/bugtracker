<?php
// ❌ 1. Syntax Error - فراموشی ;
echo "Hello, World!" ;
// ❌ 2. Undefined Variable

// ❌ 3. Type Error - جمع رشته و عدد
$number = 5;
echo $number + "five";
// ❌ 4. Unused Variable
$notUsed = 42;

// ❌ 5. Code Style Issue - بدون فاصله مناسب و نام‌گذاری اشتباه
function BadFunctionname($ARG1){
return$ARG1*2;
}
// ❌ 6. Long Function - تابع بیش از حد طولانی با پیچیدگی بالا
function complexLogic($x) {
    if ($x > 0) {
        if ($x < 10) {
            if ($x % 2 == 0) {
                echo "even";
            } else {
                echo "odd";
            }
        }
    }
    for ($i = 0; $i < 100; $i++) {
        echo $i;
    }
}
// ❌ 7. Security Issue - استفاده از eval با ورودی کاربر
$user_input = $_GET['input'];
eval($user_input);

// ❌ 8. Type Hint Mismatch (برای ابزارهایی که پشتیبانی کنن)
function addNumbers(int $a, int $b): int {
    return $a + $b;
}
addNumbers(5, "ten"); // ten is a string, causes issue
// ❌ 9. Logic Error - شرط اشتباه
$age = 20;
if ($age < 10 && $age > 30) {
    echo "Age is between 10 and 30";
}
// ❌ 10. Deprecated Function
split(",", "a,b,c"); // تابع منسوخ‌شده
?>
