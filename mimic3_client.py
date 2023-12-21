#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
##
## Copyright 2023 Henry Kroll <nospam@thenerdshow.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
## MA 02110-1301, USA.
##
# This client is a drop-in replacement for `spd-say`.
# But this can also run as a Python module!

import sys
import requests
import subprocess
import io

# Update the location of your default speech server.
def say(text, base_url="http://localhost:59125/api/tts"):
    # params = { 'text': text, "lengthScale": "0.6" }
    params = { 'text': text, "voice": "en_US/vctk_low" }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            audio_data = io.BytesIO(response.content)
            audio_bytes = audio_data.read()
            # Pass the audio data to gstreamer-1.0 for playback
            # You could also use `aplay -` for this
            command = ['gst-launch-1.0', '-q', 'fdsrc', '!', 'wavparse', '!', 'autoaudiosink']
            subprocess.run(command, input=audio_bytes, check=True,
            stdout=subprocess.DEVNULL)
        else:
            sys.stderr.write("Error:", response.status_code)
    except Exception as e:
        sys.stderr.write("Cannot contact speech-dispatcherd service.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        say(sys.argv[1])
    else:
        sys.stderr.write("Import say from mimic3_client in Python. Or test from command line with `mimic3_client 'this is a test'`")
