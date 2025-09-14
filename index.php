<?php
$csvUrl = '';
$csvFileName = '';
$csvDir = __DIR__ . '/tmp_csv';  // папка для веб-доступа
if(!is_dir($csvDir)) mkdir($csvDir, 0777, true);

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $fileTmpPath = $_FILES['file']['tmp_name'];
    $fileName = $_FILES['file']['name'];

    // URL вашего Python OCR сервера
    $ocrServerUrl = 'https://finovators.onrender.com/ocr';

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $ocrServerUrl);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

    $cfile = new CURLFile($fileTmpPath, mime_content_type($fileTmpPath), $fileName);
    curl_setopt($ch, CURLOPT_POSTFIELDS, ['file' => $cfile]);

    $response = curl_exec($ch);
    curl_close($ch);

    if($response) {
        // Сохраняем CSV в папку tmp_csv
        $csvFileName = 'output_' . time() . '.csv';
        $csvFilePath = $csvDir . '/' . $csvFileName;
        file_put_contents($csvFilePath, $response);

        // URL для браузера
        $csvUrl = 'tmp_csv/' . $csvFileName;
    } else {
        $csvUrl = '';
    }
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>OCR PDF → CSV</title>
<style>
body { font-family: Arial; max-width: 700px; margin: 50px auto; }
input[type="file"] { margin-bottom: 10px; }
button { margin-top: 5px; }
</style>
</head>
<body>
<h2>OCR PDF → CSV</h2>
<form method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".pdf,image/*" required><br>
    <button type="submit">Распознать и скачать CSV</button>
</form>

<?php if(!empty($csvUrl) && file_exists($csvDir . '/' . $csvFileName)): ?>
    <h3>Распознанный CSV:</h3>
    <a href="<?= htmlspecialchars($csvUrl) ?>" download="<?= htmlspecialchars($csvFileName) ?>">
        <button>Скачать CSV</button>
    </a>
<?php endif; ?>
</body>
</html>
