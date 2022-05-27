import asyncio
from chardet import detect
import urwid
from simulator import Simulator

from state import State, InActive


class Tui:

    def __init__(self, choices, simulator) -> None:
        self.choices = choices
        self.main = urwid.Padding(self.menu(), left=2, right=2)
        self.top = urwid.Overlay(self.main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 60),
                                 valign='middle', height=('relative', 60),
                                 min_width=20, min_height=9)
        self.simulator: Simulator = simulator

    def menu(self):
        body = [urwid.Divider()]
        for c in self.choices:
            button = urwid.Button(c)

            if c == "exit":
                urwid.connect_signal(button, 'click', self.exit_program)
            else:
                urwid.connect_signal(button, 'click', self.item_chosen, c)

            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def back_to_menu(self, button):
        self.main.original_widget = \
            urwid.Padding(self.menu(), left=2, right=2)

    def item_chosen(self, button, choice):
        detector = self.simulator.get_detector_by_id(choice)
        if(detector):
            response = urwid.Text(
                [u'Set ', detector._id, detector._state.name, u' state', u'\n'])
            back = urwid.Button(u'Back')
            state_buttons = self.init_state_buttons(detector, response)
            urwid.connect_signal(back, 'click', self.back_to_menu)
            pile = [response] + \
                state_buttons + \
                [urwid.AttrMap(back, None, focus_map='reversed')]
            self.set_original_widget(pile)

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def set_original_widget(self, pile):
        self.main.original_widget = urwid.Filler(
            urwid.Pile(pile))

    def init_state_buttons(self, detector, response: urwid.Text):

        def change_detector_state(button, state_name):
            while(self.simulator.get_time().is_integer()):
                pass
            self.simulator.set_detector_state(detector, state_name)
            #response.set_text([u'Set ', detector._id, detector._state.name, u' state', u'\n'])

        state_buttons = []
        for state_cls in State.__subclasses__():
            state_button = urwid.Button(state_cls.__name__)
            state_buttons.append(state_button)
            urwid.connect_signal(state_button, 'click',
                                 change_detector_state,
                                 user_arg=state_cls.__name__)

        return state_buttons

    def run(self):
        urwid.MainLoop(
            self.top,
            palette=[('reversed', 'standout', '')]).run()
