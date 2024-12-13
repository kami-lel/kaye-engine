
LF = '\n'
HEADING_MARKER = '#'


from collections import OrderedDict


class PromptTreeNode(OrderedDict):
    """
    represents a node ina prompt tree structure

    :param text:
    :type text: str or list(str)
    :param level: level which this node exist, e.g.

    - ``0`` for root node (entire document)
    - ``1`` for 1st level section, i.e. an section of ``# heading``
    - etc.

    :type level: int, optional
    :param parent: parent of the node in the tree; ``None`` if root node
    :type parent: PromptTreeNode
    """

    def __new__(cls, text, level=0, parent=None):
        return super().__new__(cls, {})  # new as empty dict

    def __init__(self, text, level=0, parent=None):
        self.level = level
        self.parent = parent
        self.enable = False  # by default
        self._init_populate(text)

    def _init_populate(self, text):
        # convert to a list of str, each contain a line
        lines = list(text.split(LF)) if isinstance(text, str) else text
        if self.level == 0:
            lines = self._init_lines_cleanup(lines)

        level_next = self.level + 1
        heading_prefix = HEADING_MARKER * level_next + ' '

        # find every line which is a heading of next level
        heading_lines = OrderedDict()
        for idx, line in enumerate(lines):
            if line.startswith(heading_prefix):
                # extract heading content
                # e.g. "### this is heading " -> "this is heading"
                heading_content = line[level_next + 1:].strip()
                heading_lines[idx] = heading_content

        # e.g. now, heading_lines = {0: 'personality',
        #       38: 'conversation', 95: 'abbreviation', 512: 'role'}

        heading_lines_idx = list(heading_lines.keys())

        if heading_lines_idx:
            # set self.content
            first_line_idx = heading_lines_idx[0]
            self.content = LF.join(lines[1:first_line_idx])

            next_idx = heading_lines_idx[1:]
            next_idx.append(len(lines))
            subsections = OrderedDict()
            for (start_idx, heading), end_idx \
                    in zip(heading_lines.items(), next_idx):
                subsections[heading] = lines[start_idx: end_idx]

            # e.g. now subsections = {
            #       'personality': ['1st line in personality', '2nd line', 'etc'],
            #       'conversation': [...], 'abbreviation': [...], 'role': [...] }

            # populate self with subsections
            for heading, section_lines in subsections.items():
                self[heading] = PromptTreeNode(section_lines, level_next, self)

        else:  # i.e. no subsection, all lines are content
            self.content = LF.join(lines[1:])

    @staticmethod
    def _init_lines_cleanup(lines):
        """
        :param lines:
        :type lines: list(str)
        :return: lines, but remove every occurence of consecutive empty lines, then replace with a single empty line
        :rtype: list(str)
        """
        i = 0  # index
        while i < len(lines):
            if lines[i] == '':  # detect an empty line
                j = i + 1
                for _ in range(j, len(lines)):
                    if lines[j]:  # non-empty
                        break
                    j += 1

                lines = lines[:i+1] + lines[j:]

            i += 1

        return lines

    def set(self):
        """
        enable this node (& its sub-nodes) to be present during ``.md`` render (q.v. ``__str__``)
        """
        self._set_unset(True)

    def unset(self):
        """
        disable this node (& its sub-nodes) to be absent during ``.md`` render (q.v. ``__str__``)
        """
        self._set_unset(False)

    def _set_unset(self, enable=True):
        self.enable = enable

        parent = self.parent
        while parent is not None:
            parent.enable = enable
            parent = parent.parent

        for _, node in self.items():
            node._set_unset(enable)

    def __str__(self):
        """
        :return: rendered ``.md`` content, when conisder ``.enable`` of current node and sub-nodes
        :rtype: str
        """
        parts = [self.content]

        for heading, node in self.items():
            if node.enable:
                heading_md = HEADING_MARKER * node.level + ' ' + heading + LF
                part = heading_md + node.__str__()
                parts.append(part)

        return LF.join(parts)

    def __repr__(self, heading=''):
        """
        debug print of _PromptTreeNode, showing

        - node enable by ☑ or ☐
        - node content as 1st entry
        - heading & content of its sub-nodes
        """
        tab_prefix = '\t' * self.level

        first_line = \
                ('☑' if self.enable else '☐') + \
                tab_prefix + \
                HEADING_MARKER * self.level + " " + \
                heading + " " + \
                "{"

        content_line = repr(self.content[:64])

        nodes_repr = LF.join(
                node.__repr__(heading) for heading, node in self.items())

        last_line = "}"

        if nodes_repr:
            content_line = tab_prefix + content_line
            last_line = tab_prefix + last_line
            return LF.join([first_line, content_line, nodes_repr, last_line])
        else:
            return first_line + content_line + last_line
