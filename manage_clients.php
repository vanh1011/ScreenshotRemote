<?php
// Đặt múi giờ Việt Nam (+7)
date_default_timezone_set('Asia/Ho_Chi_Minh');

// Xác định các thư mục và file
$uploadDir = 'uploads/';
$logFile = 'screenshots.log';

// Lấy danh sách các client
$clients = [];
if (file_exists($uploadDir) && is_dir($uploadDir)) {
    $clients = array_filter(glob($uploadDir . '*'), 'is_dir');
}

// Xử lý xóa một client
if (isset($_GET['action']) && $_GET['action'] === 'delete' && isset($_GET['client_id'])) {
    $clientId = $_GET['client_id'];
    $clientDir = $uploadDir . $clientId;
    
    // Kiểm tra xem thư mục client có tồn tại không
    if (file_exists($clientDir) && is_dir($clientDir)) {
        // Xóa tất cả các file trong thư mục client
        $files = glob($clientDir . '/*');
        foreach ($files as $file) {
            if (is_file($file)) {
                unlink($file);
            }
        }
        
        // Xóa thư mục client
        if (rmdir($clientDir)) {
            // Nếu xóa thành công, xóa bỏ client này khỏi file log
            if (file_exists($logFile)) {
                $logLines = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
                $newLogLines = [];
                
                foreach ($logLines as $line) {
                    $entry = json_decode($line, true);
                    if (!$entry || $entry['client_id'] !== $clientId) {
                        $newLogLines[] = $line;
                    }
                }
                
                // Ghi lại file log không có client đã xóa
                file_put_contents($logFile, implode("\n", $newLogLines) . (empty($newLogLines) ? '' : "\n"));
            }
            
            // Chuyển hướng về trang chính với thông báo thành công
            header('Location: index.php?client_deleted=' . urlencode($clientId));
            exit;
        }
    }
    
    // Nếu không xóa được, chuyển hướng với thông báo lỗi
    header('Location: index.php?error=delete_failed&client=' . urlencode($clientId));
    exit;
}

// Xử lý làm mới thông tin client (cập nhật tên)
if (isset($_GET['action']) && $_GET['action'] === 'refresh_name' && isset($_GET['client_id']) && isset($_GET['new_name'])) {
    $clientId = $_GET['client_id'];
    $newName = $_GET['new_name'];
    
    // Kiểm tra xem client có tồn tại không
    $clientDir = $uploadDir . $clientId;
    if (file_exists($clientDir) && is_dir($clientDir)) {
        // Cập nhật tên trong file log
        if (file_exists($logFile)) {
            $logLines = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            $newLogLines = [];
            $updated = false;
            
            foreach ($logLines as $line) {
                $entry = json_decode($line, true);
                if ($entry && $entry['client_id'] === $clientId) {
                    $entry['client_name'] = $newName;
                    $newLogLines[] = json_encode($entry);
                    $updated = true;
                } else {
                    $newLogLines[] = $line;
                }
            }
            
            // Nếu không tìm thấy client trong log, thêm mới một mục
            if (!$updated) {
                $newEntry = [
                    'client_id' => $clientId,
                    'client_name' => $newName,
                    'timestamp' => date('Y-m-d H:i:s'),
                    'filename' => 'updated_name_' . date('Ymd_His') . '.png',
                    'file_path' => $clientDir . '/placeholder.png',
                    'upload_time' => date('Y-m-d H:i:s')
                ];
                $newLogLines[] = json_encode($newEntry);
            }
            
            // Ghi lại file log với tên client đã cập nhật
            file_put_contents($logFile, implode("\n", $newLogLines) . "\n");
        }
        
        // Chuyển hướng về trang chính với thông báo thành công
        header('Location: index.php?name_updated=' . urlencode($clientId) . '&new_name=' . urlencode($newName));
        exit;
    }
    
    // Nếu không tìm thấy client, chuyển hướng với thông báo lỗi
    header('Location: index.php?error=client_not_found&client=' . urlencode($clientId));
    exit;
}

// Xử lý xóa tất cả máy đã offline
if (isset($_GET['action']) && $_GET['action'] === 'delete_offline') {
    $currentTime = time();
    $offlineThreshold = 600; // 10 phút
    $deletedCount = 0;
    
    foreach ($clients as $clientPath) {
        $clientId = basename($clientPath);
        $lastActive = 0;
        
        // Lấy danh sách ảnh của client
        $images = glob($clientPath . '/*.{jpg,jpeg,png,gif}', GLOB_BRACE);
        $latestImage = !empty($images) ? end($images) : null;
        
        if ($latestImage) {
            $imageModTime = filemtime($latestImage);
            if ($imageModTime > $lastActive) {
                $lastActive = $imageModTime;
            }
        }
        
        // Đọc log để lấy thời gian hoạt động
        if (file_exists($logFile)) {
            $logContent = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            foreach ($logContent as $line) {
                $entry = json_decode($line, true);
                if ($entry && isset($entry['client_id']) && $entry['client_id'] === $clientId) {
                    // Kiểm tra thời gian từ log
                    if (isset($entry['upload_time'])) {
                        $timestamp = strtotime($entry['upload_time']);
                        if ($timestamp && $timestamp > $lastActive) {
                            $lastActive = $timestamp;
                        }
                    }
                }
            }
        }
        
        // Nếu client đã offline, xóa thư mục và cập nhật log
        if ($currentTime - $lastActive > $offlineThreshold) {
            // Xóa tất cả các file trong thư mục client
            foreach ($images as $file) {
                if (is_file($file)) {
                    unlink($file);
                }
            }
            
            // Xóa thư mục client
            if (rmdir($clientPath)) {
                $deletedCount++;
                
                // Xóa client này khỏi file log
                if (file_exists($logFile)) {
                    $logLines = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
                    $newLogLines = [];
                    
                    foreach ($logLines as $line) {
                        $entry = json_decode($line, true);
                        if (!$entry || $entry['client_id'] !== $clientId) {
                            $newLogLines[] = $line;
                        }
                    }
                    
                    // Ghi lại file log không có client đã xóa
                    file_put_contents($logFile, implode("\n", $newLogLines) . (empty($newLogLines) ? '' : "\n"));
                }
            }
        }
    }
    
    // Chuyển hướng về trang chính với thông báo thành công
    header('Location: index.php?offline_deleted=' . $deletedCount);
    exit;
}

// Xử lý làm mới tất cả log
if (isset($_GET['action']) && $_GET['action'] === 'refresh_log') {
    // Tạo file log mới
    if (file_exists($logFile)) {
        unlink($logFile);
    }
    
    $logEntries = [];
    foreach ($clients as $clientPath) {
        $clientId = basename($clientPath);
        $clientName = isset($_GET['default_name']) ? $_GET['default_name'] : 'MacBook Pro';
        
        // Tạo một mục log mới cho client này
        $logEntry = [
            'client_id' => $clientId,
            'client_name' => $clientName,
            'timestamp' => date('Y-m-d H:i:s'),
            'filename' => 'refresh_' . date('Ymd_His') . '.png',
            'file_path' => $clientPath . '/refresh.png',
            'upload_time' => date('Y-m-d H:i:s')
        ];
        
        $logEntries[] = json_encode($logEntry);
    }
    
    // Ghi vào file log mới
    if (!empty($logEntries)) {
        file_put_contents($logFile, implode("\n", $logEntries) . "\n");
    }
    
    // Chuyển hướng về trang chính với thông báo thành công
    header('Location: index.php?log_refreshed=1');
    exit;
}
?>

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quản lý Máy Client</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4">Quản lý Máy Client</h1>
        <a href="index.php" class="btn btn-primary mb-4">Quay lại trang chính</a>
        
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Làm mới thông tin</h5>
                    </div>
                    <div class="card-body">
                        <p>Làm mới toàn bộ thông tin log để cập nhật tên máy.</p>
                        <form action="manage_clients.php" method="get">
                            <input type="hidden" name="action" value="refresh_log">
                            <div class="mb-3">
                                <label for="default_name" class="form-label">Tên máy mặc định</label>
                                <input type="text" class="form-control" id="default_name" name="default_name" value="MacBook Pro">
                            </div>
                            <button type="submit" class="btn btn-primary" onclick="return confirm('Bạn có chắc muốn làm mới toàn bộ log?')">Làm mới log</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-danger text-white">
                        <h5 class="mb-0">Xóa máy offline</h5>
                    </div>
                    <div class="card-body">
                        <p>Xóa tất cả các máy đã ngắt kết nối (offline) khỏi hệ thống.</p>
                        <a href="manage_clients.php?action=delete_offline" class="btn btn-danger" onclick="return confirm('Bạn có chắc muốn xóa TẤT CẢ máy đã offline?')">Xóa tất cả máy offline</a>
                    </div>
                </div>
            </div>
        </div>
        
        <h2 class="mb-3">Danh sách máy đã kết nối</h2>
        
        <?php if (empty($clients)): ?>
            <div class="alert alert-info">Chưa có máy nào kết nối</div>
        <?php else: ?>
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>ID</th>
                            <th>Tên hiện tại</th>
                            <th>Số ảnh</th>
                            <th>Hoạt động gần nhất</th>
                            <th>Trạng thái</th>
                            <th>Thao tác</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php 
                        $currentTime = time();
                        $onlineThreshold = 600; // 10 phút
                        
                        foreach ($clients as $clientPath): 
                            $clientId = basename($clientPath);
                            $clientName = "Unknown";
                            $lastActive = 0;
                            
                            // Lấy số lượng ảnh
                            $images = glob($clientPath . '/*.{jpg,jpeg,png,gif}', GLOB_BRACE);
                            $imageCount = count($images);
                            
                            // Lấy thời gian hoạt động gần nhất
                            $latestImage = !empty($images) ? end($images) : null;
                            if ($latestImage) {
                                $imageModTime = filemtime($latestImage);
                                if ($imageModTime > $lastActive) {
                                    $lastActive = $imageModTime;
                                }
                            }
                            
                            // Đọc log để lấy tên và thời gian
                            if (file_exists($logFile)) {
                                $logContent = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
                                $logContent = array_reverse($logContent); // Đọc từ mục mới nhất
                                
                                foreach ($logContent as $line) {
                                    $entry = json_decode($line, true);
                                    if ($entry && isset($entry['client_id']) && $entry['client_id'] === $clientId) {
                                        if (isset($entry['client_name']) && !empty($entry['client_name'])) {
                                            $clientName = $entry['client_name'];
                                            break; // Đã tìm thấy tên, dừng vòng lặp
                                        }
                                        
                                        if (isset($entry['upload_time'])) {
                                            $timestamp = strtotime($entry['upload_time']);
                                            if ($timestamp && $timestamp > $lastActive) {
                                                $lastActive = $timestamp;
                                            }
                                        }
                                    }
                                }
                            }
                            
                            // Kiểm tra trạng thái online/offline
                            $isOnline = ($currentTime - $lastActive < $onlineThreshold);
                            $statusClass = $isOnline ? 'success' : 'danger';
                            $statusText = $isOnline ? 'Online' : 'Offline';
                        ?>
                        <tr>
                            <td><?php echo htmlspecialchars($clientId); ?></td>
                            <td>
                                <form action="manage_clients.php" method="get" class="d-flex">
                                    <input type="hidden" name="action" value="refresh_name">
                                    <input type="hidden" name="client_id" value="<?php echo htmlspecialchars($clientId); ?>">
                                    <input type="text" class="form-control form-control-sm me-2" name="new_name" value="<?php echo htmlspecialchars($clientName); ?>">
                                    <button type="submit" class="btn btn-sm btn-primary">Cập nhật</button>
                                </form>
                            </td>
                            <td><?php echo $imageCount; ?></td>
                            <td><?php echo date('d/m/Y H:i:s', $lastActive); ?></td>
                            <td><span class="badge bg-<?php echo $statusClass; ?>"><?php echo $statusText; ?></span></td>
                            <td>
                                <a href="client_images.php?id=<?php echo urlencode($clientId); ?>" class="btn btn-sm btn-info">Xem ảnh</a>
                                <a href="manage_clients.php?action=delete&client_id=<?php echo urlencode($clientId); ?>" class="btn btn-sm btn-danger" onclick="return confirm('Bạn có chắc muốn xóa máy này?')">Xóa</a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html> 