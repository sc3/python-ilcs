import csv
import os.path

sections = []
ilrs_to_ilcs = {}

class BaseSection(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

class ILCSSection(BaseSection):
    """
    A section of the Illinois Compiled Statutes (ILCS).

    Args:
        chapter (str): Chapter number of the section.
        act_prefix (str): Act prefix number of the section.
        section (str): Section number within the chapter and act.

    Attributes:
        chapter (str): Chapter number of the section.
        act_prefix (str): Act prefix number of the section.
        section (str): Section number within the chapter and act.

    """

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
    """
    A section of the Illinois Revised Statutes (ILRS).

    Args:
        chapter (str): Chapter number of the section.
        paragraph (str): Paragraph number of the section.

    Attributes:
        chapter (str): Chapter number of the section.
        paragraph (str): Paragraph number of the section.

    """
    def __init__(self, **kwargs):
        super(ILRSSection, self).__init__(**kwargs)

        # Some data files may specify chapter "56 1/2" as "56.5".
        # Try to handle this gracefully.
        self.chapter = self.chapter.replace(".5", " 1/2")

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
    """
    Populate list of sections and ILRS to ILCS crosswalk from data file
    
    Args:
        filename (str): Filename of data file containing the section
            definitions.  Defaults to ``{package_dir}/data/ilrs2ilcs.csv``.

    Returns:
        Tuple where the first value is a list of all ILCS sections and the 
        second value is a dictionary mapping ILRSSection objects to their
        corresponding ILCSSection objects.

    """
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
    """
    Look up an ILCS section based on its corresponding ILRS section.

    Args:
        chapter (str): Chapter number of ILRS chapter.
        paragraph (str): Paragraph number of ILRS chapter.

    Returns:
        ILCSSection object corresponding to the chapter and paragraph
        of the ILRS section.

    Raises:
        KeyError if an ILCS section matching the ILRS chapter and
        paragraph doesn't exist.

    """
    ilrs_section = ILRSSection(chapter=chapter, paragraph=paragraph)
    return ilrs_to_ilcs[ilrs_section]


sections, ilrs_to_ilcs = load_sections() 
