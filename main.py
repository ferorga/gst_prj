import gi
import sys
import time

gi.require_version('Gst', '1.0')
gi.require_version('GstApp', '1.0')
gi.require_version('GstVideo', '1.0')
gi.require_version('GstBase', '1.0')

from gi.repository import Gst, GLib
from threading import Thread

Gst.init(sys.argv)

DEF_PIPELINE = "videotestsrc num-buffers=100 ! autovideosink"

loop = GLib.MainLoop()
loopTh = Thread(target=loop.run)
loopTh.start()

pipeline = Gst.parse_launch("filesrc location=/media/sf_SHARED/gst_frozen_n1.mp4 ! decodebin ! videoconvert ! autovideosink")

pipeline.set_state(Gst.State.PLAYING)

def message(bus, message):
    if message.type == Gst.MessageType.EOS:
        pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, 0)

bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect('message', message)

try:   
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
loop.quit()
loopTh.join()









