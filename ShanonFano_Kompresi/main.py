from flask import Flask, render_template, request, send_file
from PIL import Image
import shannon_fano

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['file']
    compressed_image = shannon_fano.compress(file)
    compressed_image = compressed_image.convert('RGB')  # Ubah mode gambar menjadi RGB
    compressed_image.save('compressed_image.jpg', 'JPEG')
    return send_file('compressed_image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
