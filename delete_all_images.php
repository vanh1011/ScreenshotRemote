<?php
// Kiểm tra yêu cầu xóa
if (!isset($_GET['client_id'])) {
    header("Location: index.php");
    exit;
}

$clientId = $_GET['client_id'];
$uploadDir = 'uploads/' . $clientId . '/';

// Kiểm tra xem thư mục có tồn tại không
if (!file_exists($uploadDir) || !is_dir($uploadDir)) {
    header("Location: index.php?error=not_found");
    exit;
}

// Lấy danh sách tất cả ảnh
$images = glob($uploadDir . '/*.{jpg,jpeg,png,gif}', GLOB_BRACE);

// Đếm số ảnh đã xóa
$deletedCount = 0;

// Xóa từng ảnh
foreach ($images as $image) {
    if (is_file($image) && unlink($image)) {
        $deletedCount++;
    }
}

// Chuyển hướng về trang chủ với thông báo
header("Location: index.php?deleted=$deletedCount&client=$clientId");
exit;
?> 