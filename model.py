import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

# MNISTデータセットのロード
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# データの前処理
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# モデル定義
model = models.Sequential()
model.add(layers.MaxPooling2D(pool_size=(2, 2),input_shape=(28,28,1)))
model.add(layers.Conv2D(16, (3, 3), activation='relu' )) 
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))  
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu')) 
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_data=(test_images, test_labels))
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'Test accuracy: {test_acc:.4f}')

# モデルのトレーニング後にモデルを保存
model.save('model.h5')
