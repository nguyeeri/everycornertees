import os
import base64
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import resend

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'ai', 'svg', 'eps', 'psd', 'cdr'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name        = request.form.get('name', '').strip()
        email       = request.form.get('email', '').strip()
        phone       = request.form.get('phone', '').strip()
        event_type  = request.form.get('event_type', '').strip()
        quantity    = request.form.get('quantity', '').strip()
        deadline    = request.form.get('deadline', '').strip()
        shirt_sizes = request.form.getlist('shirt_sizes')
        notes       = request.form.get('notes', '').strip()

        if not name or not email:
            return jsonify({'success': False, 'error': 'Name and email are required.'}), 400

        files = request.files.getlist('designs')
        attachments = []
        for f in files:
            if f and f.filename and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_data = f.read()
                attachments.append({
                    "filename": filename,
                    "content": base64.b64encode(file_data).decode('utf-8')
                })

        sizes_str = ', '.join(shirt_sizes) if shirt_sizes else 'Not specified'
        body = f"""New quote request from Every Corner Tees website!

Name:       {name}
Email:      {email}
Phone:      {phone or 'Not provided'}
Event type: {event_type}
Quantity:   {quantity}
Deadline:   {deadline}
Sizes:      {sizes_str}

Notes / details:
{notes or 'None'}

Files attached: {len(attachments)}
"""

        resend.api_key = os.environ.get('RESEND_API_KEY', '')
        to_email = os.environ.get('TO_EMAIL', '')

        if resend.api_key and to_email:
            params = {
                "from": "Every Corner Tees <onboarding@resend.dev>",
                "to": [to_email],
                "reply_to": email,
                "subject": f"New Quote Request from {name} ({quantity} shirts)",
                "text": body,
                "attachments": attachments
            }
            resend.Emails.send(params)

        return jsonify({'success': True})

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': 'Something went wrong. Please email us directly.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
