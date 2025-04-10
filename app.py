from flask import Flask, request, send_file, render_template
from rembg import remove
import io
import os
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
app.logger.setLevel(logging.INFO)

# Configure model path for Render.com
os.makedirs('/tmp/.u2net', exist_ok=True)
os.environ['U2NET_HOME'] = '/tmp/.u2net'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400
    
    file = request.files['image']
    
    if file.filename == '':
        return {'error': 'Empty filename'}, 400
        
    if not allowed_file(file.filename):
        return {'error': 'Invalid file type'}, 400

    try:
        input_image = file.read()
        # Use smaller u2netp model for free tier compatibility
        output_image = remove(input_image, model='u2netp')
        
        return send_file(
            io.BytesIO(output_image),
            mimetype='image/png',
            as_attachment=True,
            download_name=f'bg_removed_{secure_filename(file.filename)}'
        )
    except Exception as e:
        app.logger.error(f'Processing error: {str(e)}')
        return {'error': 'Image processing failed'}, 500

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
