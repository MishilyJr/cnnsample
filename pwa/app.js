document.getElementById('submitBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('imageUpload');
    const resultElement = document.getElementById('result');
    
    if (fileInput.files.length === 0) {
        resultElement.textContent = 'Please upload an image.';
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = async function(event) {
        const image = new Image();
        image.src = event.target.result;

        image.onload = async function() {
            // 画像を28x28にリサイズ
            const canvas = document.createElement('canvas');
            canvas.width = 28;
            canvas.height = 28;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(image, 0, 0, 28, 28);

            // 画像データを取得
            const imageData = ctx.getImageData(0, 0, 28, 28);
            const data = Array.from(imageData.data).filter((_, index) => index % 4 === 0);
            
            // サイズを確認
            if (data.length !== 28 * 28) {
                resultElement.textContent = 'Image data size is incorrect.';
                return;
            }

            // サーバーにPOSTリクエストを送信
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: data })
            });

            const result = await response.json();
            resultElement.textContent = `Predicted Label: ${result.predicted_label}`;
        };
    };

    reader.readAsDataURL(file);
});
