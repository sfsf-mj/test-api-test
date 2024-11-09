import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# تحديد المجلد لحفظ الصور المرفوعة
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# إنشاء المجلد إذا لم يكن موجودًا
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# السماح بأنواع معينة من الملفات
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# وظيفة للتحقق إذا كانت الصورة بتنسيق صحيح
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# نقطة النهاية التي تستقبل الصورة
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # التحقق مما إذا كانت الصورة فعلاً باستخدام PIL
        try:
            img = Image.open(file_path)
            img.verify()  # التحقق من أن الملف هو صورة فعلًا
            return jsonify({'message': 'نعم صورة'}), 200
        except (IOError, SyntaxError):
            return jsonify({'message': 'ليست صورة'}), 400
    else:
        return jsonify({'message': 'ملف غير مدعوم'}), 400

if __name__ == '__main__':
    app.run(debug=True)
