from modules._template import Template

class Module(Template):

    def __init__(self):
        pattern_list = [r"regex1", r"regex2"] # All the expressions you want
        super(Module, self).__init__(pattern_list, "test_js")

