<?php
if (!isset($_GET['file']) || !isset($_GET['client'])) {
    header('Location: index.php');
    exit;
}

$filePath = $_GET['file'];
$clientId = $_GET['client'];

// Kiểm tra đường dẫn file hợp lệ (nằm trong thư mục uploads)
if (strpos($filePath, 'uploads/') !== 0 || strpos($filePath, '..') !== false) {
    header('Location: index.php');
    exit;
}

// Kiểm tra file tồn tại
if (file_exists($filePath)) {
    // Xóa file
    unlink($filePath);
}

// Chuyển về trang danh sách ảnh của client
header('Location: client_images.php?id=' . urlencode($clientId));
exit; 