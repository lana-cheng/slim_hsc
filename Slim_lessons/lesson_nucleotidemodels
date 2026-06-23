## Nucleotide Based Models

Properties:
- tracks nucleotides of every haplosome
- mutations have an associated nucleotide
- mutation rates are sequence dependent

**Initializing**

Declaring model: initializeSLiMOptions(nucleotideBased=T);

Setup ancestral sequence: initializeAncestralNucleotide();
- returns length of ancestral sequence

Ex: Chromosome length is 1e6
```
defineConstant("L", 1e6);
initializeAncestralNucleotides(randomNucleotides(L));
```

Eidos output:
```
# One string with nucleotides as letters
>randomNucleotides(10)
> randomNucleotides(10, format="string")

#Each nucleotide is a string in letters
> randomNucleotides(10, format="char")

#"A" is 0, "C" is 1, "G" is 2, and "T" is 3
> randomNucleotides(10, format="integer")
```

Mutation type (uses stacking): initializeMutationTypeNuc("m1", 0.5, "f", 0.0);
- tells slim that mutations should have nucleoties associated with it

Sequence based mutation matrix instead of universal mutation rate: initializeGenomicElementType("g1", m1, 1.0, mmJukesCantor(2.5e-6));
- Eidos:
  - Each row represents a possible nucleotide prior to mutation. Each column provides the corresponding mutation rates for the mutation of a given state to a new state: A, C, G, or T
  - For a mutating site that presently has a C in it (row 1), for example, the probabilities of mutating to an A, G, or T are all given as ~3.3e-8 (columns 0, 2, and 3). The probability of an “identity” mutation, of a nucleotide to itself, must conventionally be specified as zero, as it is here (the zero values along the matrix diagonal)
```
> mmJukesCantor(1e-7 / 3)
[,0] [,1] [,2] [,3]
[0,] 0 3.33333e-08 3.33333e-08 3.33333e-08
[1,] 3.33333e-08 0 3.33333e-08 3.33333e-08
[2,] 3.33333e-08 3.33333e-08 0 3.33333e-08
[3,] 3.33333e-08 3.33333e-08 3.33333e-08 0
```

**Running Model**

Ancestral sequence is updated/changed every time a mutation fixes. If convertToSubstitution=F, then ancestral sequence is not changed. 

Eidos
```
> sim.chromosome.ancestralNucleotides()
"TGTTATGCTGCTGTGGGTGAGTTGTGCTTATTCCATAACTTCACTTACAATGAGCCCATGGAGGTTAGCGGAA
TTGCGCCGGCATGAGCTTGTGAGGGTC"
```

To compare ancestralNucleotides() sequence above with initial ancestal sequence, add the following to the initialize callback
```
s = randomNucleotides(L);
print(s);
initializeAncestralNucleotides(s);
```

outputFixedMutations(): last entry is now the nucleotide associated with the mutation

**Mutations**

Eidos:
```
> sim.mutations.nucleotide
"G" "T" "T" "A" "T" "A" "C" "C" "C" "G" "G" "A"

> sim.substitutions.nucleotide
"T" "A" "C"

> sim.substitutions.position
31 82 62 78 92 56 48 7 35 79 51 10
```

**Codon and Amino Acid Sequences**

4* 4 *4=64 trinucleotide combinations to produce codons. Each codon has an integer ID [0,63]. 
```
> c = p1.haplosomes[0].nucleotides(0, 29, "codon")
> c
48 52 23 29 1 19 6 8 18 33

> codonsToAminoAcids(c)
"XSPLNHTRQD"

> codonsToAminoAcids(c, long=T)
"Ter-Ser-Pro-Leu-Asn-His-Thr-Arg-Gln-Asp"

> codonsToAminoAcids(c, long=T, paste=F)
"Ter" "Ser" "Pro" "Leu" "Asn" "His" "Thr" "Arg" "Gln" "Asp"
```

**Recipe 19.9**

Initializing:

Last line:
- match(x, table): takes each element in x and matches it against table. It returns a vector where an entry is the position number if a match was found, and -1 if no match was found. 
- the entries are converted to logical elements with <0 to only keep non-stop codons. 
```
defineConstant("TAA", nucleotidesToCodons("TAA"));
defineConstant("TAG", nucleotidesToCodons("TAG"));
defineConstant("TGA", nucleotidesToCodons("TGA"));
defineConstant("STOP", c(TAA, TAG, TGA));
defineConstant("NONSTOP", (0:63)[match(0:63, STOP) < 0]);
```

Setting up gene:
- sample() returns a vector of length 194 samples from NONSTOP with replacement
- seq1 is non coding region with random nucleotides
- seq2 takes the whole nonstop codons vector, converts it to nucleotides, and takes positions 0-417. Paste0 joins the elements into one string. This becomes the first part of an exon
- seq3 is an intron
- seq4 takes the remaining codons from the vector "codons" as the other part of the exon. 
- seq5 fills the remainder of the chromosome. 
```
codons = sample(NONSTOP, 194, replace=T);
seq1 = randomNucleotides(253);
seq2 = paste0(codonsToNucleotides(codons, format="char")[0:417]);
seq3 = randomNucleotides(200);
seq4 = paste0(codonsToNucleotides(codons, format="char")[418:581]);
seq5 = randomNucleotides(L-1035);
seq = seq1 + seq2 + seq3 + seq4 + seq5;
catn("Initial AA sequence: " + codonsToAminoAcids(codons));
```

**Fitness Effect**

In the following example, the individual has a fitness effect of 0.0 if a nonstop codon mutated into a stop codon in the exon regions. fitnessEffect() is called once per individual per tick

```
fitnessEffect() {
for (g in individual.haplosomes)
{
seq = g.nucleotides(253, 670) + g.nucleotides(871, 1034);
codons = nucleotidesToCodons(seq);
if (sum(match(codons, STOP) >= 0))
return 0.0;
}
return 1.0;
}

#OR same but amino acid version. "X" is built-in stop codon group

fitnessEffect() {
	for (g in individual.haplosomes)
	{
		seq = g.nucleotides(253, 670) + g.nucleotides(871, 1034);
		codons = nucleotidesToCodons(seq);
		aa=codonsToAminoAcids(codons);
		if (any(strcontains(aa, "X") == T))
			return 0.0;
	}
	
	return 1.0;
}
```

### **Working with files**

Setting up working directory: Press folder icon on right side and select folder

**Simulate neutral drift with empirical SNPs**
*Initializing*

initializeAncestralNucelotides(*fasta_name.fa*): loads FASTA file that contains the ancestral sequence for chromosome 22

m1 is a neutral mutation, and no new mutations are introduced because mmJukesCantor is set to 0. Genetic changes are due to initial SNPs only. 

```
initialize() {
initializeSLiMOptions(nucleotideBased=T);
length = initializeAncestralNucleotides("hs37d5_chr22_patched.fa");
defineConstant("L", length);
initializeMutationTypeNuc("m1", 0.5, "f", 0.0);
initializeGenomicElementType("g1", m1, 1.0, mmJukesCantor(0.0));
initializeGenomicElement(g1, 0, L-1);
initializeRecombinationRate(1e-8);
}
```

*Tick 1*

Add a population of size 99, which is the number of individuals in the VCF file

The VCF file, which contains SNP genotypic data, is read and stored into each individual's haplosomes. Those SNPs are of type m1 and overlays the ancestral sequence. Since humans are diploid, the VCF file for each person looks like ex: 0|1 for a SNP. 1 indicates that haplosome has the SNP. 

The population is expanded to 1000. For each new individual, its two haplosomes are drawn from the pool of haplosomes of the 99 individuals. 

```
1 late() {
sim.addSubpop("p1", 99);
p1.haplosomes.readHaplosomesFromVCF("chr22_filtered.recode.vcf", m1);
p1.setSubpopulationSize(1000);
}
```

*Storing Genomic Information*

final.vcf stores information on mutations that are still segregating and haven't reached fixation.

subs.csv stores information on mutations that have fixed. 

The final ancestral sequence (with fixations resulting from the simulation) can be stored as a FASTA file. 

```
1000 late() {
p1.haplosomes.outputHaplosomesToVCF("final.vcf");

subs = sim.substitutions;
lines = "position, nucleotide";
for (sub in subs)
lines = c(lines, sub.position + ", " + sub.nucleotide);
writeFile("subs.csv", lines);

seq = sim.chromosome.ancestralNucleotides();
writeFile("anc.fa", c(">final_ancestral_seq", seq));
}
```

**File Types**

VCF: chromosome, position, mutation nucleotide etc. Stores single nucleotide mutation information

Fasta: string of nucleotides. used to store ancestral sequence. 

CSV: position, nucleotide. used to store substitutions

