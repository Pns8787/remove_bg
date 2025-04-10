from flask import Flask, request, send_file, render_template  # Added render_template
from rembg import remove
import io
import os
import logging

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        output_image = remove(input_image)
        
        return send_file(
            io.BytesIO(output_image),
            mimetype='image/png',
            as_attachment=True,
            download_name='background_removed.png'
        )
    except Exception as e:
        app.logger.error(f'Processing error: {str(e)}')
        return {'error': 'Image processing failed'}, 500

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}

@app.route('/')
def index():
    return render_template('index.html')  # Now properly imported

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
