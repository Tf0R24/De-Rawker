import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    
import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import subprocess

logging.basicConfig(level=logging.DEBUG)

def get_visible_ssids(interface='wlan0'):
    try:
        # Run the iwlist command to get wireless information
        result = subprocess.check_output(['iwlist', interface, 'scan'], stderr=subprocess.STDOUT)

        # Decode the byte output to string
        result = result.decode('utf-8')

        # Extract SSIDs from the result
        ssids = [line.split('ESSID:"')[1].split('"')[0] for line in result.split('\n') if 'ESSID:' in line]

        return ssids

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []




# MAIN MAIN MAIN MAIN MAIN

# Get the list of visible SSIDs
visible_ssids = get_visible_ssids()

try:   
    epd = epd2in13_V2.EPD()
    logging.info("init and clear display")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

	#init font
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    draw.text((0, 0), 'Visible Networks', font = font15, fill = 0)
    draw.text((0, 20), 'test_networkssid1', font = font15, fill = 0)
    draw.text((0, 40), 'test_networkssid2', font = font15, fill = 0)
    draw.text((0, 60), 'test_networkssid3', font = font15, fill = 0)
    draw.text((0, 80), 'test_networkssid4', font = font15, fill = 0)
    draw.text((0, 100), 'test_networkssid5', font = font15, fill = 0)
    draw.text((0, 120), 'test_networkssid6', font = font15, fill = 0)
    
    # for x in range (0, 6):
    #     draw.text(20, 20)
    epd.display(epd.getbuffer(image))

    # # epd.Clear(0xFF)
    # logging.info("Clear...")
    # epd.init(epd.FULL_UPDATE)
    # epd.Clear(0xFF)
    
    # logging.info("Goto Sleep...")
    # epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()