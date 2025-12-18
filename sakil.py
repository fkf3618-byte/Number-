from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

# HTML এবং CSS কোডটি একটি মাল্টি-লাইন স্ট্রিং-এ রাখা হয়েছে
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Number Info Tool </title>
<style>
body{
    background:#04070f;
    font-family:Arial, sans-serif;
    color:#fff;
    padding:20px;
}
.box{
    max-width:430px;
    margin:auto;
    background:#0b1220;
    padding:25px;
    border-radius:15px;
    box-shadow:0 0 35px rgba(0,255,160,.35);
}
.alpha-name{
    text-align:center;
    font-size:34px;
    font-weight:900;
    letter-spacing:3px;
    margin-bottom:10px;
}
.alpha-name span{
    display:inline-block;
    color:#00ff88;
    animation:letterGlow 1.8s infinite;
    text-shadow:0 0 8px #00ff88;
}
.alpha-name span:nth-child(1){animation-delay:0s}
.alpha-name span:nth-child(2){animation-delay:.1s}
.alpha-name span:nth-child(3){animation-delay:.2s}
.alpha-name span:nth-child(4){animation-delay:.3s}
.alpha-name span:nth-child(5){animation-delay:.4s}
.alpha-name span:nth-child(6){animation-delay:.5s}
.alpha-name span:nth-child(7){animation-delay:.6s}
.alpha-name span:nth-child(8){animation-delay:.7s}
.alpha-name span:nth-child(9){animation-delay:.8s}
.alpha-name span:nth-child(10){animation-delay:.9s}
.alpha-name span:nth-child(11){animation-delay:1s}
.alpha-name span:nth-child(12){animation-delay:1.1s}
@keyframes letterGlow{
    0%{ opacity:.3; transform:scale(1); text-shadow:none; }
    50%{ opacity:1; transform:scale(1.25); text-shadow: 0 0 10px #00ff88, 0 0 30px #00ffaa; }
    100%{ opacity:.3; transform:scale(1); text-shadow:none; }
}
.small{
    text-align:center;
    font-size:12px;
    color:#aaa;
    margin-bottom:15px;
}
input{
    width:100%;
    padding:12px;
    font-size:16px;
    border:none;
    border-radius:8px;
    box-sizing: border-box; /* প্যাডিং এর কারণে বক্স বড় হওয়া ঠেকাতে */
}
button{
    width:100%;
    margin-top:10px;
    padding:12px;
    border:none;
    border-radius:8px;
    background:#00ff88;
    font-size:16px;
    font-weight:bold;
    cursor:pointer;
}
.result{
    margin-top:15px;
    background:#081a14;
    padding:15px;
    border-radius:10px;
    line-height:1.7;
}
a{
    color:#00ffcc;
    font-weight:bold;
    text-decoration:none;
}
</style>
</head>
<body>
<div class="box">
    <div class="alpha-name">
        <span>2</span><span>x</span><span>f</span><span>a</span><span>s</span><span>t</span>
        <span>&nbsp;</span>
        <span>S</span><span>A</span><span>K</span><span>I</span><span>L</span>
    </div>
    <div class="small">Ultimate Number Information Tool (Python)</div>
    
    <!-- ফর্মটি এখন POST মেথড ব্যবহার করে ডাটা পাঠাবে -->
    <form method="post">
        <input type="text" name="number" placeholder="Enter any number" required>
        <button type="submit">Check Info</button>
    </form>
    
    <!-- ফলাফল এখানে দেখানো হবে -->
    {% if result_html %}
        {{ result_html | safe }}
    {% endif %}
</div>
</body>
</html>
"""

def get_operator(n):
    """বাংলাদেশী মোবাইল অপারেটর খুঁজে বের করে"""
    prefix = n[:3]
    operators = {
        '017': 'Grameenphone', '013': 'Grameenphone',
        '019': 'Banglalink', '014': 'Banglalink',
        '018': 'Robi', '016': 'Airtel', '015': 'Teletalk'
    }
    return operators.get(prefix, 'Unknown')

def get_whatsapp_link(n):
    """WhatsApp লিঙ্ক তৈরি করে"""
    international_number = re.sub(r'^0', '880', n)
    return f"https://wa.me/{international_number}"

def get_facebook_link(n):
    """Facebook সার্চ লিঙ্ক তৈরি করে"""
    return f"https://www.facebook.com/search/top/?q={n}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = ""
    if request.method == 'POST':
        raw_number = request.form['number']
        # শুধুমাত্র সংখ্যা রেখে অন্য সবকিছু বাদ দিন
        number = re.sub(r'[^0-9]', '', raw_number)
        
        processed_number = ""
        error_message = ""

        # নম্বরটিকে ১১ ডিজিটের ফরম্যাটে নিয়ে আসা
        if len(number) == 11 and number.startswith('01'):
            processed_number = number
        elif len(number) == 13 and number.startswith('880'):
            processed_number = number[2:]
        else:
            error_message = "<b>Invalid Number Format!</b><br>Please enter a valid Bangladeshi mobile number (11 digits starting with 01 or 13 digits starting with 880)."

        if not error_message:
            # ফলাফল তৈরি করুন
            result_html = f"""
            <div class='result'>
                <b>Number:</b> {processed_number} <br>
                <b>Length:</b> {len(processed_number)}<br>
                <b>Operator:</b> {get_operator(processed_number)}<br>
                <b>WhatsApp:</b> <a href='{get_whatsapp_link(processed_number)}' target='_blank'>Open Chat</a><br>
                <b>Facebook:</b> <a href='{get_facebook_link(processed_number)}' target='_blank'>Search ID</a>
            </div>
            """
        else:
            # ত্রুটি মেসেজ দেখান
            result_html = f"<div class='result'>{error_message}</div>"

    # HTML টেমপ্লেটটি রেন্ডার করুন
    return render_template_string(HTML_TEMPLATE, result_html=result_html)

if __name__ == '__main__':
    # ডিবাগ মোডে অ্যাপটি চালানো হচ্ছে
    # host='0.0.0.0' মানে আপনার লোকাল নেটওয়ার্কের যেকোনো ডিভাইস থেকে এক্সেস করা যাবে
    app.run(host='0.0.0.0', port=5000, debug=True)