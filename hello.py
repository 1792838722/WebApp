import json, base64, os
from flask import Flask, request, jsonify

from exercise import test_out, Show_result
from img_to_base64 import img_to_base64

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    raw_data = request.get_json()
    raw_file = base64.b64decode(json.loads(raw_data)['raw_file'])
    patient_name = json.loads(raw_data)['patient_name']
    upload_time = json.loads(raw_data)['time']

    folder_path = os.path.join('patients', upload_time, patient_name)
    os.makedirs(folder_path)

    with open(os.path.join(folder_path, patient_name), 'wb') as file:
        file.write(raw_file)
    file.close()
    test_out.generate_mha(folder_path)
    Show_result.generate_img(folder_path=folder_path, patient_name=patient_name)

    return jsonify({
        'pre_img': img_to_base64(os.path.join(folder_path, patient_name + '_pre.png')),
        'tar_img': img_to_base64(os.path.join(folder_path, patient_name + '_tar.png'))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12500)