import pyautogui
import pyperclip
import time
import os
import mss
import numpy as np
from PIL import Image

from check import check_compile_pass, check_test_result
from problems import id_name_map, id_testorder_map

# Utils #
def take_screenshot():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[0])
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        img = np.array(img)
        return img

def locate_on_screen(image_path, grayscale=None, confidence=0.95):
    '''
    Replace `pyautogui.locateOnScreen`
    '''
    try:
        return pyautogui.locateOnScreen(image_path, grayscale=grayscale, confidence=confidence)
    except Exception as e:
        return None

def wait_to_find_image_location(image_path, grayscale=False, confidence=0.95, timeout=None):
    time_start = time.time()
    while True:
        location = locate_on_screen(image_path, grayscale=grayscale, confidence=confidence)
        if location:
            return location
        time.sleep(0.05)
        if timeout and time.time() - time_start > timeout:
            return None

def locate_center_on_screen(image_path, grayscale=None, confidence=0.95):
    '''
    Replace `pyautogui.locateCenterOnScreen`
    '''
    try:
        return pyautogui.locateCenterOnScreen(image_path, grayscale=grayscale, confidence=confidence)
    except Exception as e:
        return None

def wait_to_find_image_center(image_path, grayscale=False, confidence=0.95, timeout=None):
    time_start = time.time()
    while True:
        location = locate_center_on_screen(image_path, grayscale=grayscale, confidence=confidence)
        if location:
            return location
        time.sleep(0.05)
        if timeout and time.time() - time_start > timeout:
            return None

def click_location(location, left=True, clicks=1):
    pyautogui.click(location, button='left' if left else 'right', clicks=clicks, _pause=False)
    time.sleep(0.02)

# Functions #
def make_sure_app_front():
    front_location = locate_center_on_screen('locator/marker_front.png')
    if not front_location:
        back_location = locate_center_on_screen('locator/icon.png')
        if not back_location:
            raise NotImplementedError
        click_location(back_location)
        front_location = wait_to_find_image_center('locator/marker_front.png')
    # else:
    #     print("App is already at front")
    return front_location

def get_scrollbar_top_location():
    scrollbar_location = wait_to_find_image_location('locator/menu/scrollbar.png')
    scrollbar_location = pyautogui.Point(scrollbar_location.left + scrollbar_location.width // 2, scrollbar_location.top + scrollbar_location.height)
    return scrollbar_location

def scroll_left_menu_to_top(scrollbar_location):
    click_location(scrollbar_location, left=False)
    pyautogui.press('down', presses=2)
    pyautogui.press('enter')

def scroll_left_menu_to_bottom(scrollbar_location):
    click_location(scrollbar_location, left=False)
    pyautogui.press('down', presses=3)
    pyautogui.press('enter')

def find_image_in_left_menu(image_path, scrollbar_location, confidence=0.95, go_to_top=True):
    if go_to_top:
        scroll_left_menu_to_top(scrollbar_location)
    screen_last = take_screenshot()
    while True:
        image_location = locate_center_on_screen(image_path, grayscale=True, confidence=confidence)
        if image_location:
            return image_location
        click_location(scrollbar_location, left=False)
        pyautogui.press('up', presses=3)
        pyautogui.press('enter')
        time.sleep(0.3)
        screen_new = take_screenshot()
        if (screen_new == screen_last).all():
            print("Scrolled to end!")
            return None
        screen_last = screen_new

def reload_project():
    mouse_exile_location = make_sure_app_front()
    scrollbar_location = get_scrollbar_top_location()
    scroll_left_menu_to_bottom(scrollbar_location)
    pyautogui.moveTo(mouse_exile_location)
    pyautogui.hotkey('ctrl', 'o')
    pyautogui.press('enter')
    discard_button_location = wait_to_find_image_location('locator/discard_changes.png', timeout=5)
    if discard_button_location:
        pyautogui.hotkey('shift', 'tab')
        pyautogui.press('enter')
    plc_folded_location = wait_to_find_image_center('locator/menu/project.png')
    pyautogui.click(plc_folded_location)
    pyautogui.press('down', presses=3)
    pyautogui.press('right')
    pyautogui.press('down', presses=6)
    pyautogui.press('right')

def run_test(problem_id, problem_dir=None):
    """
    Return:
        compile_pass: bool
        test_case_correct: int
        test_case_total: int
        message: str
    """
    mouse_exile_location = make_sure_app_front()
    scrollbar_location = get_scrollbar_top_location()

    # Load SCL file
    upload_file_button = find_image_in_left_menu('locator/menu/item_add_external_file.png', scrollbar_location)
    click_location(upload_file_button, clicks=2)
    problem_path = f"{problem_id}.scl"
    if problem_dir:
        problem_path = os.path.abspath(os.path.join(problem_dir, problem_path))
    pyperclip.copy(problem_path)
    pyautogui.hotkey('ctrl' ,'v')
    pyautogui.press('enter')
    wait_to_find_image_location('locator/text_import_file_conflict.png', grayscale=True, confidence=0.8)
    pyautogui.press('tab', presses=2)
    pyautogui.press('down')
    pyautogui.press('enter')

    # Generate block from file
    pyautogui.moveTo(mouse_exile_location)
    pyautogui.press('down')
    pyautogui.press('up')
    pyautogui.press('apps')
    pyautogui.press('up', presses=5)
    pyautogui.press('enter')

    # Compile
    while True:
        compile_success_location = locate_on_screen(image_path='locator/msgbox/compile_success.png', grayscale=True)
        compile_error_location = locate_on_screen(image_path='locator/msgbox/compile_error.png', grayscale=True)
        compile_warning_location = locate_on_screen(image_path='locator/msgbox/compile_warning.png', grayscale=True)
        if compile_success_location or compile_error_location or compile_warning_location:
            break
    time.sleep(2)
    load_output_location = compile_error_location if compile_error_location else compile_success_location if compile_success_location else compile_warning_location
    load_output_location = pyautogui.Point(load_output_location.left + load_output_location.width // 2, load_output_location.top + load_output_location.height)
    # click_location(load_output_location, left=False)
    click_location(load_output_location, clicks=2)
    pyautogui.press('apps')
    wait_to_find_image_location(image_path='locator/msgbox/text_copy_test_result.png')
    pyautogui.press('down', presses=2)
    pyautogui.press('enter')
    pyautogui.moveTo(mouse_exile_location)
    pyautogui.press('apps')
    pyautogui.press('down', presses=3)
    pyautogui.press('enter')
    compile_message = pyperclip.paste()
    compile_passed = check_compile_pass(compile_message, problem_id)
    if not compile_passed:
        return compile_passed, 0, 100, compile_message
    
    # Find and run test case
    problem_file_location = find_image_in_left_menu(f'locator/menu/item_test.png', scrollbar_location, confidence=0.8, go_to_top=False)
    click_location(problem_file_location)
    pyautogui.moveTo(mouse_exile_location)
    pyautogui.press('right')
    pyautogui.press('down', presses=2)
    pyautogui.press('right')
    pyautogui.press('down', presses=3 + id_testorder_map[problem_id])
    pyautogui.press('up')
    pyautogui.press('apps')
    pyautogui.press('down', presses=3)
    pyautogui.press('enter')
    # Notification for "can not trust device" begins
    while True:
        cant_trust_location = locate_center_on_screen(image_path='locator/text_cant_trust_device.png', grayscale=True)
        run_error_location = locate_center_on_screen(image_path='locator/msgbox/run_error.png')
        if cant_trust_location or run_error_location:
            break
    if run_error_location:
        test_output_location = wait_to_find_image_center(image_path='locator/msgbox/test_error.png', grayscale=True)
    else:
        pyautogui.press('tab', presses=3)
        pyautogui.press('enter')
        test_output_location = wait_to_find_image_center(image_path='locator/msgbox/test_info.png', grayscale=True)
    click_location(test_output_location, left=False)
    wait_to_find_image_location(image_path='locator/msgbox/text_copy_test_result.png')
    pyautogui.press('down', presses=2)
    pyautogui.press('enter')
    pyautogui.moveTo(mouse_exile_location)
    pyautogui.press('apps')
    pyautogui.press('down', presses=3)
    pyautogui.press('enter')
    run_message = pyperclip.paste()
    compile_passed, num_correct_tests, num_total_tests = check_test_result(run_message)
    return compile_passed, num_correct_tests, num_total_tests, run_message

def test_problem(problem_id, code, problem_dir):
    os.makedirs(problem_dir, exist_ok=True)
    open(os.path.join(problem_dir, f"{problem_id}.scl"), 'w', encoding='utf-8-sig').write(code.strip())
    compile_passed, num_correct_tests, num_total_tests, message = run_test(problem_id, problem_dir=problem_dir)
    reload_project()
    return compile_passed, num_correct_tests, num_total_tests, message
