# coding=utf-8
import sublime_plugin


class InterpretWithPythonCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()

        edit = view.begin_edit()

        # Import
        for import_me in ['math', 'random']:
            module = __import__(import_me, globals(), locals(), ['*'])
            for k in dir(module):
                locals()[k] = getattr(module, k)

        # Interpret forwards
        replaces = []
        for sel in view.sel():
            if sel.size() > 0:
                text = view.substr(sel)

                try:
                    evald = str(eval(text))
                except Exception, e:
                    evald = e.message
                replaces.append((sel, evald))

        # Replace backwards (intention is to later get them to share context)
        for (sel, evald) in reversed(replaces):
            view.replace(edit, sel, evald)

        view.end_edit(edit)
