from unittest import TestCase
from molecupy import exceptions
from molecupy.structures import PdbBetaStrand, ResiduicSequence, PdbAtom, PdbResidue, PdbChain

class StrandTest(TestCase):

    def setUp(self):
        self.atom1 = PdbAtom(1.0, 1.0, 1.0, "H", 1, "H1")
        self.atom2 = PdbAtom(1.0, 1.0, 2.0, "C", 2, "CA")
        self.atom3 = PdbAtom(1.0, 1.0, 3.0, "O", 3, "OX1")
        self.residue1 = PdbResidue("A1", "ARG", self.atom1, self.atom2, self.atom3)
        self.atom4 = PdbAtom(1.0, 1.0, 4.0, "H", 4, "H1")
        self.atom5 = PdbAtom(1.0, 1.0, 5.0, "C", 5, "CA")
        self.atom6 = PdbAtom(1.0, 1.0, 6.0, "O", 6, "OX1")
        self.residue2 = PdbResidue("A2", "HST", self.atom4, self.atom5, self.atom6)
        self.atom7 = PdbAtom(1.0, 1.0, 7.0, "H", 7, "H1")
        self.atom8 = PdbAtom(1.0, 1.0, 8.0, "C", 8, "CA")
        self.atom9 = PdbAtom(1.0, 1.0, 9.0, "O", 9, "OX1")
        self.residue3 = PdbResidue("A3", "TRP", self.atom7, self.atom8, self.atom9)
        self.chain = PdbChain("A", self.residue1, self.residue2, self.residue3)


    def check_valid_strand(self, strand):
        self.assertIsInstance(strand, PdbBetaStrand)
        self.assertIsInstance(strand, ResiduicSequence)
        self.assertIsInstance(strand.strand_id, int)
        self.assertIsInstance(strand.residues, list)
        self.assertIsInstance(strand.sense, int)
        self.assertIsInstance(strand.get_chain(), PdbChain)
        self.assertIn(strand, strand.get_chain().beta_strands)
        self.assertRegex(str(strand), r"<BetaStrand (\d+) \((\d+) residues\)>")



class StrandCreationTests(StrandTest):

    def test_can_create_strand(self):
        strand = PdbBetaStrand(1, 0, self.residue1, self.residue2)
        self.check_valid_strand(strand)
        self.assertIs(strand.get_chain(), self.chain)


    def test_strand_id_must_be_int(self):
        with self.assertRaises(TypeError):
            strand = PdbBetaStrand("1", 0, self.residue1, self.residue2)
        with self.assertRaises(TypeError):
            strand = PdbBetaStrand(None, 0, self.residue1, self.residue2)


    def test_all_strand_residues_must_be_on_same_chain(self):
        new_residue = PdbResidue("B1", "VAL", PdbAtom(1.0, 1.0, 1.0, "H", 10, "H1"))
        new_chain = PdbChain("B", new_residue)
        with self.assertRaises(exceptions.BrokenStrandError):
            strand = PdbBetaStrand(1, 1, self.residue1, new_residue)


    def test_strand_sense_must_be_int(self):
        with self.assertRaises(TypeError):
            strand = PdbBetaStrand(1, "0", self.residue1, self.residue2)
        with self.assertRaises(TypeError):
            strand = PdbBetaStrand(1, None, self.residue1, self.residue2)


    def test_strand_sense_must_be_valid(self):
        with self.assertRaises(ValueError):
            strand = PdbBetaStrand(1, -2, self.residue1, self.residue2)
        with self.assertRaises(ValueError):
            strand = PdbBetaStrand(1, 2, self.residue1, self.residue2)
        strand = PdbBetaStrand(1, -1, self.residue1, self.residue2)
        strand = PdbBetaStrand(1, 1, self.residue1, self.residue2)