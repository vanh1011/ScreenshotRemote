"""
CapScreen Server - Flask Application
Nhận và hiển thị ảnh từ clients
"""

from flask import Flask, request, jsonify, render_template_string, send_from_directory, redirect, url_for
import os
import json
from datetime import datetime
import webbrowser
import threading

import shutil

app = Flask(__name__)

# Cấu hình
UPLOAD_FOLDER = 'uploads'
PORT = 8080

# Tạo thư mục uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kira Magic Dashboard</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>✨</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4F46E5;
            --primary-dark: #4338CA;
            --bg: #F3F4F6;
            --card-bg: #FFFFFF;
            --text-main: #111827;
            --text-secondary: #6B7280;
            --success: #10B981;
            --danger: #EF4444;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Helper Classes */
        .flex { display: flex; }
        .items-center { align-items: center; }
        .justify-between { justify-content: space-between; }
        .gap-2 { gap: 0.5rem; }
        .gap-4 { gap: 1rem; }

        /* Header */
        .dashboard-header {
            margin-bottom: 2rem;
        }

        .brand {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
        }

        /* Clients Grid */
        .clients-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }

        .client-card {
            background: var(--card-bg);
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
        }

        .client-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        .client-header {
            padding: 1.5rem 1.5rem 1rem 1.5rem;
            border-bottom: 1px solid #E5E7EB;
        }

        .client-name-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.25rem;
        }

        .client-name {
            font-weight: 600;
            font-size: 1.125rem;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
        }

        .client-id {
            font-size: 0.75rem;
            background: #EFF6FF;
            color: var(--primary);
            padding: 2px 8px;
            border-radius: 12px;
            font-family: monospace;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-top: 0.5rem;
        }

        .status-badge.online {
            background-color: #D1FAE5;
            color: #065F46;
        }

        .status-badge.offline {
            background-color: #FEE2E2;
            color: #991B1B;
        }

        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            margin-right: 6px;
            background-color: currentColor;
        }

        .client-preview {
            width: 100%;
            height: 200px;
            object-fit: cover;
            cursor: pointer;
            background-color: #f3f4f6;
            display: block; /* Remove space below inline-block */
        }

        .no-image {
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #F9FAFB;
            color: var(--text-secondary);
            font-size: 0.875rem;
        }

        .client-footer {
            padding: 1rem 1.25rem;
            background-color: #F9FAFB;
            border-top: 1px solid #E5E7EB;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.875rem;
        }

        .last-seen {
            color: var(--text-secondary);
            font-size: 0.75rem;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 500;
            font-size: 0.875rem;
            cursor: pointer;
            transition: background-color 0.2s;
            text-decoration: none;
            border: none;
        }

        .btn-primary {
            background-color: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background-color: var(--primary-dark);
        }
        
        .btn-sm {
            padding: 0.25rem 0.75rem;
            font-size: 0.75rem;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            z-index: 50;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(4px);
        }

        .modal.active { display: flex; }

        .modal img {
            max-width: 95%;
            max-height: 95%;
            border-radius: 0.5rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        /* Refresh Button */
        .refresh-btn {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background-color: var(--primary);
            color: white;
            width: 3.5rem;
            height: 3.5rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: none;
            cursor: pointer;
            transition: transform 0.2s;
            font-size: 1.5rem;
        }

        .refresh-btn:hover {
            transform: scale(1.1);
            background-color: var(--primary-dark);
        }

    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="dashboard-header flex justify-between items-center">
            <div class="brand">
                <span>📸</span> CapScreen Check
            </div>
            <div style="color: var(--text-secondary); font-size: 0.875rem;">
                Last update: <span id="update-time">Just now</span>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-value">{{ total_clients }}</span>
                <span class="stat-label">Tổng Thiết Bị</span>
            </div>
            <div class="stat-card">
                <span class="stat-value" style="color: var(--success)">{{ online_clients }}</span>
                <span class="stat-label">Đang Online</span>
            </div>
            <div class="stat-card">
                <span class="stat-value" style="color: var(--primary)">{{ total_screenshots }}</span>
                <span class="stat-label">Ảnh Đã Chụp</span>
            </div>
        </div>

        <!-- Grid Starts -->
        <div class="clients-grid">
            {% for client in clients %}
            <div class="client-card">
                <div class="client-header">
                    <div class="client-name-row">
                        <div class="client-name" title="{{ client.name }}">{{ client.name }}</div>
                        <div class="client-id">#{{ client.short_id }}</div>
                    </div>
                    <div class="status-badge {{ 'online' if client.online else 'offline' }}">
                        <span class="status-dot"></span>
                        {{ 'Hoạt động' if client.online else 'Không hoạt động' }}
                    </div>
                </div>

                {% if client.latest_image %}
                    <img src="/uploads/{{ client.id }}/{{ client.latest_image }}" 
                         class="client-preview" 
                         onclick="showModal(this.src)"
                         loading="lazy">
                {% else %}
                    <div class="no-image">
                        Chưa có ảnh nào
                    </div>
                {% endif %}

                <div class="client-footer">
                    <div class="last-seen">
                        🕒 {{ client.last_seen }}
                    </div>
                    <a href="/client/{{ client.id }}" class="btn btn-primary btn-sm">
                        Chi tiết →
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Pagination -->
        {% if total_pages > 1 %}
        <div style="margin-top: 2rem; display: flex; justify-content: center; align-items: center; gap: 1rem;">
            {% if page > 1 %}
                <a href="?page={{ page - 1 }}" class="btn btn-secondary" style="text-decoration: none;">‹ Trang trước</a>
            {% else %}
                <button class="btn btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed;">‹ Trang trước</button>
            {% endif %}
            
            <div style="display: flex; gap: 0.5rem; align-items: center;">
                {% for p in range(1, total_pages + 1) %}
                    {% if p == page %}
                        <span style="padding: 0.5rem 0.75rem; background: var(--primary); color: white; border-radius: 0.375rem; font-weight: 600;">{{ p }}</span>
                    {% elif (p <= 3) or (p >= total_pages - 2) or (p >= page - 1 and p <= page + 1) %}
                        <a href="?page={{ p }}" style="padding: 0.5rem 0.75rem; background: var(--card-bg); border-radius: 0.375rem; text-decoration: none; color: var(--text-main); transition: all 0.2s;">{{ p }}</a>
                    {% elif p == 4 or p == total_pages - 3 %}
                        <span style="padding: 0.5rem;">...</span>
                    {% endif %}
                {% endfor %}
            </div>
            
            {% if page < total_pages %}
                <a href="?page={{ page + 1 }}" class="btn btn-secondary" style="text-decoration: none;">Trang sau ›</a>
            {% else %}
                <button class="btn btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed;">Trang sau ›</button>
            {% endif %}
        </div>
        <div style="text-align: center; margin-top: 1rem; color: var(--text-secondary); font-size: 0.875rem;">
            Trang {{ page }} / {{ total_pages }} • Hiển thị {{ clients|length }} / {{ total_clients }} thiết bị
        </div>
        {% endif %}
    </div>

    <!-- Refresh Button -->
    <button class="refresh-btn" onclick="location.reload()" title="Refresh Dashboard">
        ↻
    </button>

    <!-- Modal for Image Preview -->
    <div class="modal" id="modal" onclick="this.classList.remove('active')">
        <img id="modal-img" src="">
    </div>

    <script>
        // Update Time Helper
        document.getElementById('update-time').innerText = new Date().toLocaleTimeString();

        // Image Modal
        function showModal(src) {
            document.getElementById('modal-img').src = src;
            document.getElementById('modal').classList.add('active');
        }

        // Auto Refresh (30s)
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Dashboard chính"""
    clients = []
    total_screenshots = 0
    online_count = 0
    
    # Đọc thông tin từ thư mục uploads
    if os.path.exists(UPLOAD_FOLDER):
        for client_id in os.listdir(UPLOAD_FOLDER):
            client_path = os.path.join(UPLOAD_FOLDER, client_id)
            if os.path.isdir(client_path):
                try:
                    images = sorted([f for f in os.listdir(client_path) if f.endswith('.png')])
                    
                    if images:
                        # Old structure: images directly in client folder
                        total_screenshots += len(images)
                        latest_image = images[-1]
                        image_path = os.path.join(client_path, latest_image)
                        last_modified = os.path.getmtime(image_path)
                        last_seen = datetime.fromtimestamp(last_modified)
                        
                        # Đọc client_name từ file
                        name_file = os.path.join(client_path, 'client_name.txt')
                        if os.path.exists(name_file):
                            with open(name_file, 'r') as f:
                                client_name = f.read().strip()
                        else:
                            client_name = client_id
                        
                        # Online nếu hoạt động trong 10 phút
                        is_online = (datetime.now() - last_seen).seconds < 600
                        if is_online:
                            online_count += 1
                        
                        clients.append({
                            'id': client_id,
                            'name': client_name,
                            'short_id': client_id[-5:] if len(client_id) > 5 else client_id,
                            'latest_image': latest_image,
                            'last_seen': last_seen.strftime('%H:%M:%S - %d/%m/%Y'),
                            'online': is_online,
                            'image_count': len(images)
                        })
                    else:
                         # New structure: images in date folders (uploads/client_id/YYYY-MM-DD/img.png)
                         all_items = os.listdir(client_path)
                         dates = []
                         for item in all_items:
                             item_path = os.path.join(client_path, item)
                             if os.path.isdir(item_path):
                                 # Validate if it's a date folder (YYYY-MM-DD)
                                 try:
                                     datetime.strptime(item, '%Y-%m-%d')
                                     dates.append(item)
                                 except:
                                     pass  # Skip non-date folders
                         
                         dates.sort(reverse=True)  # Newest first
                         
                         total_images_client = 0
                         last_seen = datetime.min
                         latest_image_rel = None
                         
                         for d in dates:
                             d_path = os.path.join(client_path, d)
                             try:
                                 imgs = [f for f in os.listdir(d_path) if f.endswith('.png')]
                                 total_images_client += len(imgs)
                                 
                                 if imgs and last_seen == datetime.min:
                                     # Found latest date with images
                                     # Sort imgs to find latest
                                     imgs.sort(reverse=True) # timestamp filename
                                     latest_img = imgs[0]
                                     latest_image_rel = f"{d}/{latest_img}"
                                     
                                     img_path = os.path.join(d_path, latest_img)
                                     ts = os.path.getmtime(img_path)
                                     last_seen = datetime.fromtimestamp(ts)
                             except Exception as e:
                                 print(f"Error reading date folder {d}: {e}")
                                 continue
                         
                         if latest_image_rel:
                            total_screenshots += total_images_client
                            
                            # Đọc client_name
                            name_file = os.path.join(client_path, 'client_name.txt')
                            if os.path.exists(name_file):
                                with open(name_file, 'r') as f:
                                    client_name = f.read().strip()
                            else:
                                client_name = client_id

                            is_online = (datetime.now() - last_seen).seconds < 600
                            if is_online:
                                online_count += 1
                                
                            clients.append({
                                'id': client_id,
                                'name': client_name,
                                'short_id': client_id[-5:] if len(client_id) > 5 else client_id,
                                'latest_image': latest_image_rel, # Format: YYYY-MM-DD/filename.png
                                'last_seen': last_seen.strftime('%H:%M:%S - %d/%m/%Y'),
                                'online': is_online,
                                'image_count': total_images_client
                            })
                except OSError as e:
                    # Xử lý lỗi thư mục bị corrupt (bad sector, NTFS error, etc.)
                    print(f"⚠️  WARNING: Cannot read client folder '{client_id}': {e}")
                    print(f"   Thư mục có thể bị hỏng. Hãy chạy CHKDSK hoặc xóa thư mục này.")
                    continue  # Bỏ qua client này và tiếp tục
                except Exception as e:
                    # Bắt các lỗi khác không mong đợi
                    print(f"❌ ERROR processing client '{client_id}': {e}")
                    continue
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 16  # 4x4 grid
    total_pages = (len(clients) + per_page - 1) // per_page if clients else 1
    page = max(1, min(page, total_pages))  # Clamp page number
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_clients = clients[start:end]
    
    return render_template_string(
        HTML_TEMPLATE,
        clients=paginated_clients,
        page=page,
        total_pages=total_pages,
        total_clients=len(clients),
        online_clients=online_count,
        total_screenshots=total_screenshots
    )

def migrate_files(client_id):
    """Di chuyển các file cũ chưa vào folder ngày"""
    client_path = os.path.join(UPLOAD_FOLDER, client_id)
    if not os.path.exists(client_path):
        return

    try:
        filenames = os.listdir(client_path)
    except OSError as e:
        print(f"⚠️  WARNING: Cannot read client folder '{client_id}' for migration: {e}")
        return
    
    for filename in filenames:
        filepath = os.path.join(client_path, filename)
        
        # Chỉ xử lý file ảnh nằm trực tiếp
        if os.path.isfile(filepath) and filename.endswith('.png'):
            try:
                # Parse ngày từ tên file (YYYYMMDD_HHMMSS.png)
                # Hoặc lấy từ file modified time nếu tên ko chuẩn
                if '_' in filename:
                    date_part = filename.split('_')[0] # 20231027
                    if len(date_part) == 8:
                        date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
                    else:
                        continue
                else:
                    # Fallback thời gian tạo file
                    ts = os.path.getmtime(filepath)
                    date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                
                # Tạo folder ngày
                date_folder = os.path.join(client_path, date_str)
                os.makedirs(date_folder, exist_ok=True)
                
                # Move file
                shutil.move(filepath, os.path.join(date_folder, filename))
            except Exception as e:
                print(f"Error migrating {filename}: {e}")

@app.route('/api/upload', methods=['POST'])
def upload():
    """API nhận ảnh từ client"""
    try:
        # Lấy thông tin
        client_id = request.form.get('client_id')
        client_name = request.form.get('client_name', client_id)
        screenshot = request.files.get('screenshot')
        
        if not client_id or not screenshot:
            return jsonify({'success': False, 'message': 'Missing data'}), 400
        
        # Tạo folder cho client
        client_folder = os.path.join(UPLOAD_FOLDER, client_id)
        os.makedirs(client_folder, exist_ok=True)
        
        # Lưu client_name vào file
        name_file = os.path.join(client_folder, 'client_name.txt')
        with open(name_file, 'w') as f:
            f.write(client_name)
        
        # Xác định ngày hiện tại (Server time + offset nếu cần, nhưng user bảo:
        # "tôi ở Việt Nam sẽ query múi Giờ +7 nên phải trừ 7h so với mongo DB"
        # Ở đây là file system local, server chạy trên máy user (hoặc PC user) nên dùng local time là chuẩn nhất.
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        
        # Tạo folder ngày
        date_folder = os.path.join(client_folder, date_str)
        os.makedirs(date_folder, exist_ok=True)
        
        # Lưu ảnh
        filename = f'{timestamp}.png'
        filepath = os.path.join(date_folder, filename)
        screenshot.save(filepath)
        
        return jsonify({
            'success': True,
            'message': 'Upload successful',
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/client/<client_id>')
def client_detail(client_id):
    """Trang xem tất cả ảnh của 1 client"""
    client_path = os.path.join(UPLOAD_FOLDER, client_id)
    
    if not os.path.exists(client_path):
        return "Client not found", 404
    
    # Chạy migration cho các file cũ
    migrate_files(client_id)

    # Đọc client_name
    name_file = os.path.join(client_path, 'client_name.txt')
    if os.path.exists(name_file):
        with open(name_file, 'r') as f:
            client_name = f.read().strip()
    else:
        client_name = client_id[:5] if len(client_id) > 5 else client_id
    
    short_id = client_id[-5:] if len(client_id) > 5 else client_id
    
    # Lấy danh sách ngày (folder con)
    dates = []
    try:
        items = os.listdir(client_path)
    except OSError as e:
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Error</title></head>
<body style="font-family: Arial; padding: 2rem; text-align: center;">
<h1>⚠️ Lỗi đọc thư mục</h1>
<p>Không thể đọc thư mục client <code>{client_id}</code></p>
<p style="color: #666;">Thư mục có thể bị hỏng. Hãy chạy CHKDSK (Windows) hoặc xóa thư mục này.</p>
<p style="color: #999; font-size: 0.875rem;">Chi tiết: {e}</p>
<a href="/" style="display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: #4F46E5; color: white; text-decoration: none; border-radius: 0.5rem;">← Quay lại Dashboard</a>
</body></html>""", 500
    
    for item in items:
        path = os.path.join(client_path, item)
        if os.path.isdir(path):
            try:
                datetime.strptime(item, '%Y-%m-%d')
                dates.append(item)
            except:
                pass
    
    dates.sort(reverse=True)
    
    # Xác định ngày đang chọn
    selected_date = request.args.get('date')
    if not selected_date and dates:
        selected_date = dates[0]
    
    processed_images = []
    if selected_date:
        date_folder = os.path.join(client_path, selected_date)
        if os.path.exists(date_folder):
            try:
                filenames = sorted([f for f in os.listdir(date_folder) if f.endswith('.png')], reverse=True)
            except OSError as e:
                print(f"⚠️  WARNING: Cannot read date folder '{selected_date}': {e}")
                filenames = []
             for fname in filenames:
                 try:
                     # YYYYMMDD_HHMMSS.png -> HH:MM:SS
                     time_part = fname.split('_')[1].replace('.png', '')
                     time_display = f"{time_part[0:2]}:{time_part[2:4]}:{time_part[4:6]}"
                 except:
                     time_display = fname
                 
                 processed_images.append({
                     'filename': fname,
                     'time_display': time_display
                 })

    # Pagination for gallery
    page = request.args.get('page', 1, type=int)
    per_page = 20
    total_images = len(processed_images)
    total_pages = (total_images + per_page - 1) // per_page if total_images else 1
    page = max(1, min(page, total_pages))  # Clamp page number
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = processed_images[start:end]
    
    DETAIL_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>✨ {{ client_name }} - Kira Magic</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>✨</text></svg>">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
             :root {
                --primary: #4F46E5;
                --primary-dark: #4338CA;
                --bg: #F3F4F6;
                --card-bg: #FFFFFF;
                --text-main: #111827;
                --text-secondary: #6B7280;
                --danger: #EF4444;
                --danger-hover: #DC2626;
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', sans-serif;
                background-color: var(--bg);
                color: var(--text-main);
                min-height: 100vh;
                padding: 2rem;
            }
            .container { max-width: 1400px; margin: 0 auto; }
            
             /* Layout 2 columns */
            .main-content {
                display: grid;
                grid-template-columns: 250px 1fr;
                gap: 2rem;
                align-items: start;
            }
            
            @media (max-width: 768px) {
                .main-content { grid-template-columns: 1fr; }
            }

            /* Sidebar */
            .sidebar {
                background: var(--card-bg);
                padding: 1rem;
                border-radius: 1rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                position: sticky;
                top: 2rem;
                max-height: calc(100vh - 4rem);
                overflow-y: auto;
            }
            .sidebar-title {
                font-weight: 700;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid #E5E7EB;
            }
            
            /* Calendar View */
            .calendar-container {
                padding: 0.75rem;
            }
            .calendar-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }
            .calendar-month {
                font-weight: 600;
                font-size: 0.875rem;
                color: var(--text-main);
            }
            .calendar-nav {
                background: none;
                border: none;
                color: var(--text-secondary);
                font-size: 1.25rem;
                cursor: pointer;
                padding: 0.25rem 0.5rem;
                border-radius: 0.25rem;
                transition: all 0.2s;
            }
            .calendar-nav:hover {
                background: var(--bg);
                color: var(--primary);
            }
            .calendar-weekdays {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 0.25rem;
                margin-bottom: 0.5rem;
            }
            .calendar-weekdays div {
                text-align: center;
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--text-secondary);
                padding: 0.25rem;
            }
            .calendar-days {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 0.25rem;
            }
            .calendar-day {
                aspect-ratio: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.75rem;
                border-radius: 0.375rem;
                color: var(--text-secondary);
                transition: all 0.2s;
            }
            .calendar-day.empty {
                visibility: hidden;
            }
            .calendar-day.has-data {
                background: #EEF2FF;
                color: var(--primary);
                font-weight: 600;
            }
            .calendar-day.has-data:hover {
                background: var(--primary);
                color: white;
                transform: scale(1.1);
            }
            .calendar-day.selected {
                background: var(--primary);
                color: white;
                font-weight: 700;
                box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
            }
            .calendar-day.today {
                border: 2px solid var(--primary);
            }
            .calendar-day.today.selected {
                border-color: white;
            }

            /* Header */
            .detail-header {
                background: var(--card-bg);
                padding: 1.5rem 2rem;
                border-radius: 1rem;
                margin-bottom: 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            .header-info h1 { font-size: 1.5rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.25rem; }
            .header-meta { color: var(--text-secondary); font-size: 0.875rem; }
            .header-actions { display: flex; gap: 1rem; }

            /* Buttons */
            .btn { padding: 0.625rem 1.25rem; border-radius: 0.5rem; font-weight: 500; font-size: 0.875rem; cursor: pointer; text-decoration: none; border: none; transition: all 0.2s; display: inline-flex; align-items: center; gap: 0.5rem; }
            .btn-secondary { background-color: #E5E7EB; color: var(--text-main); }
            .btn-secondary:hover { background-color: #D1D5DB; }
            .btn-danger { background-color: var(--danger); color: white; }
            .btn-danger:hover { background-color: var(--danger-hover); }
            
            .images-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
            .image-card { background: var(--card-bg); border-radius: 0.75rem; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: transform 0.2s; display: flex; flex-direction: column; }
            .image-card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .image-card img { width: 100%; height: 180px; object-fit: cover; cursor: pointer; background-color: #f3f4f6; }
            .image-footer { padding: 0.75rem 1rem; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #E5E7EB; background-color: white; }
            .time-label { font-size: 0.875rem; color: var(--text-secondary); font-family: monospace; }
            .btn-del-sm { padding: 0.375rem 0.75rem; font-size: 0.75rem; color: var(--danger); background-color: #FEF2F2; border-radius: 0.375rem; font-weight: 500; cursor: pointer; border: none; }
            .btn-del-sm:hover { background-color: #FEE2E2; }

            /* Modal - Advanced Image Viewer */
            .image-viewer {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0,0,0,0.98);
                z-index: 10000;
                flex-direction: column;
            }
            .image-viewer.active { display: flex; }
            
            /* Viewer Toolbar */
            .viewer-toolbar {
                background: rgba(0,0,0,0.9);
                padding: 0.75rem 1.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .viewer-info {
                display: flex;
                gap: 1.5rem;
                color: #fff;
                font-size: 0.875rem;
            }
            .viewer-controls {
                display: flex;
                gap: 0.5rem;
            }
            .viewer-btn {
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                color: #fff;
                padding: 0.5rem 0.75rem;
                border-radius: 0.375rem;
                cursor: pointer;
                font-size: 0.875rem;
                transition: all 0.2s;
            }
            .viewer-btn:hover {
                background: rgba(255,255,255,0.2);
            }
            .viewer-btn.active {
                background: var(--primary);
                border-color: var(--primary);
            }
            
            /* Viewer Content */
            .viewer-content {
                flex: 1;
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .image-container {
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: grab;
                user-select: none;
            }
            .image-container.grabbing {
                cursor: grabbing;
            }
            .image-container img {
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
                transition: transform 0.3s ease;
                pointer-events: none;
            }
            
            /* Navigation Buttons */
            .nav-btn {
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(0,0,0,0.7);
                border: 2px solid rgba(255,255,255,0.3);
                color: #fff;
                font-size: 2rem;
                width: 3rem;
                height: 3rem;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
                z-index: 10;
            }
            .nav-btn:hover {
                background: rgba(0,0,0,0.9);
                border-color: #fff;
            }
            .nav-btn.prev { left: 1rem; }
            .nav-btn.next { right: 1rem; }
            .nav-btn:disabled {
                opacity: 0.3;
                cursor: not-allowed;
            }
            
            /* Thumbnail Strip */
            .thumbnail-strip {
                background: rgba(0,0,0,0.9);
                padding: 0.75rem;
                display: flex;
                gap: 0.5rem;
                overflow-x: auto;
                border-top: 1px solid rgba(255,255,255,0.1);
                max-height: 120px;
            }
            .thumbnail-strip::-webkit-scrollbar {
                height: 6px;
            }
            .thumbnail-strip::-webkit-scrollbar-thumb {
                background: rgba(255,255,255,0.3);
                border-radius: 3px;
            }
            .thumbnail-item {
                flex-shrink: 0;
                width: 80px;
                height: 80px;
                cursor: pointer;
                border: 2px solid transparent;
                border-radius: 0.375rem;
                overflow: hidden;
                transition: all 0.2s;
            }
            .thumbnail-item:hover {
                border-color: rgba(255,255,255,0.5);
            }
            .thumbnail-item.active {
                border-color: var(--primary);
                box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
            }
            .thumbnail-item img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="detail-header">
                <div class="header-info">
                    <h1>📸 {{ client_name }}</h1>
                    <div class="header-meta">
                        ID: #{{ short_id }} • Ngày: {{ selected_date or 'N/A' }} • {{ images|length }} ảnh
                    </div>
                </div>
                <div class="header-actions">
                    <a href="/" class="btn btn-secondary">← Quay lại</a>
                    <button onclick="deleteAll()" class="btn btn-danger">🗑️ Xóa ngày này</button>
                    <button onclick="deleteClient()" class="btn btn-danger" style="background-color: #991B1B;">Hủy thiết bị</button>
                </div>
            </div>
            
            <div class="main-content">
                <div class="sidebar">
                    <div class="sidebar-title">📅 Lịch sử</div>
                    
                    <!-- Calendar View -->
                    <div class="calendar-container">
                        <div class="calendar-header">
                            <button class="calendar-nav" onclick="changeMonth(-1)">‹</button>
                            <span class="calendar-month" id="calendarMonth">Tháng 1, 2026</span>
                            <button class="calendar-nav" onclick="changeMonth(1)">›</button>
                        </div>
                        
                        <div class="calendar-weekdays">
                            <div>CN</div>
                            <div>T2</div>
                            <div>T3</div>
                            <div>T4</div>
                            <div>T5</div>
                            <div>T6</div>
                            <div>T7</div>
                        </div>
                        
                        <div class="calendar-days" id="calendarDays">
                            <!-- Days will be generated by JavaScript -->
                        </div>
                    </div>
                    
                    <script>
                        // Available dates from server (YYYY-MM-DD format)
                        const calendarDates = {{ dates | tojson }};
                        const calendarSelectedDate = "{{ selected_date }}";
                        const calendarClientId = "{{ client_id }}";
                        
                        let currentMonth = new Date();
                        if (calendarSelectedDate) {
                            currentMonth = new Date(calendarSelectedDate);
                        }
                        
                        function renderCalendar() {
                            const year = currentMonth.getFullYear();
                            const month = currentMonth.getMonth();
                            
                            // Update header
                            const monthNames = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6',
                                              'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'];
                            document.getElementById('calendarMonth').textContent = `${monthNames[month]}, ${year}`;
                            
                            // Get first day of month and total days
                            const firstDay = new Date(year, month, 1).getDay();
                            const daysInMonth = new Date(year, month + 1, 0).getDate();
                            
                            // Generate calendar days
                            const calendarDays = document.getElementById('calendarDays');
                            calendarDays.innerHTML = '';
                            
                            // Empty cells for days before month starts
                            for (let i = 0; i < firstDay; i++) {
                                const emptyDay = document.createElement('div');
                                emptyDay.className = 'calendar-day empty';
                                calendarDays.appendChild(emptyDay);
                            }
                            
                            // Days of the month
                            for (let day = 1; day <= daysInMonth; day++) {
                                const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                                const hasData = calendarDates.includes(dateStr);
                                const isSelected = dateStr === calendarSelectedDate;
                                const isToday = dateStr === new Date().toISOString().split('T')[0];
                                
                                const dayEl = document.createElement('div');
                                dayEl.className = 'calendar-day';
                                if (hasData) dayEl.classList.add('has-data');
                                if (isSelected) dayEl.classList.add('selected');
                                if (isToday) dayEl.classList.add('today');
                                
                                dayEl.textContent = day;
                                
                                if (hasData) {
                                    dayEl.onclick = () => {
                                        window.location.href = `?date=${dateStr}`;
                                    };
                                    dayEl.style.cursor = 'pointer';
                                }
                                
                                calendarDays.appendChild(dayEl);
                            }
                        }
                        
                        function changeMonth(delta) {
                            currentMonth.setMonth(currentMonth.getMonth() + delta);
                            renderCalendar();
                        }
                        
                        // Initial render
                        renderCalendar();
                    </script>
                </div>

                <div class="gallery-section">
                     {% if not images %}
                        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                            Không có ảnh nào trong ngày {{ selected_date }}
                        </div>
                     {% else %}
                        <div class="images-grid">
                            {% for img in images %}
                            <div class="image-card">
                                <img src="/uploads/{{ client_id }}/{{ selected_date }}/{{ img.filename }}" 
                                     onclick="openViewer({{ (page - 1) * 20 + loop.index0 }})" 
                                     loading="lazy">
                                <div class="image-footer">
                                    <span class="time-label">{{ img.time_display }}</span>
                                    <button onclick="deleteImage('{{ client_id }}', '{{ selected_date }}', '{{ img.filename }}')" class="btn btn-del-sm">Xóa</button>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                        
                        <!-- Pagination -->
                        {% if total_pages > 1 %}
                        <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #E5E7EB; display: flex; justify-content: center; align-items: center; gap: 1rem;">
                            {% if page > 1 %}
                                <a href="?date={{ selected_date }}&page={{ page - 1 }}" class="btn btn-secondary" style="text-decoration: none;">‹ Trang trước</a>
                            {% else %}
                                <button class="btn btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed;">‹ Trang trước</button>
                            {% endif %}
                            
                            <div style="display: flex; gap: 0.5rem; align-items: center;">
                                {% for p in range(1, total_pages + 1) %}
                                    {% if p == page %}
                                        <span style="padding: 0.5rem 0.75rem; background: var(--primary); color: white; border-radius: 0.375rem; font-weight: 600;">{{ p }}</span>
                                    {% elif (p <= 3) or (p >= total_pages - 2) or (p >= page - 1 and p <= page + 1) %}
                                        <a href="?date={{ selected_date }}&page={{ p }}" style="padding: 0.5rem 0.75rem; background: var(--card-bg); border: 1px solid #E5E7EB; border-radius: 0.375rem; text-decoration: none; color: var(--text-main); transition: all 0.2s;">{{ p }}</a>
                                    {% elif p == 4 or p == total_pages - 3 %}
                                        <span style="padding: 0.5rem;">...</span>
                                    {% endif %}
                                {% endfor %}
                            </div>
                            
                            {% if page < total_pages %}
                                <a href="?date={{ selected_date }}&page={{ page + 1 }}" class="btn btn-secondary" style="text-decoration: none;">Trang sau ›</a>
                            {% else %}
                                <button class="btn btn-secondary" disabled style="opacity: 0.5; cursor: not-allowed;">Trang sau ›</button>
                            {% endif %}
                        </div>
                        <div style="text-align: center; margin-top: 1rem; color: var(--text-secondary); font-size: 0.875rem;">
                            Trang {{ page }} / {{ total_pages }} • Hiển thị {{ images|length }} / {{ total_images }} ảnh
                        </div>
                        {% endif %}
                     {% endif %}
                </div>
            </div>
        </div>
        
        <!-- Advanced Image Viewer -->
        <div class="image-viewer" id="imageViewer">
            <div class="viewer-toolbar">
                <div class="viewer-info">
                    <span id="imagePosition">-/-</span>
                    <span id="imageTime">--:--:--</span>
                    <span id="zoomLevel">100%</span>
                </div>
                <div class="viewer-controls">
                    <button class="viewer-btn" onclick="viewer.rotate(-90)" title="Rotate Left (Shift+R)">↶</button>
                    <button class="viewer-btn" onclick="viewer.rotate(90)" title="Rotate Right (R)">↷</button>
                    <button class="viewer-btn" onclick="viewer.zoomOut()" title="Zoom Out (-)">−</button>
                    <button class="viewer-btn" onclick="viewer.resetZoom()" title="Reset (0)">⊡</button>
                    <button class="viewer-btn" onclick="viewer.zoomIn()" title="Zoom In (+)">+</button>
                    <button class="viewer-btn" id="slideshowBtn" onclick="viewer.toggleSlideshow()" title="Slideshow (Space)">▶</button>
                    <button class="viewer-btn" onclick="viewer.download()" title="Download (D)">⬇</button>
                    <button class="viewer-btn" onclick="viewer.close()" title="Close (Esc)">✕</button>
                </div>
            </div>
            
            <div class="viewer-content">
                <button class="nav-btn prev" id="prevBtn" onclick="viewer.prev()">‹</button>
                <div class="image-container" id="imageContainer">
                    <img id="viewerImage" src="" alt="">
                </div>
                <button class="nav-btn next" id="nextBtn" onclick="viewer.next()">›</button>
            </div>
            
            <div class="thumbnail-strip" id="thumbnailStrip"></div>
        </div>
        
        <script>
            // Image data from server
            const allImages = {{ all_images | tojson }};  // All images for viewer navigation
            const clientId = "{{ client_id }}";
            const selectedDate = "{{ selected_date }}";
            
            // Image Viewer Class
            class ImageViewer {
                constructor() {
                    this.currentIndex = 0;
                    this.images = allImages;
                    this.zoom = 1;
                    this.rotation = 0;
                    this.panX = 0;
                    this.panY = 0;
                    this.isDragging = false;
                    this.dragStartX = 0;
                    this.dragStartY = 0;
                    this.slideshowTimer = null;
                    this.slideshowInterval = 3000;
                    
                    this.initElements();
                    this.initEvents();
                }
                
                initElements() {
                    this.viewer = document.getElementById('imageViewer');
                    this.image = document.getElementById('viewerImage');
                    this.container = document.getElementById('imageContainer');
                    this.prevBtn = document.getElementById('prevBtn');
                    this.nextBtn = document.getElementById('nextBtn');
                    this.thumbnailStrip = document.getElementById('thumbnailStrip');
                    this.slideshowBtn = document.getElementById('slideshowBtn');
                }
                
                initEvents() {
                    // Pan/drag events
                    this.container.addEventListener('mousedown', (e) => this.startDrag(e));
                    this.container.addEventListener('mousemove', (e) => this.drag(e));
                    this.container.addEventListener('mouseup', () => this.endDrag());
                    this.container.addEventListener('mouseleave', () => this.endDrag());
                    
                    // Keyboard shortcuts
                    document.addEventListener('keydown', (e) => this.handleKeyboard(e));
                    
                    // Prevent context menu on image
                    this.image.addEventListener('contextmenu', (e) => e.preventDefault());
                }
                
                open(index) {
                    this.currentIndex = index;
                    this.viewer.classList.add('active');
                    this.loadImage();
                    this.buildThumbnails();
                    this.resetTransform();
                }
                
                close() {
                    this.viewer.classList.remove('active');
                    this.stopSlideshow();
                }
                
                loadImage() {
                    if (this.images.length === 0) return;
                    
                    const img = this.images[this.currentIndex];
                    const imgUrl = `/uploads/${clientId}/${selectedDate}/${img.filename}`;
                    this.image.src = imgUrl;
                    
                    // Update UI
                    document.getElementById('imagePosition').textContent = 
                        `${this.currentIndex + 1}/${this.images.length}`;
                    document.getElementById('imageTime').textContent = img.time_display;
                    
                    // Update navigation buttons
                    this.prevBtn.disabled = this.currentIndex === 0;
                    this.nextBtn.disabled = this.currentIndex === this.images.length - 1;
                    
                    // Update thumbnail active state
                    document.querySelectorAll('.thumbnail-item').forEach((thumb, idx) => {
                        thumb.classList.toggle('active', idx === this.currentIndex);
                    });
                    
                    // Scroll thumbnail into view
                    const activeThumb = this.thumbnailStrip.children[this.currentIndex];
                    if (activeThumb) {
                        activeThumb.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                    }
                }
                
                buildThumbnails() {
                    this.thumbnailStrip.innerHTML = '';
                    this.images.forEach((img, idx) => {
                        const thumb = document.createElement('div');
                        thumb.className = 'thumbnail-item';
                        if (idx === this.currentIndex) thumb.classList.add('active');
                        
                        const thumbImg = document.createElement('img');
                        thumbImg.src = `/uploads/${clientId}/${selectedDate}/${img.filename}`;
                        thumbImg.loading = 'lazy';
                        
                        thumb.appendChild(thumbImg);
                        thumb.onclick = () => {
                            this.currentIndex = idx;
                            this.loadImage();
                            this.resetTransform();
                        };
                        
                        this.thumbnailStrip.appendChild(thumb);
                    });
                }
                
                next() {
                    if (this.currentIndex < this.images.length - 1) {
                        this.currentIndex++;
                        this.loadImage();
                        this.resetTransform();
                    }
                }
                
                prev() {
                    if (this.currentIndex > 0) {
                        this.currentIndex--;
                        this.loadImage();
                        this.resetTransform();
                    }
                }
                
                zoomIn() {
                    this.zoom = Math.min(this.zoom + 0.25, 4);
                    this.updateTransform();
                }
                
                zoomOut() {
                    this.zoom = Math.max(this.zoom - 0.25, 0.25);
                    this.updateTransform();
                }
                
                resetZoom() {
                    this.zoom = 1;
                    this.panX = 0;
                    this.panY = 0;
                    this.updateTransform();
                }
                
                rotate(degrees) {
                    this.rotation = (this.rotation + degrees) % 360;
                    this.updateTransform();
                }
                
                resetTransform() {
                    this.zoom = 1;
                    this.rotation = 0;
                    this.panX = 0;
                    this.panY = 0;
                    this.updateTransform();
                }
                
                updateTransform() {
                    const transform = `
                        translate(${this.panX}px, ${this.panY}px)
                        scale(${this.zoom})
                        rotate(${this.rotation}deg)
                    `;
                    this.image.style.transform = transform;
                    document.getElementById('zoomLevel').textContent = `${Math.round(this.zoom * 100)}%`;
                }
                
                startDrag(e) {
                    if (this.zoom <= 1) return;
                    this.isDragging = true;
                    this.dragStartX = e.clientX - this.panX;
                    this.dragStartY = e.clientY - this.panY;
                    this.container.classList.add('grabbing');
                }
                
                drag(e) {
                    if (!this.isDragging) return;
                    this.panX = e.clientX - this.dragStartX;
                    this.panY = e.clientY - this.dragStartY;
                    this.updateTransform();
                }
                
                endDrag() {
                    this.isDragging = false;
                    this.container.classList.remove('grabbing');
                }
                
                toggleSlideshow() {
                    if (this.slideshowTimer) {
                        this.stopSlideshow();
                    } else {
                        this.startSlideshow();
                    }
                }
                
                startSlideshow() {
                    this.slideshowTimer = setInterval(() => {
                        if (this.currentIndex < this.images.length - 1) {
                            this.next();
                        } else {
                            this.stopSlideshow();
                        }
                    }, this.slideshowInterval);
                    this.slideshowBtn.classList.add('active');
                    this.slideshowBtn.textContent = '⏸';
                }
                
                stopSlideshow() {
                    if (this.slideshowTimer) {
                        clearInterval(this.slideshowTimer);
                        this.slideshowTimer = null;
                    }
                    this.slideshowBtn.classList.remove('active');
                    this.slideshowBtn.textContent = '▶';
                }
                
                download() {
                    const img = this.images[this.currentIndex];
                    const a = document.createElement('a');
                    a.href = `/uploads/${clientId}/${selectedDate}/${img.filename}`;
                    a.download = img.filename;
                    a.click();
                }
                
                handleKeyboard(e) {
                    if (!this.viewer.classList.contains('active')) return;
                    
                    switch(e.key) {
                        case 'ArrowLeft':
                            this.prev();
                            break;
                        case 'ArrowRight':
                            this.next();
                            break;
                        case '+':
                        case '=':
                            this.zoomIn();
                            break;
                        case '-':
                        case '_':
                            this.zoomOut();
                            break;
                        case '0':
                            this.resetZoom();
                            break;
                        case 'r':
                            this.rotate(e.shiftKey ? -90 : 90);
                            break;
                        case ' ':
                            e.preventDefault();
                            this.toggleSlideshow();
                            break;
                        case 'Escape':
                            this.close();
                            break;
                        case 'd':
                        case 'D':
                            this.download();
                            break;
                        case 'f':
                        case 'F':
                            if (document.fullscreenElement) {
                                document.exitFullscreen();
                            } else {
                                this.viewer.requestFullscreen();
                            }
                            break;
                    }
                }
            }
            
            // Initialize viewer
            const viewer = new ImageViewer();
            
            // Global function to open viewer
            function openViewer(index) {
                viewer.open(index);
            }
            
            function deleteImage(clientId, date, filename) {
                if (confirm('Bạn có chắc muốn xóa ảnh này?')) {
                    fetch(`/api/delete/${clientId}/${date}/${filename}`, { method: 'DELETE' })
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                location.reload();
                            } else {
                                alert('Error: ' + data.message);
                            }
                        });
                }
            }
            
            function deleteAll() {
                if (confirm('Xóa tất cả ảnh của ngày {{ selected_date }}?')) {
                    fetch(`/api/delete-date/{{ client_id }}/{{ selected_date }}`, { method: 'DELETE' })
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                location.reload();
                            } else {
                                alert('Error: ' + data.message);
                            }
                        });
                }
            }

            function deleteClient() {
                if (confirm('CẢNH BÁO: Xóa toàn bộ dữ liệu thiết bị này?')) {
                    fetch(`/api/delete-all/{{ client_id }}`, { method: 'DELETE' })
                         .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                window.location.href = '/';
                            } else {
                                alert('Error: ' + data.message);
                            }
                        });
                }
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(DETAIL_TEMPLATE, 
        client_name=client_name, 
        short_id=short_id,
        client_id=client_id,
        images=paginated_images,  # Paginated images for display
        all_images=processed_images,  # All images for viewer navigation
        dates=dates,
        selected_date=selected_date,
        page=page,
        total_pages=total_pages,
        total_images=total_images
    )

@app.route('/api/delete/<client_id>/<date>/<filename>', methods=['DELETE'])
def delete_image(client_id, date, filename):
    """Xóa 1 ảnh trong ngày"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, client_id, date, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': 'Image deleted'})
        else:
            return jsonify({'success': False, 'message': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/delete-date/<client_id>/<date>', methods=['DELETE'])
def delete_date_images(client_id, date):
    """Xóa tất cả ảnh trong 1 ngày"""
    try:
        folder_path = os.path.join(UPLOAD_FOLDER, client_id, date)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            return jsonify({'success': True, 'message': 'Date folder deleted'})
        return jsonify({'success': False, 'message': 'Folder not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/delete-all/<client_id>', methods=['DELETE'])
def delete_all_images(client_id):
    """Xóa tất cả ảnh của 1 client"""
    try:
        import shutil
        client_path = os.path.join(UPLOAD_FOLDER, client_id)
        if os.path.exists(client_path):
            shutil.rmtree(client_path)
            return jsonify({'success': True, 'message': 'All images deleted'})
        else:
            return jsonify({'success': False, 'message': 'Client not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def open_browser():
    """Tự động mở browser sau 1.5 giây"""
    import time
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print("="*60)
    print("🚀 CapScreen Server Starting...")
    print("="*60)
    print(f"📍 Server URL: http://localhost:{PORT}")
    print(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print("="*60)
    print("🌐 Opening browser...")
    print("🛑 Press Ctrl+C to stop")
    print("="*60)
    
    # Mở browser trong thread riêng
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Chạy server
    app.run(host='0.0.0.0', port=PORT, debug=False)
