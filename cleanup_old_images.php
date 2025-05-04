<?php
// Thư mục chứa ảnh
$uploadDir = 'uploads/';

// Số ngày giữ lại ảnh (mặc định 1 ngày)
$daysToKeep = 1;

// Hàm xóa file cũ
function deleteOldFiles($directory, $days) {
    if (!is_dir($directory)) {
        return;
    }

    $files = glob($directory . '/*');
    $now = time();

    foreach ($files as $file) {
        if (is_file($file)) {
            if ($now - filemtime($file) >= $days * 24 * 60 * 60) {
                unlink($file);
            }
        } elseif (is_dir($file)) {
            deleteOldFiles($file, $days);
        }
    }
}

// Xóa ảnh cũ
deleteOldFiles($uploadDir, $daysToKeep);

echo "Đã xóa ảnh cũ thành công!\n"; 