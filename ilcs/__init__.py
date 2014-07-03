import csv
import os.path

sections = []
ilrs_to_ilcs = {}

class BaseSection(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

class ILCSSection(BaseSection):
    def __repr__(self):
        return "<ILCSSection:{}>".format(str(self))

    def __str__(self):
        return "{} ILCS {}/{}".format(self.chapter, self.act_prefix,
            self.section)

    def __hash__(self):
        return hash((self.chapter, self.act_prefix, self.section))

    def __lt__(self, other):
        if self.chapter < other.chapter:
            return True
        elif self.chapter == other.chapter and self.act_prefix < other.act_prefix:
            return True
        elif (self.chapter == other.chapter and
              self.act_prefix == other.act_prefix and
              self.section < other.section):
            return True
        else:
            return False

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __eq__(self, other):
        return (self.chapter == other.chapter and
                self.act_prefix == other.act_prefix and 
                self.section == other.section)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)


class ILRSSection(BaseSection):
    def __repr__(self):
        return "<ILRSSection:{}>".format(str(self))

    def __str__(self):
        return "Ch. {}, par. {}".format(self.chapter, self.paragraph)

    def __hash__(self):
        return hash((self.chapter, self.paragraph))

    def __lt__(self, other):
        if self.chapter < other.chapter:
            return True
        elif self.chapter == other.chapter and self.paragraph < other.paragraph:
            return True
        else:
            return False

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __eq__(self, other):
        return (self.chapter == other.chapter and
                self.paragraph == other.paragraph)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__eq__(other) and not self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)


def load_sections(filename=None):
    sections = []
    ilcs_seen = set()
    ilrs_to_ilcs = {}

    if filename is None:
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'data', 'ilrs2ilcs.csv')

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ilrs_section = ILRSSection(
                chapter=row['ilrs_chapter'].strip(),
                paragraph=row['ilrs_paragraph'].strip())
            ilcs_section = ILCSSection(chapter=row['ilcs_chapter'].strip(),
                act_prefix=row['ilcs_act_prefix'].strip(),
                section=row['ilcs_section'].strip())

            try:
                ilcs_sections = ilrs_to_ilcs[ilrs_section]
                if ilcs_section not in ilcs_sections:
                    ilcs_sections.append(ilcs_sections)
            except KeyError:
                ilrs_to_ilcs[ilrs_section] = [ilcs_section,]

            if ilcs_section not in ilcs_seen:
                sections.append(ilcs_section)
                ilcs_seen.add(ilcs_section)

    return sections, ilrs_to_ilcs


def lookup_by_ilrs(chapter, paragraph):
    ilrs_section = ILRSSection(chapter=chapter, paragraph=paragraph)
    return ilrs_to_ilcs[ilrs_section]


sections, ilrs_to_ilcs = load_sections() 
