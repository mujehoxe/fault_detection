import urwid
from simulator import Simulator

from state import State


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
        response = urwid.Text([u'Set ', choice, u' state', u'\n'])

        back = urwid.Button(u'Back')

        state_buttons = self.init_state_buttons(choice)

        urwid.connect_signal(back, 'click', self.back_to_menu)
        self.main.original_widget = urwid.Filler(
            urwid.Pile(
                [response,
                 urwid.AttrMap(back, None, focus_map='reversed')]))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def init_state_buttons(self, choice):

        def change_detector_state(state_name):
            self.simulator.set_detector_state(choice, state_name)

        state_buttons = []
        for state_cls in State.__subclasses__():
            state_button = urwid.Button(state_cls.__name__)
            state_buttons.append(state_button)
            urwid.connect_signal(state_button, 'click',
                                 change_detector_state, state_cls.__name__)
        return state_buttons

    def run(self):
        urwid.MainLoop(
            self.top,
            palette=[('reversed', 'standout', '')]).run()
