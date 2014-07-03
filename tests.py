from unittest import TestCase

import ilcs

class ILCSSectionTestCase(TestCase):
    def test_comparison(self):
        s1 = ilcs.ILCSSection(chapter="5", act_prefix="20", section="1") 
        s2 = ilcs.ILCSSection(chapter="5", act_prefix="20", section="1") 
        self.assertEqual(s1, s2)

    def test_str(self):
        s1 = ilcs.ILCSSection(chapter="5", act_prefix="20", section="1") 
        self.assertEqual(str(s1), "5 ILCS 20/1")


class ModuleGlobalsTestCase(TestCase):
    def test_sections_auto_loaded(self):
        self.assertEqual(len(ilcs.sections), 45561) 

    def test_lookup_by_ilrs(self):
        sections = ilcs.lookup_by_ilrs(chapter="1", paragraph="100")
        self.assertEqual(len(sections), 1)
        section = sections[0]
        self.assertEqual(section.chapter, "5")
        self.assertEqual(section.act_prefix, "20")
        self.assertEqual(section.section, "0.01")

