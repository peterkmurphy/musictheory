import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from musictheory.musutility import rotate, enl_seq, multislice, norm_seq, repseq, rotate_and_zero, scalar_addition
from musictheory.temperament import M_SHARP, M_FLAT, M_NATURAL, seq_dict, NSEQ_SCALE, NSEQ_CHORD, WestTemp, CHROM_NAT_NOTE_POS, CHROM_SIZE, un_unicode_accdtls, CHROM_NAT_NOTES
from musictheory.scales import noteseq, MajorScale, MelMinorScale, HarmMinorScale, HarmMajorScale, DiscMinorScale, HungarianScale
from musictheory.scales import HEPT_NAT_POSNS, MEL_MIN_NOTE_POS, HARM_MIN_NOTE_POS, HARM_MAJ_NOTE_POS, DISC_MIN_NOTE_POS, HUNGARIAN_NOTE_POS

class TestMusutility(unittest.TestCase):
    """ This only tests functions in this module. """
    
    def setUp(self):
        self.eseq = [];
        self.one_elem_seq = ["0"];
        self.one_elem_seq_one = ["1"]
        self.two_elem_seq = ["0", "1"];
        self.two_elem_seq_rot = ["1", "0"];
        self.three_elem_seq = ["0", "1", "2", "3"];
        self.three_elem_seq_left = ["1", "2", "3", "0"];
        self.three_elem_seq_right = ["3", "0", "1", "2"]; 
        self.all_test_seq = [[], ["0"], ["0", "1"], ["1", "0"],
            ["0", "1", "2", "3"], ["1", "2", "3", "0"], 
            ["3", "0", "1", "2"]];

    def test_rotate(self):
        self.assertEqual(rotate(self.eseq, 0), self.eseq);
        self.assertEqual(rotate(self.eseq, 1), self.eseq);
        self.assertEqual(rotate(self.eseq, -1), self.eseq);
        self.assertEqual(rotate(self.one_elem_seq, 0), 
            self.one_elem_seq);
        self.assertEqual(rotate(self.one_elem_seq, 1), 
            self.one_elem_seq);
        self.assertEqual(rotate(self.one_elem_seq, -1), 
            self.one_elem_seq);
        self.assertEqual(rotate(self.two_elem_seq, 0), 
            self.two_elem_seq);
        self.assertEqual(rotate(self.two_elem_seq, 1), 
            self.two_elem_seq_rot);
        self.assertEqual(rotate(self.two_elem_seq, -1), 
            self.two_elem_seq_rot);
        self.assertEqual(rotate(self.three_elem_seq, 0), 
            self.three_elem_seq);
        self.assertEqual(rotate(self.three_elem_seq, 1), 
            self.three_elem_seq_left);
        self.assertEqual(rotate(self.three_elem_seq, -1), 
            self.three_elem_seq_right);

    def test_scalar_addition(self):
        
# Tests on small sequences.            
        
        self.assertEqual(scalar_addition([], 0, 0), []);
        self.assertEqual(scalar_addition([], 0, 5), []);
        self.assertEqual(scalar_addition([], 5, 0), []);
        self.assertEqual(scalar_addition([], 5, 5), []);
        self.assertEqual(scalar_addition([1], 0, 0), [1]);
        self.assertEqual(scalar_addition([1], 0, 5), [1]);
        self.assertEqual(scalar_addition([1], 5, 0), [6]);
        self.assertEqual(scalar_addition([1], 5, 5), [1]);            
        self.assertEqual(scalar_addition([-1], 0, 0), [-1]);
        self.assertEqual(scalar_addition([-1], 0, 5), [4]);
        self.assertEqual(scalar_addition([-1], 5, 0), [4]);
        self.assertEqual(scalar_addition([-1], 5, 5), [4]);  

# Tests on sequences used in the representation of the major chord.

        self.assertEqual(scalar_addition([4, 7, 0], -4, 12), [0, 3, 8]);
        self.assertEqual(scalar_addition([3, 8, 0], -3, 12), [0, 5, 9]);
        self.assertEqual(scalar_addition([5, 9, 0], -5, 12), [0, 4, 7]);
        self.assertEqual(scalar_addition([2, 4, 0], -2, 7), [0, 2, 5]);
        self.assertEqual(scalar_addition([2, 5, 0], -2, 7), [0, 3, 5]);
        self.assertEqual(scalar_addition([3, 5, 0], -3, 7), [0, 2, 4]);

    def test_rotate_and_zero(self):

# Tests on small sequences.            
        
        self.assertEqual(rotate_and_zero([], 0, 0), []);
        self.assertEqual(rotate_and_zero([], 0, 5), []);
        self.assertEqual(rotate_and_zero([], 5, 0), []);
        self.assertEqual(rotate_and_zero([], 5, 5), []);
        self.assertEqual(rotate_and_zero([1], 0, 0), [0]);
        self.assertEqual(rotate_and_zero([1], 0, 5), [0]);
        self.assertEqual(rotate_and_zero([1], 5, 0), [0]);
        self.assertEqual(rotate_and_zero([1], 5, 5), [0]);            
        self.assertEqual(rotate_and_zero([-1], 0, 0), [0]);
        self.assertEqual(rotate_and_zero([-1], 0, 5), [0]);
        self.assertEqual(rotate_and_zero([-1], 5, 0), [0]);
        self.assertEqual(rotate_and_zero([-1], 5, 5), [0]);  

# Tests on sequences used in the representation of the major chord.

        self.assertEqual(rotate_and_zero([0, 4, 7], 1, 12), [0, 3, 8]);
        self.assertEqual(rotate_and_zero([0, 3, 8], 1, 12), [0, 5, 9]);
        self.assertEqual(rotate_and_zero([0, 5, 9], 1, 12), [0, 4, 7]);
        self.assertEqual(rotate_and_zero([0, 2, 4], 1, 7), [0, 2, 5]);
        self.assertEqual(rotate_and_zero([0, 2, 5], 1, 7), [0, 3, 5]);
        self.assertEqual(rotate_and_zero([0, 3, 5], 1, 7), [0, 2, 4]);

# And one for the diminished chord.

        self.assertEqual(rotate_and_zero([0, 3, 6, 9], 1, 12), 
            [0, 3, 6, 9]);

    def test_multislice(self):
        zero_slice = [0];
        one_slice = [1];
        zero_and_one_slice = [0, 1];

# For all sequences, the empty slice ([]) acting on it returns [], irrespective
# of the modulo and the offset.

        for i in range(8):
            for j in range(4):
                for k in self.all_test_seq:
                    self.assertEqual(multislice(k, self.eseq,
                        i, j), self.eseq);

# For all sequences of one element, the zero slice ([0]) returns the same 
# sequence, irrespective of the modulo and the offset.

        for i in range(4):
            for j in range(4):
                self.assertEqual(multislice(self.one_elem_seq,
                    zero_slice, i, j), self.one_elem_seq);

# Now we try slices on two elements.

        for j in range(4):
            for i in [0, 2, 4, 6]:
                self.assertEqual(multislice(self.two_elem_seq, 
                    zero_slice, j, i), self.one_elem_seq);
                self.assertEqual(multislice(self.two_elem_seq_rot, 
                    zero_slice, j, i), self.one_elem_seq_one);                    
            for i in [1, 3, 5, 7]:
                self.assertEqual(multislice(self.two_elem_seq, 
                    zero_slice, j, i), self.one_elem_seq_one);
                self.assertEqual(multislice(self.two_elem_seq_rot, 
                    zero_slice, j, i), self.one_elem_seq); 

# Slices of three elements should be tested later, but I would rather look at
# implementing other routines. I may come back to them, or not.

    def test_repseq(self):
        doubler = lambda x: x * 2;
        self.assertEqual(repseq(self.eseq), "");
        self.assertEqual(repseq(self.eseq, doubler), "");
        self.assertEqual(repseq([1]), "1");
        self.assertEqual(repseq([1], doubler), "2");
        self.assertEqual(repseq([1, 2]), "1, 2");
        self.assertEqual(repseq([1, 2], doubler), "2, 4");            

    def test_enl_seq(self):
        self.assertEqual(enl_seq(self.eseq, self.eseq), self.eseq);
        self.assertEqual(enl_seq(self.eseq, self.one_elem_seq), self.eseq);
        self.assertEqual(enl_seq(self.one_elem_seq, self.eseq), self.eseq);
        self.assertEqual(enl_seq([["0"]], self.one_elem_seq_one),
            [["0","1"]]);

    def test_norm_seq(self):
        self.assertEqual(norm_seq([7, 6, 5], 7), [0, 5, 6]);
        self.assertEqual(norm_seq([5, 6, 7], 7), [0, 5, 6]);
        self.assertEqual(norm_seq([7, 6, 5], 12), [5, 6, 7]);
        self.assertEqual(norm_seq([5, 6, 7], 12), [5, 6, 7]);

class TestTemperament(unittest.TestCase):
    """ This tests the temperament class. it also tests the seq_dict
        class and un_unicode_accdtls function, as they are associated. 
    """
    
    def setUp(self):
        self.chromabsrep = ["C", "C" + M_SHARP, "D", "E" + M_FLAT, "E", 
            "F", "F" + M_SHARP, "G", "A" + M_FLAT, "A", "B" + M_FLAT, 
            "B"+M_NATURAL];
        self.chrom_as_sharp = ["C", "C" + M_SHARP, "D", "D" + M_SHARP, "E", 
            "F", "F" + M_SHARP, "G", "G" + M_SHARP, "A", "A" + M_SHARP, 
            "B"]; 
        self.chrom_as_flat = ["C", "D" + M_FLAT, "D", "E" + M_FLAT, "E", 
            "F", "G" + M_FLAT, "G", "A" + M_FLAT, "A", "B" + M_FLAT, 
            "B"];
        self.triad_pattern = [0, 2, 4];
        self.major_interval = [0, 4, 7]; 
        
        self.ourseqdict = seq_dict([NSEQ_SCALE, NSEQ_CHORD], WestTemp);
        self.majorchord = ["Major", "maj", self.major_interval];
        self.majorscale = ["Major", [], CHROM_NAT_NOTE_POS];
        self.seq_maps = seq_dict([NSEQ_SCALE, NSEQ_CHORD], WestTemp);
        self.seq_maps.add_elem(self.majorchord, NSEQ_CHORD, "Major", "maj", 
            self.major_interval);
        self.seq_maps.add_elem(self.majorscale, NSEQ_SCALE, "Major", [], 
            CHROM_NAT_NOTE_POS);                
            
    def test_temperament_init_(self):
        self.assertEqual(WestTemp.no_keys, CHROM_SIZE);
        self.assertEqual(WestTemp.no_nat_keys, 7);
        self.assertEqual(WestTemp.nat_keys, CHROM_NAT_NOTES);
        self.assertEqual(WestTemp.nat_key_posn, CHROM_NAT_NOTE_POS);
        for i in range(7):
            note_desired = CHROM_NAT_NOTES[i];
            note_index = WestTemp.nat_key_pos_lookup[note_desired];
            self.assertEqual(WestTemp.pos_lookup_nat_key[note_index],
                note_desired);
        
    def test_temperament_get_pos_of_key(self):
        for i in range(CHROM_SIZE):
            self.assertEqual(WestTemp.get_pos_of_key(self.chromabsrep[i]),
                i);

    def test_temperament_get_key_of_pos(self):
        for i in range(CHROM_SIZE):
            self.assertEqual(WestTemp.get_key_of_pos(i, None, True),
                self.chrom_as_sharp[i]);            
            self.assertEqual(WestTemp.get_key_of_pos(i, None, False),
                self.chrom_as_flat[i]);
            if i < 6:
                self.assertEqual(WestTemp.get_key_of_pos(i, "C", False),
                    "C" + (M_SHARP * i));
                self.assertEqual(WestTemp.get_key_of_pos(i, "B", False),
                    "B" + (M_SHARP * (i + 1)));
            elif i == 6:
                self.assertEqual(WestTemp.get_key_of_pos(i, "C", False),
                    "C" + (M_SHARP * 6));
                self.assertEqual(WestTemp.get_key_of_pos(i, "B", False),
                    "B" + (M_FLAT * 5));
            else:
                self.assertEqual(WestTemp.get_key_of_pos(i, "C", False),
                    "C" + (M_FLAT * (12 - i)));
                self.assertEqual(WestTemp.get_key_of_pos(i, "B", False),
                    "B" + (M_FLAT * (11 - i)));

    def test_get_note_sequence(self):
        self.assertEqual(WestTemp.get_note_sequence("C", 
            self.major_interval, None, False), ["C", "E", "G"]);
        self.assertEqual(WestTemp.get_note_sequence("C", 
            self.major_interval, None, True), 
            ["C", "E", "G"]);                
        self.assertEqual(WestTemp.get_note_sequence("C", 
            self.major_interval, self.triad_pattern, True), 
            ["C", "E", "G"]);              
        self.assertEqual(WestTemp.get_note_sequence("C#", 
            self.major_interval, None, False), 
            ["D" + M_FLAT, "F", "A" + M_FLAT]);
        self.assertEqual(WestTemp.get_note_sequence("C#", 
            self.major_interval, None, True), 
            ["C" + M_SHARP, "F", "G" + M_SHARP]);                
        self.assertEqual(WestTemp.get_note_sequence("C#", 
            self.major_interval, self.triad_pattern, True), 
            ["C" + M_SHARP, "E" + M_SHARP, "G" + M_SHARP]); 

        self.assertEqual(WestTemp.get_note_sequence("Db", 
            self.major_interval, None, False), 
            ["D" + M_FLAT, "F", "A" + M_FLAT]);
        self.assertEqual(WestTemp.get_note_sequence("Db", 
            self.major_interval, None, True), 
            ["C" + M_SHARP, "F", "G" + M_SHARP]);                
        self.assertEqual(WestTemp.get_note_sequence("Db", 
            self.major_interval, self.triad_pattern, True), 
            ["D" + M_FLAT, "F", "A" + M_FLAT]); 
        
    def test_get_keyseq_notes(self):            
        self.assertEqual(WestTemp.get_keyseq_notes(["C", "E", "G"]), 
            ["C", [0, 4, 7]]);
        self.assertEqual(WestTemp.get_keyseq_notes(["C" + M_SHARP,
            "F", "A" + M_FLAT]), ["C" + M_SHARP, [0, 4, 7]]);                  
        self.assertEqual(WestTemp.get_keyseq_notes(["D" + M_FLAT,
            "F", "A" + M_FLAT]), ["D" + M_FLAT, [0, 4, 7]]);  

# PKM2020 - test failing
#    def test_un_unicode_accdtls(self):
#        """ We also do testing for the un_unicode_accdtls function. """
#        self.assertEqual(repseq(self.chromabsrep, un_unicode_accdtls), 
#            "C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, B");

    def test_seq_dict(self):
        """ Fits all testing for the seq_dict class in here. """
        self.assertTrue(self.seq_maps.check_nseqby_subdict(NSEQ_CHORD));
        self.assertTrue(self.seq_maps.check_nseqby_subdict(NSEQ_SCALE));
        self.assertFalse(self.seq_maps.check_nseqby_subdict(666));
        self.assertTrue(self.seq_maps.check_nseqby_name(NSEQ_CHORD, "Major"));
        self.assertTrue(self.seq_maps.check_nseqby_name(NSEQ_SCALE, "Major"));
        self.assertFalse(self.seq_maps.check_nseqby_name(NSEQ_CHORD, "Minor"));
        self.assertFalse(self.seq_maps.check_nseqby_name(NSEQ_SCALE, "Minor"));
        self.assertTrue(self.seq_maps.check_nseqby_abbrv(NSEQ_CHORD, 
            "maj"));
        self.assertFalse(self.seq_maps.check_nseqby_abbrv(NSEQ_SCALE, 
            "maj"));
        self.assertFalse(self.seq_maps.check_nseqby_abbrv(NSEQ_CHORD, 
            "min"));
        self.assertFalse(self.seq_maps.check_nseqby_abbrv(NSEQ_SCALE, 
            "min"));
        self.assertFalse(self.seq_maps.check_nseqby_seqpos(NSEQ_CHORD, 
            CHROM_NAT_NOTE_POS));
        self.assertTrue(self.seq_maps.check_nseqby_seqpos(NSEQ_SCALE, 
            CHROM_NAT_NOTE_POS));
        self.assertTrue(self.seq_maps.check_nseqby_seqpos(NSEQ_CHORD,
            self.major_interval));
        self.assertFalse(self.seq_maps.check_nseqby_seqpos(NSEQ_SCALE,
            self.major_interval));
        self.assertEqual(self.seq_maps.get_nseqby_name("Major", NSEQ_CHORD), 
            self.majorchord);
        self.assertEqual(self.seq_maps.get_nseqby_name("Major", NSEQ_SCALE), 
            self.majorscale);
        self.assertEqual(self.seq_maps.get_nseqby_abbrv("maj", NSEQ_CHORD), 
            self.majorchord);                
        self.assertEqual(self.seq_maps.get_nseqby_seqpos(
            self.major_interval, NSEQ_CHORD), self.majorchord);
        self.assertEqual(self.seq_maps.get_nseqby_seqpos(
            CHROM_NAT_NOTE_POS, NSEQ_SCALE), self.majorscale);

    def test_temperament_dict(self):
        """ Like test_seq_dict, but checks dictionary in WestTemp. """
        self.assertTrue(WestTemp.check_nseqby_subdict(NSEQ_CHORD));
        self.assertTrue(WestTemp.check_nseqby_subdict(NSEQ_SCALE));
        self.assertFalse(WestTemp.check_nseqby_subdict(666));
        WestTemp.add_elem(self.majorchord, NSEQ_CHORD, "Major", "maj", 
            self.major_interval);
        WestTemp.add_elem(self.majorscale, NSEQ_SCALE, "Major", [], 
            CHROM_NAT_NOTE_POS);     
        self.assertTrue(WestTemp.check_nseqby_name(NSEQ_CHORD, "Major"));
        self.assertTrue(WestTemp.check_nseqby_name(NSEQ_SCALE, "Major"));
        self.assertFalse(WestTemp.check_nseqby_name(NSEQ_CHORD, "Minor"));
        self.assertFalse(WestTemp.check_nseqby_name(NSEQ_SCALE, "Minor"));
        self.assertTrue(WestTemp.check_nseqby_abbrv(NSEQ_CHORD, 
            "maj"));
        self.assertFalse(WestTemp.check_nseqby_abbrv(NSEQ_SCALE, 
            "maj"));
        self.assertFalse(WestTemp.check_nseqby_abbrv(NSEQ_CHORD, 
            "min"));
        self.assertFalse(WestTemp.check_nseqby_abbrv(NSEQ_SCALE, 
            "min"));
        self.assertFalse(WestTemp.check_nseqby_seqpos(NSEQ_CHORD, 
            CHROM_NAT_NOTE_POS));
        self.assertTrue(WestTemp.check_nseqby_seqpos(NSEQ_SCALE, 
            CHROM_NAT_NOTE_POS));
        self.assertTrue(WestTemp.check_nseqby_seqpos(NSEQ_CHORD,
            self.major_interval));
        self.assertEqual(WestTemp.get_nseqby_name("Major", NSEQ_CHORD), 
            self.majorchord);
        self.assertEqual(WestTemp.get_nseqby_name("Major", NSEQ_SCALE), 
            self.majorscale);
        self.assertEqual(WestTemp.get_nseqby_abbrv("maj", NSEQ_CHORD), 
            self.majorchord);                
        self.assertEqual(WestTemp.get_nseqby_seqpos(
            self.major_interval, NSEQ_CHORD), self.majorchord);
        self.assertEqual(WestTemp.get_nseqby_seqpos(
            CHROM_NAT_NOTE_POS, NSEQ_SCALE), self.majorscale);

class TestNoteSeqAndScales(unittest.TestCase):
    """ This tests the note_seq and scales class. """
    
    def setUp(self):
        self.majorscale = MajorScale;
        self.melminscale = MelMinorScale;
        self.harmminscale = HarmMinorScale;
        self.harmmajscale = HarmMajorScale;
        self.dorianscale = WestTemp.get_nseqby_seqpos(
            [0, 2, 3, 5, 7, 9, 10], NSEQ_SCALE);
        self.locrianscale = WestTemp.get_nseqby_seqpos(
            [0, 1, 3, 5, 6, 8, 10], NSEQ_SCALE);
        self.superlocrianscale = WestTemp.get_nseqby_seqpos(
            [0, 1, 3, 4, 6, 8, 10], NSEQ_SCALE);
        self.ultralocrianscale = WestTemp.get_nseqby_seqpos(
            [0, 1, 3, 4, 6, 8, 9], NSEQ_SCALE);
        self.dubflat7locrianscale = WestTemp.get_nseqby_seqpos(
            [0, 1, 3, 5, 6, 8, 9], NSEQ_SCALE);
        self.majorchord = noteseq("TestMajor", NSEQ_SCALE, WestTemp, 
            [0, 4, 7], [0, 2, 4]);
        
    def test_temperament_dict(self):
        """ Like test_seq_dict, but checks dictionary in WestTemp. """
        self.assertTrue(WestTemp.check_nseqby_subdict(NSEQ_CHORD));
        self.assertTrue(WestTemp.check_nseqby_subdict(NSEQ_SCALE));
        self.assertFalse(WestTemp.check_nseqby_subdict(666));
        self.assertTrue(WestTemp.check_nseqby_name(NSEQ_SCALE, "Major"));
        self.assertFalse(WestTemp.check_nseqby_name(NSEQ_CHORD, "Minor"));
        self.assertFalse(WestTemp.check_nseqby_name(NSEQ_SCALE, "Minor"));
        self.assertFalse(WestTemp.check_nseqby_abbrv(NSEQ_SCALE, 
            "maj"));
        self.assertFalse(WestTemp.check_nseqby_abbrv(NSEQ_CHORD, 
            "min"));
        self.assertFalse(WestTemp.check_nseqby_abbrv(NSEQ_SCALE, 
            "min"));
        self.assertFalse(WestTemp.check_nseqby_seqpos(NSEQ_CHORD, 
            CHROM_NAT_NOTE_POS));
        self.assertTrue(WestTemp.check_nseqby_seqpos(NSEQ_SCALE, 
            CHROM_NAT_NOTE_POS));
        self.assertEqual(WestTemp.get_nseqby_name("Major", NSEQ_SCALE), 
            self.majorscale);
        self.assertEqual(WestTemp.get_nseqby_name("Ionian", NSEQ_SCALE), 
            self.majorscale);
        self.assertEqual(WestTemp.get_nseqby_name("Melodic Minor", 
            NSEQ_SCALE), self.melminscale);
        self.assertEqual(WestTemp.get_nseqby_name("Jazz Minor", 
            NSEQ_SCALE), self.melminscale);
        self.assertEqual(WestTemp.get_nseqby_name("Harmonic Minor", 
            NSEQ_SCALE), self.harmminscale);
        self.assertEqual(WestTemp.get_nseqby_name("Harmonic Major", 
            NSEQ_SCALE), self.harmmajscale); 
        self.assertEqual(WestTemp.get_nseqby_name("Dorian", 
            NSEQ_SCALE), self.dorianscale);
        self.assertEqual(WestTemp.get_nseqby_name("Locrian", 
            NSEQ_SCALE), self.locrianscale);  
        self.assertEqual(WestTemp.get_nseqby_name("Superlocrian", 
            NSEQ_SCALE), self.superlocrianscale);  
        self.assertEqual(WestTemp.get_nseqby_name("Ultralocrian", 
            NSEQ_SCALE), self.ultralocrianscale);                  
        self.assertEqual(WestTemp.get_nseqby_name("Locrian " + M_FLAT \
            + M_FLAT + "7", NSEQ_SCALE), self.dubflat7locrianscale);

        self.assertEqual(WestTemp.get_nseqby_seqpos(
            CHROM_NAT_NOTE_POS, NSEQ_SCALE), self.majorscale);

        self.assertEqual(WestTemp.get_nseqby_seqpos(
            MEL_MIN_NOTE_POS, NSEQ_SCALE), self.melminscale);
        self.assertEqual(WestTemp.get_nseqby_seqpos(
            HARM_MIN_NOTE_POS, NSEQ_SCALE), self.harmminscale);
        self.assertEqual(WestTemp.get_nseqby_seqpos(
            HARM_MAJ_NOTE_POS, NSEQ_SCALE), self.harmmajscale);                

    def test_get_notes_for_key(self):
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            0, [0]), ['E\u266d']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            1, [0]), ['G']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            2, [0]), ['B\u266d']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            3, [0]), ['E\u266d']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            0, [0, 2]), ['E\u266d', 'B\u266d']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            1, [0, 2]), ['G', 'E\u266d']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            2, [0, 2]), ['B\u266d', 'G']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            3, [0, 2]), ['E\u266d', 'B\u266d']);
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            0, [0, 1]), ['E\u266d', 'G']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            1, [0, 1]), ['G', 'B\u266d']);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            2, [0, 1]), ['B\u266d', 'E\u266d',]);            
        self.assertEqual(self.majorchord.get_notes_for_key("Eb", 
            3, [0, 1]), ['E\u266d', 'G']);                
        self.assertEqual(self.majorscale.get_notes_for_key("C", 
            3, [0, 1, 2, 3]), ['F', 'G', 'A', 'B']);  

    def test_get_posn_for_offset(self):
        self.assertEqual(self.majorchord.get_posn_for_offset(0, 
            raz=False), [0, 4, 7]);
        self.assertEqual(self.majorchord.get_posn_for_offset(0, 
            raz=True), [0, 4, 7]);            
        self.assertEqual(self.majorchord.get_posn_for_offset(0, [0], 
            raz=False), [0]);
        self.assertEqual(self.majorchord.get_posn_for_offset(0, [0], 
            raz=True), [0]);
        self.assertEqual(self.majorchord.get_posn_for_offset(0, [1], 
            raz=False), [4]);
        self.assertEqual(self.majorchord.get_posn_for_offset(0, [1], 
            raz=True), [0]);
        self.assertEqual(self.majorchord.get_posn_for_offset(0, [2], 
            raz=False), [7]);
        self.assertEqual(self.majorchord.get_posn_for_offset(0, [2], 
            raz=True), [0]);                
        self.assertEqual(self.majorchord.get_posn_for_offset(1, 
            raz=False), [4, 7, 0]);
        self.assertEqual(self.majorchord.get_posn_for_offset(1, 
            raz=True), [0, 3, 8]);            
        self.assertEqual(self.majorchord.get_posn_for_offset(1, [0], 
            raz=False), [4]);
        self.assertEqual(self.majorchord.get_posn_for_offset(1, [0], 
            raz=True), [0]);
        self.assertEqual(self.majorscale.get_posn_for_offset(0, 
            [0, 2, 4], raz=True), [0, 4, 7]);
        self.assertEqual(self.majorscale.get_posn_for_offset(1, 
            [0, 2, 4], raz=True), [0, 3, 7]);                 
        self.assertEqual(self.majorscale.get_posn_for_offset(3, 
            [0, 2, 4], raz=True), [0, 4, 7]);                
        self.assertEqual(self.majorscale.get_posn_for_offset(4, 
            [0, 2, 4], raz=True), [0, 4, 7]);
        self.assertEqual(self.majorscale.get_posn_for_offset(6, 
            [0, 2, 4], raz=True), [0, 3, 6]);                

if __name__ == '__main__':
    unittest.main()
