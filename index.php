<?php
// Đặt múi giờ Việt Nam (+7)
date_default_timezone_set('Asia/Ho_Chi_Minh');
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quản lý Ảnh Chụp Màn Hình</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .screenshot-container {
            margin: 20px 0;
        }
        .screenshot-img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            cursor: pointer;
        }
        .modal-img {
            max-width: 100%;
            height: auto;
        }
        .client-card {
            margin-bottom: 20px;
        }
        .client-status {
            position: absolute;
            right: 10px;
            top: 10px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .status-online {
            background-color: #28a745;
        }
        .status-offline {
            background-color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h1 class="mb-4">Hệ thống Quản lý Ảnh Chụp Màn Hình</h1>
        
        <?php
        // Hiển thị thông báo nếu có
        if (isset($_GET['deleted'])) {
            $deletedCount = intval($_GET['deleted']);
            $clientId = htmlspecialchars($_GET['client']);
            echo '<div class="alert alert-success">Đã xóa ' . $deletedCount . ' ảnh của client ' . $clientId . '</div>';
        } elseif (isset($_GET['error']) && $_GET['error'] == 'not_found') {
            echo '<div class="alert alert-danger">Không tìm thấy thư mục client</div>';
        } elseif (isset($_GET['client_deleted'])) {
            echo '<div class="alert alert-success">Đã xóa thành công máy: ' . htmlspecialchars($_GET['client_deleted']) . '</div>';
        } elseif (isset($_GET['name_updated'])) {
            echo '<div class="alert alert-success">Đã cập nhật tên máy thành: ' . htmlspecialchars($_GET['new_name']) . '</div>';
        } elseif (isset($_GET['offline_deleted'])) {
            $count = intval($_GET['offline_deleted']);
            echo '<div class="alert alert-success">Đã xóa ' . $count . ' máy offline</div>';
        } elseif (isset($_GET['log_refreshed'])) {
            echo '<div class="alert alert-success">Đã làm mới thông tin log thành công</div>';
        } elseif (isset($_GET['error']) && $_GET['error'] == 'delete_failed') {
            echo '<div class="alert alert-danger">Không thể xóa máy: ' . htmlspecialchars($_GET['client']) . '</div>';
        } elseif (isset($_GET['error']) && $_GET['error'] == 'client_not_found') {
            echo '<div class="alert alert-danger">Không tìm thấy máy: ' . htmlspecialchars($_GET['client']) . '</div>';
        }
        
        $uploadDir = 'uploads/';
        
        if (!file_exists($uploadDir)) {
            echo '<div class="alert alert-warning">Chưa có ảnh nào được upload</div>';
        } else {
            // Đọc các thư mục client
            $clients = array_filter(glob($uploadDir . '*'), 'is_dir');
            $clientCount = count($clients);
            
            // Xác định thời gian hiện tại
            $currentTime = time();
            $onlineThreshold = 600; // 10 phút thay vì 5 phút
            $onlineCount = 0;
            
            if (empty($clients)) {
                echo '<div class="alert alert-info">Chưa có máy nào kết nối</div>';
            } else {
                // Hiển thị số lượng máy đã kết nối
                echo '<div class="alert alert-info mb-4">';
                echo '<h5>Tổng số máy đã kết nối: ' . $clientCount . '</h5>';
                echo '<div id="online-counter">Đang kiểm tra số máy online...</div>';
                echo '<div class="mt-2">';
                echo '<a href="manage_clients.php" class="btn btn-sm btn-primary me-2">Quản lý máy</a>';
                echo '<a href="manage_clients.php?action=delete_offline" class="btn btn-sm btn-danger" onclick="return confirm(\'Bạn có chắc muốn xóa tất cả máy offline?\')">Xóa máy offline</a>';
                echo '</div>';
                echo '</div>';
                
                echo '<div class="row">';
                
                foreach ($clients as $clientPath) {
                    $clientId = basename($clientPath);
                    $clientName = "Unknown";
                    $lastActive = 0;
                    $isOnline = false;
                    
                    // Kiểm tra trực tiếp thời gian sửa đổi của thư mục và file ảnh mới nhất
                    $dirModTime = filemtime($clientPath);
                    
                    // Lấy danh sách ảnh của client
                    $images = array_reverse(glob($clientPath . '/*.{jpg,jpeg,png,gif}', GLOB_BRACE));
                    $latestImage = !empty($images) ? $images[0] : null;
                    
                    if ($latestImage) {
                        $imageModTime = filemtime($latestImage);
                        if ($imageModTime > $lastActive) {
                            $lastActive = $imageModTime;
                        }
                    }
                    
                    // Đọc log để lấy tên client và thời gian hoạt động
                    if (file_exists('screenshots.log')) {
                        $logContent = file('screenshots.log', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
                        // Duyệt từ mục mới nhất đến cũ nhất để tìm tên client
                        $logContent = array_reverse($logContent);
                        foreach ($logContent as $line) {
                            $entry = json_decode($line, true);
                            if ($entry && isset($entry['client_id']) && $entry['client_id'] === $clientId) {
                                // Chỉ gán tên client nếu nó có giá trị hợp lệ
                                if (isset($entry['client_name']) && !empty($entry['client_name']) && $entry['client_name'] !== "Unknown") {
                                    $clientName = $entry['client_name'];
                                    // Đã tìm thấy tên client, dừng vòng lặp
                                    break;
                                }
                                
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
                    
                    // Debug: Ghi ra thông tin về quá trình tìm tên client
                    error_log("Client ID: $clientId, Name found: $clientName");
                    
                    // Kiểm tra xem client có online không (hoạt động trong thời gian quy định)
                    if ($currentTime - $lastActive < $onlineThreshold) {
                        $isOnline = true;
                        $onlineCount++;
                    }
                    
                    $imageCount = count($images);
                    
                    echo '<div class="col-md-4 client-card">';
                    echo '<div class="card position-relative">';
                    
                    // Hiển thị trạng thái online/offline
                    if ($isOnline) {
                        echo '<div class="client-status status-online" title="Online"></div>';
                    } else {
                        echo '<div class="client-status status-offline" title="Offline"></div>';
                    }
                    
                    echo '<div class="card-header d-flex justify-content-between align-items-center">';
                    echo '<div>';
                    echo '<h5>' . htmlspecialchars($clientName) . '</h5>';
                    echo '<small class="text-muted">ID: ' . htmlspecialchars($clientId) . '</small>';
                    echo '</div>';
                    echo '</div>';
                    
                    if ($latestImage) {
                        echo '<img src="' . $latestImage . '" class="card-img-top screenshot-img" data-bs-toggle="modal" data-bs-target="#imageModal" data-img="' . $latestImage . '">';
                        $timestamp = filemtime($latestImage);
                        $timeStr = date('d/m/Y H:i:s', $timestamp);
                        
                        echo '<div class="card-body">';
                        echo '<p>Ảnh mới nhất: ' . $timeStr . '</p>';
                        echo '<p>' . $imageCount . ' ảnh đã chụp</p>';
                        echo '<div class="d-flex justify-content-between">';
                        echo '<a href="client_images.php?id=' . urlencode($clientId) . '" class="btn btn-primary">Xem tất cả ảnh</a>';
                        echo '<a href="delete_all_images.php?client_id=' . urlencode($clientId) . '" class="btn btn-danger" onclick="return confirm(\'Bạn có chắc muốn xóa TẤT CẢ ảnh của user này?\')">Xóa tất cả ảnh</a>';
                        echo '</div>';
                        echo '</div>';
                    } else {
                        echo '<div class="card-body">';
                        echo '<p class="text-center">Chưa có ảnh nào</p>';
                        echo '</div>';
                    }
                    
                    // Hiển thị thông tin debug ở footer của mỗi card:
                    echo '<div class="card-footer text-muted small">';
                    echo 'Hoạt động lần cuối: ' . date('d/m/Y H:i:s', $lastActive) . '<br>';
                    echo 'Thời gian hiện tại: ' . date('d/m/Y H:i:s', $currentTime) . '<br>';
                    echo 'Chênh lệch: ' . ($currentTime - $lastActive) . ' giây';
                    echo '</div>';
                    
                    echo '</div>'; // Đóng card
                    echo '</div>'; // Đóng col
                }
                
                echo '</div>'; // Đóng row
                
                // Cập nhật số máy online
                echo '<script>document.getElementById("online-counter").innerHTML = "Số máy đang online: ' . $onlineCount . '";</script>';
            }
        }
        ?>
    </div>
    
    <!-- Modal xem ảnh -->
    <div class="modal fade" id="imageModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Ảnh Chụp Màn Hình</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center">
                    <img src="" class="modal-img" id="modalImage">
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Script để hiển thị ảnh trong modal
        document.addEventListener('DOMContentLoaded', function() {
            const imageModal = document.getElementById('imageModal');
            if (imageModal) {
                imageModal.addEventListener('show.bs.modal', function(event) {
                    const button = event.relatedTarget;
                    const imgSrc = button.getAttribute('data-img');
                    const modalImage = document.getElementById('modalImage');
                    modalImage.src = imgSrc;
                });
            }
        });
    </script>
</body>
</html> 