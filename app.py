from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np

# Flaskアプリケーションの初期化
app = Flask(__name__)
CORS(app)  # すべてのエンドポイントに対してCORSを有効化

# 保存されたモデルをロード
model = tf.keras.models.load_model('model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image = data['image']
        
        # データをnumpy配列に変換し、形状を調整
        image = np.array(image, dtype=np.float32)
        
        # 画像データのサイズが正しいことを確認
        if image.size != 28 * 28:
            raise ValueError("Image data size is not 28x28 pixels")
        
        # 形状を調整してモデルに入力
        image = image.reshape((1, 28, 28, 1))  # グレースケール画像なので、チャンネル数は1
        
        # 画像データを正規化
        image /= 255.0
        
        prediction = model.predict(image)
        predicted_label = prediction.argmax(axis=-1)
        
        return jsonify({'predicted_label': int(predicted_label)})
    except Exception as e:
        print(f"Error: {e}")  # ターミナルにエラーを出力
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
