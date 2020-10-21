from abc import ABC
import re


class Template(ABC):

    def __init__(self, patterns, vulnerability):
        self.patterns = patterns
        self.vulnerability = vulnerability

    def check_code(self, filename, code):
        return self.analysis(self.patterns, filename, code, self.vulnerability)
    
    def analysis(self, patterns_list, filename, code, vulnerability):
        data = []
        line=[]
        for m in re.finditer('.*\n', code):
            line.append(m.end()+1)

        for pattern in patterns_list:
            match = re.compile(pattern, re.MULTILINE|re.IGNORECASE) 
                    
            for m in re.finditer(match, code):
                file_line = next(i for i in range(len(line)) if line[i] > m.start())
                match_pat = m.group(0)
                data.append({"file": filename, "line": file_line, 
                            "vulnerability": vulnerability, "code": match_pat})
        return data