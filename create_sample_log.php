<?php
// Tạo dữ liệu log mẫu để sửa lỗi "Unknown"

// Lấy danh sách thư mục client
$uploadDir = 'uploads/';
$clients = array_filter(glob($uploadDir . '*'), 'is_dir');

if (empty($clients)) {
    echo "Không tìm thấy thư mục client nào.\n";
    exit;
}

$logFile = 'screenshots.log';
$logEntries = [];

// Tạo dữ liệu log cho mỗi client
foreach ($clients as $clientPath) {
    $clientId = basename($clientPath);
    
    // Tạo một mục log mới cho client này
    $logEntry = [
        'client_id' => $clientId,
        'client_name' => 'MacBook Pro', // Đặt tên máy thành "MacBook Pro"
        'timestamp' => date('Y-m-d H:i:s'),
        'filename' => 'sample_' . date('Ymd_His') . '.png',
        'file_path' => $clientPath . '/sample.png',
        'upload_time' => date('Y-m-d H:i:s')
    ];
    
    // Thêm vào mảng log
    $logEntries[] = json_encode($logEntry);
}

// Ghi vào file log
if (!empty($logEntries)) {
    file_put_contents($logFile, implode("\n", $logEntries) . "\n", FILE_APPEND);
    echo "Đã tạo " . count($logEntries) . " mục log mẫu.\n";
    echo "File log: " . realpath($logFile) . "\n";
} else {
    echo "Không có dữ liệu log nào được tạo.\n";
}

echo "Hoàn tất.\n"; 