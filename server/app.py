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
    <title>CapScreen - Dashboard</title>
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
                images = sorted([f for f in os.listdir(client_path) if f.endswith('.png')])
                total_screenshots += len(images)
                
                if images:
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
    
    return render_template_string(
        HTML_TEMPLATE,
        clients=clients,
        total_clients=len(clients),
        online_clients=online_count,
        total_screenshots=total_screenshots
    )

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
        
        # Tạo thư mục client
        client_folder = os.path.join(UPLOAD_FOLDER, client_id)
        os.makedirs(client_folder, exist_ok=True)
        
        # Lưu client_name vào file
        name_file = os.path.join(client_folder, 'client_name.txt')
        with open(name_file, 'w') as f:
            f.write(client_name)
        
        # Lưu ảnh
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{timestamp}.png'
        filepath = os.path.join(client_folder, filename)
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
    
    # Đọc client_name
    name_file = os.path.join(client_path, 'client_name.txt')
    if os.path.exists(name_file):
        with open(name_file, 'r') as f:
            client_name = f.read().strip()
    else:
        client_name = client_id[:5] if len(client_id) > 5 else client_id
    
    short_id = client_id[-5:] if len(client_id) > 5 else client_id
    
    images = sorted([f for f in os.listdir(client_path) if f.endswith('.png')], reverse=True)
    
    html = f'''
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{client_name} - Gallery</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary: #4F46E5;
                --primary-dark: #4338CA;
                --bg: #F3F4F6;
                --card-bg: #FFFFFF;
                --text-main: #111827;
                --text-secondary: #6B7280;
                --danger: #EF4444;
                --danger-hover: #DC2626;
            }}
            
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background-color: var(--bg);
                color: var(--text-main);
                min-height: 100vh;
                padding: 2rem;
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}

            /* Header */
            .detail-header {{
                background: var(--card-bg);
                padding: 1.5rem 2rem;
                border-radius: 1rem;
                margin-bottom: 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}

            .header-info h1 {{
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-main);
                margin-bottom: 0.25rem;
            }}

            .header-meta {{
                color: var(--text-secondary);
                font-size: 0.875rem;
            }}

            .header-actions {{
                display: flex;
                gap: 1rem;
            }}

            /* Buttons */
            .btn {{
                padding: 0.625rem 1.25rem;
                border-radius: 0.5rem;
                font-weight: 500;
                font-size: 0.875rem;
                cursor: pointer;
                text-decoration: none;
                border: none;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            }}

            .btn-secondary {{
                background-color: #E5E7EB;
                color: var(--text-main);
            }}
            .btn-secondary:hover {{ background-color: #D1D5DB; }}

            .btn-danger {{
                background-color: var(--danger);
                color: white;
            }}
            .btn-danger:hover {{ background-color: var(--danger-hover); }}

            /* Grid */
            .images-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 1.5rem;
            }}

            .image-card {{
                background: var(--card-bg);
                border-radius: 0.75rem;
                overflow: hidden;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                transition: transform 0.2s;
                display: flex;
                flex-direction: column;
            }}

            .image-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}

            .image-card img {{
                width: 100%;
                height: 200px;
                object-fit: cover;
                cursor: pointer;
                background-color: #f3f4f6;
            }}

            .image-footer {{
                padding: 1rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid #E5E7EB;
                background-color: white;
            }}

            .time-label {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                font-family: monospace;
            }}

            .btn-del-sm {{
                padding: 0.375rem 0.75rem;
                font-size: 0.75rem;
                color: var(--danger);
                background-color: #FEF2F2;
                border-radius: 0.375rem;
                font-weight: 500;
            }}
            .btn-del-sm:hover {{
                background-color: #FEE2E2;
            }}

            /* Modal */
            .modal {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.9);
                z-index: 100;
                justify-content: center;
                align-items: center;
                backdrop-filter: blur(4px);
            }}
            .modal.active {{ display: flex; }}
            .modal img {{
                max-width: 95%;
                max-height: 95%;
                border-radius: 0.5rem;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            }}

        </style>
    </head>
    <body>
        <div class="container">
            <div class="detail-header">
                <div class="header-info">
                    <h1>📸 {client_name}</h1>
                    <div class="header-meta">
                        ID: #{short_id} • {len(images)} screenshots
                    </div>
                </div>
                <div class="header-actions">
                    <a href="/" class="btn btn-secondary">
                        ← Quay lại
                    </a>
                    <button onclick="deleteAll()" class="btn btn-danger">
                        🗑️ Xóa tất cả ảnh
                    </button>
                    <button onclick="deleteClient()" class="btn btn-danger" style="background-color: #991B1B;">
                         Hủy thiết bị này
                    </button>
                </div>
            </div>
            
            <div class="images-grid">
    '''
    
    for img in images:
        # Parse timestamp from filename
        try:
            timestamp = img.replace('.png', '')
            dt = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
            time_str = dt.strftime('%H:%M:%S • %d/%m/%Y')
        except:
            time_str = img
        
        html += f'''
            <div class="image-card">
                <img src="/uploads/{client_id}/{img}" onclick="showModal(this.src)" loading="lazy">
                <div class="image-footer">
                    <span class="time-label">{time_str}</span>
                    <button onclick="deleteImage('{client_id}', '{img}')" class="btn btn-del-sm">Xóa</button>
                </div>
            </div>
        '''
    
    html += f'''
        </div>
        </div>
        
        <div class="modal" id="modal" onclick="this.classList.remove('active')">
            <img id="modal-img" src="">
        </div>
        
        <script>
            function showModal(src) {{
                document.getElementById('modal-img').src = src;
                document.getElementById('modal').classList.add('active');
            }}
            
            function deleteImage(clientId, filename) {{
                if (confirm('Bạn có chắc muốn xóa ảnh này?')) {{
                    fetch(`/api/delete/${{clientId}}/${{filename}}`, {{ method: 'DELETE' }})
                        .then(r => r.json())
                        .then(data => {{
                            if (data.success) {{
                                location.reload();
                            }} else {{
                                alert('Không thể xóa: ' + data.message);
                            }}
                        }});
                }}
            }}
            
            function deleteAll() {{
                if (confirm('CẢNH BÁO: Bạn chuẩn bị xóa TẤT CẢ {len(images)} ảnh của thiết bị này. Hành động này không thể hoàn tác!')) {{
                    fetch(`/api/delete-all/{client_id}`, {{ method: 'DELETE' }})
                        .then(r => r.json())
                        .then(data => {{
                            if (data.success) {{
                                location.reload(); // Reload để thấy trống
                            }} else {{
                                alert('Không thể xóa: ' + data.message);
                            }}
                        }});
                }}
            }}

            function deleteClient() {{
                if (confirm('CẢNH BÁO CAO ĐỘ: Bạn sắp xóa hoàn toàn thiết bị này và tất cả dữ liệu. Tiếp tục?')) {{
                    fetch(`/api/delete-all/{client_id}`, {{ method: 'DELETE' }})
                         .then(r => r.json())
                        .then(data => {{
                            if (data.success) {{
                                window.location.href = '/';
                            }} else {{
                                alert('Error: ' + data.message);
                            }}
                        }});
                }}
            }}
        </script>
    </body>
    </html>
    '''
    
    return html

@app.route('/api/delete/<client_id>/<filename>', methods=['DELETE'])
def delete_image(client_id, filename):
    """Xóa 1 ảnh"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, client_id, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return jsonify({'success': True, 'message': 'Image deleted'})
        else:
            return jsonify({'success': False, 'message': 'Image not found'}), 404
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
