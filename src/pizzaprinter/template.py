#!/usr/bin/env python3

from datetime import datetime
import os
import jinja2

from posprinter.suremark import SureMark

from .models import Receipt


def align_positions(pos: str) -> str:
    '''
    Returns the alignment code for the given `position`.
    1b61N
    '''
    ret = None
    if pos == 'left':
        ret = SureMark.ALIGN_POSITIONS + SureMark.ALIGN_POSITIONS_LEFT
    elif pos == 'center':
        ret = SureMark.ALIGN_POSITIONS + SureMark.ALIGN_POSITIONS_CENTER
    elif pos == 'right':
        ret = SureMark.ALIGN_POSITIONS + SureMark.ALIGN_POSITIONS_RIGHT
    else:
        raise ValueError('Invalid alignment')
    return ret.decode('utf-8')


def max_print_speed(speed: int) -> str:
    '''
    Changes the printing speed and with it the blackness of the text.
    1b2fN
    '''
    ret = None
    if speed == 52:
        ret = SureMark.MAX_PRINT_SPEED + SureMark.MAX_PRINT_SPEED_52
    elif speed == 35:
        ret = SureMark.MAX_PRINT_SPEED + SureMark.MAX_PRINT_SPEED_35
    elif speed == 26:
        ret = SureMark.MAX_PRINT_SPEED + SureMark.MAX_PRINT_SPEED_26
    elif speed == 15:
        ret = SureMark.MAX_PRINT_SPEED + SureMark.MAX_PRINT_SPEED_15
    else:
        raise ValueError('Invalid speed')
    return ret.decode('utf-8')


def set_print_mode(mode: int) -> str:
    '''
    Sets the print `mode`.
    1b21N
    '''
    if mode < 0 or mode > 255:
        raise ValueError('Invalid mode')
    ret = SureMark.CMD_SET_PRINT_MODE + bytes([mode])
    return ret.decode('utf-8')


def set_double_height() -> str:
    '''
    Enables double-height mode
    1b6801
    '''
    return (SureMark.CMD_SET_CANCEL_DOUBLE_HEIGHT_MODE + b'\x01').decode('utf-8')


def cancel_double_height() -> str:
    '''
    Disables double-height mode.
    1b6800
    '''
    return (SureMark.CMD_SET_CANCEL_DOUBLE_HEIGHT_MODE + b'\x00').decode('utf-8')


def set_code_page(page: int) -> str:
    '''
    Sets the code page.
    1b74N
    '''
    if page < 0 or page > 5:
        raise ValueError('Invalid code page')
    return (SureMark.CMD_SET_CODE_PAGE + bytes([page])).decode('utf-8')


def logo(density: int, number: int) -> str:
    '''
    Prints a logo from slot `number` with a specific `density`.
    1d2fMN
    '''
    if density < 0 or density > 2:
        raise ValueError('Invalid density')
    if number < 0 or number > 40:  # TODO some machines support 255
        raise ValueError('Logo# out of bounds')
    return (SureMark.CMD_PRINT_PREDEFINED_LOGO + bytes([density, number])).decode('utf-8')


def render(template: str, receipt: Receipt) -> str:
    '''
    Renders a given `template` file using a `receipt` data.

    Commands are registered and handed to jinja2, this allows for simple
    function calls instead of hard-to-read binary data in the templates.
    '''
    path, filename = os.path.split(template)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))

    t = env.get_template(filename)

    var = dict(
        # ### system variables ###
        # current data
        date=datetime.now().strftime('%d-%m-%Y'),
        # current time
        time=datetime.now().strftime('%H:%S'),

        # ### user supplied ###
        # day the order was created
        ordday=receipt.date.date(),
        # time the order was created
        ordtime=receipt.date.time(),
        # name of the user that ordered
        user=receipt.user,
        # name of the pizza
        pizza=receipt.pizza,
        # size of the pizza,
        size=receipt.size,
        # total price
        total=receipt.total,

        # ### control functions ###
        CUT=SureMark.CMD_PRINT_FORM_FEED_CUT.decode('utf-8'),
        align_positions=align_positions,
        max_print_speed=max_print_speed,
        set_print_mode=set_print_mode,
        set_double_height=set_double_height,
        cancel_double_height=cancel_double_height,
        set_code_page=set_code_page,
        logo=logo,
    )

    return t.render(**var)
