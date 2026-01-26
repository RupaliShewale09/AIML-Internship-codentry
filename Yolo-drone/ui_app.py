import streamlit as st
import requests
from PIL import Image
import io
import time

FASTAPI_VIDEO_URL = "http://127.0.0.1:8000/video"
FASTAPI_STATS_URL = "http://127.0.0.1:8000/stats"

st.set_page_config(page_title="Drone Detection Dashboard", layout="wide", page_icon="🚁")

# ================= CSS =================
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 1.5rem;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 0.7rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        text-align: center;
    }
    
    .stats-card h3 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stats-card .value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Video frame styling */
    .video-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        border: 2px solid #e6e6e6;
    }
    
    /* Control buttons */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Header */
    .dashboard-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .dashboard-header h1 {
        color: #2c3e50;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-header p {
        color: #7f8c8d;
        font-size: 1.1rem;
    }

    /* ALERT */
    .alert-box {
        background: #ffebee;
        color: #b71c1c;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        margin-top: 1rem;
        animation: pulse 1s infinite;
    }

</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "running" not in st.session_state:
    st.session_state.running = False
if "drone_count" not in st.session_state:
    st.session_state.drone_count = 0
if "fps" not in st.session_state:
    st.session_state.fps = 0.0
if "connection_status" not in st.session_state:
    st.session_state.connection_status = "disconnected"
if "alert_active" not in st.session_state:
    st.session_state.alert_active = False

# ================= FUNCTIONS =================
def render_stats():
    drone_card.markdown(f"""
    <div class="stats-card" style="background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);">
        <h3>DRONES DETECTED</h3>
        <div class="value">{st.session_state.drone_count}</div>
    </div>
    """, unsafe_allow_html=True)

    fps_card.markdown(f"""
    <div class="stats-card" style="background: linear-gradient(135deg, #2196F3 0%, #0D47A1 100%);">
        <h3>PROCESSING FPS</h3>
        <div class="value">{st.session_state.fps:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

def play_browser_alert():
    # This will play a beep sound in browser when drones >= 3
    st.markdown("""
    <audio autoplay>
        <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
    </audio>
    """, unsafe_allow_html=True)

def show_alert_ui():
    st.markdown("""
    <div class="alert-box">
        🚨 ALERT! 3 or more drones detected 🚨
    </div>
    """, unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="dashboard-header" style="margin-top:-5rem;">
    <h1 >🚁 Drone Detection System</h1>
    <p>Real-time aerial object detection and tracking</p>
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT =================
col1, col2 = st.columns([3.5, 2], gap="large")

with col1:
    video_container = st.container(border=True)
    with video_container:
        frame_placeholder = st.empty()

    # Connection status
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        status_indicator = "🟢" if st.session_state.running else "🔴"
        status_text = "LIVE" if st.session_state.running else "PAUSED"
        st.markdown(f"**Status:** {status_indicator} {status_text}")

    with status_col2:
        connection_indicator = "🟢" if st.session_state.connection_status == "connected" else "🟡"
        st.markdown(f"**Connection:** {connection_indicator} {st.session_state.connection_status}")

with col2:
    control_container = st.container(border=True)
    with control_container:
        st.markdown("### 🎮 Control Panel")
        
        if not st.session_state.running:
            if st.button("▶ Start Detection", type="primary", width='stretch'):
                st.session_state.running = True
                st.session_state.connection_status = "connected"
                st.rerun()
        else:
            if st.button("⏸ Pause", type="secondary", width='stretch'):
                st.session_state.running = False
                st.rerun()

    

    st.markdown("---")
    stat_container = st.container(border=True)
    with stat_container:
        st.markdown("### 📊 Live Statistics")
        col_a, col_b = st.columns(2)
        with col_a:
            drone_card = st.empty()
        with col_b:
            fps_card = st.empty()

        alert_card = st.empty()

# ================= STREAM VIDEO =================
def stream_video():
    try:
        response = requests.get(FASTAPI_VIDEO_URL, stream=True, timeout=5)
        response.raise_for_status()

        bytes_buffer = b""
        frame_count = 0
        start_time = time.time()

        for chunk in response.iter_content(chunk_size=1024):
            if not st.session_state.running:
                st.session_state.connection_status = "paused"
                break

            bytes_buffer += chunk
            a = bytes_buffer.find(b"\xff\xd8")
            b = bytes_buffer.find(b"\xff\xd9")

            if a != -1 and b != -1:
                jpg = bytes_buffer[a:b+2]
                bytes_buffer = bytes_buffer[b+2:]
                frame_count += 1

                # Calculate FPS
                elapsed_time = time.time() - start_time
                actual_fps = frame_count / elapsed_time if elapsed_time > 0 else 0

                # Display frame
                try:
                    image = Image.open(io.BytesIO(jpg))
                    frame_placeholder.image(
                        image, channels="RGB", width='stretch', caption=f"Frame: {frame_count}"
                    )
                except Exception as e:
                    continue

                # Fetch stats
                try:
                    stats_response = requests.get(FASTAPI_STATS_URL, timeout=1)
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        st.session_state.drone_count = stats.get("drone_count", 0)
                        st.session_state.fps = stats.get("fps", actual_fps)
                        st.session_state.connection_status = "connected"

                        render_stats()

                        # ===== ALERT LOGIC =====
                        if st.session_state.drone_count >= 3:
                            if not st.session_state.alert_active:
                                play_browser_alert()
                                st.session_state.alert_active = True

                            show_alert_ui()
                        else:
                            st.session_state.alert_active = False
                            alert_card.empty()

                except requests.exceptions.RequestException:
                    st.session_state.connection_status = "reconnecting"
                    st.session_state.fps = actual_fps

                time.sleep(0.001)

    except requests.exceptions.RequestException:
        st.session_state.connection_status = "disconnected"
        frame_placeholder.error("⚠️ Cannot connect to video source. Please check the backend server.")
    except Exception as e:
        st.session_state.connection_status = "error"
        frame_placeholder.error(f"⚠️ Error: {str(e)}")

# ================= MAIN =================
if st.session_state.running:
    stream_video()
else:
    if st.session_state.drone_count == 0 and st.session_state.fps == 0:
        frame_placeholder.info(
            "👆 Click **Start Detection** to begin real-time drone monitoring\n\n"
            "The system will display live video feed and detection statistics."
        )
    else:
        frame_placeholder.warning(
            "⏸ Detection Paused\n\n"
            f"Last detected: **{st.session_state.drone_count} drones**\n"
            f"Last FPS: **{st.session_state.fps:.1f}**\n\n"
            "Click **Start Detection** to resume."
        )

# Auto-refresh when running
if st.session_state.running:
    time.sleep(0.1)
    st.rerun()
