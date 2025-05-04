<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ảnh Chụp Màn Hình từ Client</title>
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
    </style>
</head>
<body>
    <div class="container mt-4">
        <?php
        // Đặt múi giờ Việt Nam (+7)
        date_default_timezone_set('Asia/Ho_Chi_Minh');
        
        if (!isset($_GET['id'])) {
            echo '<div class="alert alert-danger">Không tìm thấy ID client</div>';
            echo '<a href="index.php" class="btn btn-primary">Quay lại</a>';
            exit;
        }
        
        $clientId = $_GET['id'];
        $uploadDir = 'uploads/' . $clientId . '/';
        
        if (!file_exists($uploadDir) || !is_dir($uploadDir)) {
            echo '<div class="alert alert-danger">Không tìm thấy thư mục client</div>';
            echo '<a href="index.php" class="btn btn-primary">Quay lại</a>';
            exit;
        }
        
        // Lấy tên client từ log
        $clientName = "Unknown";
        if (file_exists('screenshots.log')) {
            $logContent = file('screenshots.log', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            foreach ($logContent as $line) {
                $entry = json_decode($line, true);
                if ($entry && isset($entry['client_id']) && $entry['client_id'] === $clientId && !empty($entry['client_name'])) {
                    $clientName = $entry['client_name'];
                    break;
                }
            }
        }
        
        echo '<h1>Ảnh từ máy: ' . htmlspecialchars($clientName) . '</h1>';
        echo '<p class="text-muted">ID: ' . htmlspecialchars($clientId) . '</p>';
        echo '<a href="index.php" class="btn btn-primary mb-4">Quay lại trang chính</a>';
        
        // Lấy danh sách ảnh
        $images = array_reverse(glob($uploadDir . '/*.{jpg,jpeg,png,gif}', GLOB_BRACE));
        
        if (empty($images)) {
            echo '<div class="alert alert-info">Chưa có ảnh nào từ client này</div>';
        } else {
            echo '<div class="row">';
            
            foreach ($images as $image) {
                $timestamp = filemtime($image);
                $timeStr = date('d/m/Y H:i:s', $timestamp);
                $fileName = basename($image);
                
                echo '<div class="col-md-6 mb-4">';
                echo '<div class="card">';
                echo '<img src="' . $image . '" class="card-img-top screenshot-img" data-bs-toggle="modal" data-bs-target="#imageModal" data-img="' . $image . '">';
                echo '<div class="card-body">';
                echo '<h5 class="card-title">' . $timeStr . '</h5>';
                echo '<p class="card-text">Filename: ' . htmlspecialchars($fileName) . '</p>';
                echo '<a href="' . $image . '" class="btn btn-sm btn-primary" download>Tải xuống</a> ';
                echo '<a href="delete_image.php?file=' . urlencode($image) . '&client=' . urlencode($clientId) . '" class="btn btn-sm btn-danger" onclick="return confirm(\'Bạn có chắc muốn xóa ảnh này?\')">Xóa</a>';
                echo '</div>';
                echo '</div>';
                echo '</div>';
            }
            
            echo '</div>';
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