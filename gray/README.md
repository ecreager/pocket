# gray
### Introduction
We use gray codes to design mappings from x-y coordinates to note space.
The goal is to make a music interface that enables a MIDI controller or mousepad to control musical notes in an interesting way.
To this end, we seek mappings that are smooth in following sense: nearby entries in x-y space should have small Hamming distances in the note space, i.e. you don't have to flip many bits (or turn notes on/off) to get between them.

### Gray codes
A [Gray code](https://en.wikipedia.org/wiki/Gray_code) encodes the integers as binary vectors such that adjacent numbers share all but one bit in their code words.
There are many such encodings.
Frank Gray invented the first Gray code in 1947 and called it the Reflected Binary Code (RBC).

base 10 | base 2 | Reflected Binary Code |
------- | ------ | --------------------- |
0 | 000 | 000
1 | 001 | 001
2 | 010 | 011
3 | 011 | 010
4 | 100 | 110
5 | 101 | 111
6 | 110 | 101
7 | 111 | 100

We can see the problem with standard binary encoding by considering what happens in hardware during the transition from 1 to 2.
This transition comprises two bit flips, which are likely to occur at slightly different times.
So we will pass through another word in the code (either 0 or 3) on our way from 1 to 2.
The RBC solves this problem by ensuring that each word in the code is a single bit flip away from its neighbors.

### Code words specify the active notes
In the max patches, the binary code words represent whether each note in a set of valid notes is on or off.
E.g., assuming the four-note valid set: {C5, E5, G5, C6}, the code word 0111 (7 in base ten) represents the chord E5-G5-C6, a C major chord in first inversion.

### 2-D gray codes
We extend Gray codes to map pairs of integers onto binary code words.
Given tuples of two integers like _(x, y)_, the 2-D Gray code finds a binary encoding such that neighboring positions in x-y space (e.g., _(x, y) and (x+1, y)_) share all but one bit in their code words.

### Max/MSP patches
* `2d.maxpat`
 * maps x-y space (quantized to an 8-by-8 square) onto 7-bit binary vectors according to a 2-D Gray code.
 * The binary code words control whether each note in a configurable seven-note set is on or off.
 * Use the patch to explore different chords and chord voicings.
* `independent_stereo.maxpat`
 * x- and y-axes are mapped to note activity by  independent gray codes.
 * Each axis has a different set of notes and is assigned to a different stereo channel.

### python scripts
* `write_gray_code_1d.py`
 * Finds a 1-D Gray code solution and writes it to disk for interpretation by the max patch. `independent_stereo.maxpat`
* `write_gray_code_2d.py`
 * Finds a 2-D Gray code solution and writes it to disk for interpretation by the max patch `2d.maxpat`.
 * You can solve for codes of different code length (_n_) and word length (_m_), but only _n=8_ and _m=7_  is supported by the max patches.
