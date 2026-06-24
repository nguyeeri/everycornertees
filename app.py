import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'ai', 'svg', 'eps', 'psd'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form fields
        name        = request.form.get('name', '').strip()
        email       = request.form.get('email', '').strip()
        phone       = request.form.get('phone', '').strip()
        event_type  = request.form.get('event_type', '').strip()
        quantity    = request.form.get('quantity', '').strip()
        deadline    = request.form.get('deadline', '').strip()
        shirt_sizes = request.form.getlist('shirt_sizes')
        notes       = request.form.get('notes', '').strip()

        # Basic validation
        if not name or not email:
            return jsonify({'success': False, 'error': 'Name and email are required.'}), 400

        # Handle uploaded files
        files = request.files.getlist('designs')
        attachments = []
        for f in files:
            if f and f.filename and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_data = f.read()
                attachments.append((filename, file_data, f.content_type))

        # Build email body
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

        # Send email (configure via environment variables)
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_user = os.environ.get('SMTP_USER', '')
        smtp_pass = os.environ.get('SMTP_PASS', '')
        to_email  = os.environ.get('TO_EMAIL', smtp_user)

        if smtp_user and smtp_pass:
            msg = MIMEMultipart()
            msg['From']    = smtp_user
            msg['To']      = to_email
            msg['Subject'] = f'New Quote Request — {name} ({quantity} shirts)'
            msg['Reply-To'] = email

            msg.attach(MIMEText(body, 'plain'))

            for filename, file_data, content_type in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_data)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

        return jsonify({'success': True})

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'error': 'Something went wrong. Please email us directly.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
