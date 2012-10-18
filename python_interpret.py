# coding=utf-8
import sublime_plugin


class InterpretWithPythonCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()

        edit = view.begin_edit()

        sels = view.sel()

        # Interpret forwards
        replaces = []
        for sel in sels:
            if sel.size() > 0:
                text = view.substr(sel)
                evald = self.evaluate(text)
                replaces.append((sel, evald))

        # Replace backwards (intention is to later get them to share context)
        for (sel, evald) in reversed(replaces):
            view.replace(edit, sel, evald)

        view.end_edit(edit)

    def evaluate(self, text):
        try:
            ret = str(eval(text))
        except Exception, e:
            ret = e.message
        return ret
