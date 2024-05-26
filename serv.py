import cv2
import atexit
from flask import Flask, render_template, Response, request
from pyngrok import ngrok
import pyaudio

app = Flask(__name__, template_folder='html/views')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
camera = cv2.VideoCapture(0)
ngrok_url = None
ngrok.set_auth_token('2h1I4PTW5Z8eLhcIa2FJIMXfbp3_3V5M61u9HaGQyxj4EL32x')

FORMAT=pyaudio.paInt16
CHANNELS=2
RATE=44100
CHUNK=1024
RECORD_SECONDS=5


audio_stream=pyaudio.PyAudio()


def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o


def Sound():
    bitspersample=16
    wav_hader=genHeader(RATE,bitspersample,2)
    stream=audio_stream.open(format=FORMAT,channels=2,rate=RATE,input=True,input_device_index=1,frames_per_buffer=CHUNK)
    first_run=True
    while True:
        if first_run:
            data=wav_hader+stream.read(CHUNK)
            first_run=False
        else:
            data=stream.read(CHUNK)
        yield(data)


try:
    tunnel = ngrok.connect(135)
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

@app.route("/audio")
def audio():
    return Response(Sound())

if __name__ == '__main__':
    app.run()
