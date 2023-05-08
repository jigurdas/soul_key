import cv2
import atexit
from flask import Flask, render_template, Response, request
from pyngrok import ngrok

app = Flask(__name__, template_folder='html/views')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
camera = cv2.VideoCapture(0)
ngrok_url = None

try:
    tunnel = ngrok.connect(5000, auth_token='ngrokToken')
    ngrok_url = tunnel.public_url.replace("https", "http")
    atexit.register(lambda: ngrok.disconnect(tunnel.public_url))
    print(" * Ngrok Tunnel:", ngrok_url)
except Exception as e:
    print("Failed to create ngrok tunnel:", e)
    exit()

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
