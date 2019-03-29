import sys
import time
import ctypes
import random

import pyautogui as pag

from lib import mouse
from lib import keyboard

sys.setrecursionlimit(9999999)  # set high recursion limit for functions that
# call themselves.
conf = 0.95  # Set the default confidence value for imagesearches.

# Obtain primary screen dimensions.
user32 = ctypes.windll.user32
screenx = user32.GetSystemMetrics(0)
screeny = user32.GetSystemMetrics(1)
halfscreenx = (int(screenx / 2))
halfscreeny = (int(screeny / 2))


def docked_check():
    # Check if the ship is currently docked by looking for the undock icon.
    undock_icon = pag.locateCenterOnScreen('./img/undock.bmp',
                                           confidence = conf)
    if undock_icon is None:
        print('docked_check -- not docked')
        return 0
    elif undock_icon is not None:
        print('docked_check -- docked')
        return 1


def open_ship_inv():
    # Click on the ship's inventory button in the inventory window while
    # docked.
    print('open_ship_inv -- opening ship inventory')
    ship_inv = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                        confidence = conf)
    while ship_inv is None:
        print("open_ship_inv -- can't find ship inventory")
        ship_inv = pag.locateCenterOnScreen('./img/cargo_hold.bmp',
                                            confidence = conf)
        time.sleep(1)
    else:
        (ship_invx, ship_invy) = ship_inv
        pag.moveTo((ship_invx + (random.randint(-4, 50))),
                   (ship_invy + (random.randint(-6, 6))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def open_spec_inv():
    # If a special inventory was found (for ore, minerals, planetary
    # products etc.) click on it in
    # inventory window while docked.
    print('open_spec_inv -- opening special inventory')
    spec_inv = pag.locateCenterOnScreen('./img/special_hold.bmp',
                                        confidence = conf)
    while spec_inv is None:
        print("open_spec_inv -- can't find special hold")
        spec_inv = pag.locateCenterOnScreen('./img/special_hold.bmp',
                                            confidence = conf)
        time.sleep(1)
    else:
        (spec_invx, spec_invy) = spec_inv
        pag.moveTo((spec_invx + (random.randint(-4, 50))),
                   (spec_invy + (random.randint(15, 30))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def open_station_inv():
    # Click on the station inventory button within the main inventory window
    # while docked.
    print('open_station_inv -- opening station inventory')
    station_inv = pag.locateCenterOnScreen('./img/station_hangar.bmp',
                                           confidence = conf)
    while station_inv is None:
        print(
            "open_station_inv -- can't find station inventory icon")
        station_inv = pag.locateCenterOnScreen('./img/station_hangar.bmp',
                                               confidence = conf)
        time.sleep(1)
    else:
        (station_inv, station_invy) = station_inv
        pag.moveTo((station_inv + (random.randint(-6, 50))),
                   (station_invy + (random.randint(-6, 6))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def focus_inv_window():
    # Click somewhere inside the station inventory window to focus it before
    # any items are selected. Look for the sorting buttons in top right corner
    # of the inventory window and position the mouse cursor relative to those
    # buttons to click a non-interactive area within the inventory window.
    sort_station_inv = pag.locateCenterOnScreen(
        './img/sorting_station_hangar.bmp', confidence = conf)
    while sort_station_inv is None:
        print("focus_inv_window -- can't find sorting icon")
        sort_station_inv = pag.locateCenterOnScreen(
            './img/sorting_station_hangar.bmp', confidence = conf)
        time.sleep(1)
    else:
        (sort_station_invx,
         sort_station_invy) = sort_station_inv
        pag.moveTo((sort_station_invx - (random.randint(0, 250))),
                   (sort_station_invy + (random.randint(50, 300))),
                   mouse.move_time(), mouse.mouse_path())
        mouse.click()
        return


def look_for_items():
    # Look at the bottom-right corner of the station inventory window for the
    # '0 items found' text. If it isn't present, there must be items in the
    # station's inventory.
    global no_items_station_inv
    global namefield_station_inv
    no_items_station_inv = pag.locateCenterOnScreen(
        './img/no_items_station_hangar.bmp',
        confidence = .99)
    if no_items_station_inv is None:
        namefield_station_inv = pag.locateCenterOnScreen(
            './img/namefield_station_hangar.bmp',
            confidence = conf)
        return 1
    elif no_items_station_inv is not None:
        print('look_for_items -- no more items')
        return 0


def look_for_spec_inv():
    # Look for a drop-down arrow next to your ship icon in the station
    # inventory window, indicating the ship has a special inventory.
    spec_inv = pag.locateCenterOnScreen('./img/special_hold.bmp',
                                        confidence = conf)
    no_additional_invs = pag.locateCenterOnScreen(
        './img/no_additional_bays.bmp', confidence = conf)
    if spec_inv is not None and no_additional_invs is None:
        print('look_for_spec_inv -- found special inventory')
        return 1
    else:
        return 0


def spec_inv_warning():
    # Look for a popup indicating the selected inventory items aren't
    # compatible with the ship's special inventory. This warning is partially
    # transparent so confidence rating must be slightly lower than normal.
    spec_inv_warning = pag.locateCenterOnScreen(
        './img/special_hold_warning.bmp', confidence = 0.8)
    if spec_inv_warning is None:
        return 0
    else:
        print('spec_inv_warning -- detected')
        return 1


def set_quant_popup():
    # Check if a 'set quantity' window appears, indicating there isn't enough
    # space in the ship's inventory for a full item stack.
    set_quant = pag.locateCenterOnScreen('./img/set_quantity.bmp',
                                         confidence = conf)
    if set_quant is None:
        return 0
    else:
        print('set_quant_popup -- detected')
        keyboard.enter()
        return 1


def not_enough_space_popup():
    # Check if a 'not enough space' popup appears, indicating the item stacks
    # selected will not fit into the ship's inventory, or inventory is
    # already full.
    not_enough_space = pag.locateCenterOnScreen('./img/not_enough_space.bmp',
                                                confidence = conf)
    if not_enough_space is None:
        return 0
    else:
        print('not_enough_space_popup -- detected')
        keyboard.enter()
        return 1


def undock():
    # Undock from the station with the default hotkey. The undock has been
    # completed once the script sees the cyan ship icon in the top left corner
    # of the client window, indicating a session change has just ocurred.
    print('undock -- undocking')
    pag.keyDown('alt')  # alt+u
    time.sleep(float(random.randint(200, 1200)) / 1000)
    pag.keyDown('u')
    time.sleep(float(random.randint(200, 1200)) / 1000)
    pag.keyUp('u')
    time.sleep(float(random.randint(200, 1200)) / 1000)
    pag.keyUp('alt')
    time.sleep(int((random.randint(5000, 10000) / 1000)))
    undocked = pag.locateCenterOnScreen('./img/session_change_undocked.bmp',
                                        confidence = 0.55,
                                        region = (
                                            0, 0, (int(screenx / 5)), screeny))
    while undocked is None:
        time.sleep(int((random.randint(3000, 10000) / 1000)))
        print('undock -- trying undocking second time')
        pag.keyDown('alt')
        time.sleep(float(random.randint(200, 1200)) / 1000)
        pag.keyDown('u')
        time.sleep(float(random.randint(200, 1200)) / 1000)
        pag.keyUp('u')
        time.sleep(float(random.randint(200, 1200)) / 1000)
        pag.keyUp('alt')
        time.sleep(int((random.randint(5000, 10000) / 1000)))
        undocked = pag.locateCenterOnScreen(
            './img/session_change_undocked.bmp', confidence = 0.55,
            region = (0, 0, (int(screenx / 5)), screeny))
    if undocked is not None:
        time.sleep(int((random.randint(2000, 3000) / 1000)))
        return
