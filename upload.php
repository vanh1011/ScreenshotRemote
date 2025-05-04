<?php
// Đặt múi giờ Việt Nam (+7)
date_default_timezone_set('Asia/Ho_Chi_Minh');

header('Content-Type: application/json');

// Thư mục lưu ảnh nhận được
$uploadDir = 'uploads/';

// Tạo thư mục nếu chưa tồn tại
if (!file_exists($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

// Kiểm tra request
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Phương thức không được hỗ trợ']);
    exit;
}

// Kiểm tra thông tin client
if (!isset($_POST['client_id']) || !isset($_POST['client_name'])) {
    echo json_encode(['success' => false, 'message' => 'Thiếu thông tin client']);
    exit;
}

// Kiểm tra file upload
if (!isset($_FILES['screenshot']) || $_FILES['screenshot']['error'] !== UPLOAD_ERR_OK) {
    echo json_encode([
        'success' => false, 
        'message' => 'Lỗi upload: ' . ($_FILES['screenshot']['error'] ?? 'Không có file')
    ]);
    exit;
}

// Lấy thông tin client
$clientId = $_POST['client_id'];
$clientName = $_POST['client_name'] ?? 'Unknown';
$timestamp = $_POST['timestamp'] ?? date('Y-m-d H:i:s');

// Tạo thư mục theo client_id nếu chưa có
$clientDir = $uploadDir . $clientId . '/';
if (!file_exists($clientDir)) {
    mkdir($clientDir, 0777, true);
}

// Tạo tên file với timestamp
$fileExtension = pathinfo($_FILES['screenshot']['name'], PATHINFO_EXTENSION);
$fileName = date('Ymd_His', strtotime($timestamp)) . '.' . $fileExtension;
$filePath = $clientDir . $fileName;

// Lưu file
if (move_uploaded_file($_FILES['screenshot']['tmp_name'], $filePath)) {
    // Lưu thông tin vào cơ sở dữ liệu
    $logFile = 'screenshots.log';
    $logEntry = json_encode([
        'client_id' => $clientId,
        'client_name' => $clientName,
        'timestamp' => $timestamp,
        'filename' => $fileName,
        'file_path' => $filePath,
        'upload_time' => date('Y-m-d H:i:s')
    ]) . "\n";
    
    file_put_contents($logFile, $logEntry, FILE_APPEND);
    
    echo json_encode([
        'success' => true,
        'message' => 'Upload thành công',
        'file' => $fileName
    ]);
} else {
    echo json_encode([
        'success' => false,
        'message' => 'Lỗi khi lưu file: ' . error_get_last()['message'] ?? 'Không rõ nguyên nhân'
    ]);
} 