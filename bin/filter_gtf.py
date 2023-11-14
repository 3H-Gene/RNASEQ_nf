#!/usr/bin/env python
from __future__ import print_function
import logging
from itertools import groupby
import argparse
import re

# Create a logger
logging.basicConfig(format="%(name)s - %(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

def is_header(line: str) -> bool:
    """Returns True if the given line is a header line in a FASTA file."""
    return line[0] == ">"


def extract_fasta_seq_names(fasta_name: str) -> set:
    """Extracts the sequence names from a FASTA file.

    modified from Brent Pedersen
    Correct Way To Parse A Fasta File In Python
    given a fasta file. yield tuples of header, sequence
    from https://www.biostars.org/p/710/

    Args:
      fasta_name: The path to the FASTA file.

    Returns:
      A set of the sequence names in the FASTA file.
    """
    seqnames = set()
    with open(fasta_name) as fasta:
        for line in fasta:
            if line[0] == ">":
                seqnames.add(line[1:].split(None, 1)[0])
    return seqnames


def extract_genes_in_genome(fasta: str, gtf_in: str, gtf_out: str) -> None:
    """Extracts the genes in the genome from a GTF file.

    Args:
      fasta: The path to the FASTA file.
      gtf_in: The path to the input GTF file.
      gtf_out: The path to the output GTF file.

    Raises:
      ValueError: If no overlap is found or if the GTF file is not tab delimited.
    """

    def tab_delimited(file) -> float:
    
        import statistics. # put to the top

        with open(file, "r") as f:
            data = f.read(1024)
            lines = data.split("\n")
            # most lines should have 9 tab-separated columns
            return statistics.median([line.count("\t") for line in lines])

    num_sep = tab_delimited(gtf_in)
    if num_sep != 8:
        raise ValueError("No valid tab-delimited GTF file.")

    seq_names_in_genome = extract_fasta_seq_names(fasta)
    logger.info(f"Extracted chromosome sequence names from {fasta}")
    logger.debug("All chromosome names: " + ", ".join(sorted(seq_names_in_genome)))

    with open(gtf_in) as gtf, open(gtf_out, "w") as out:
        seq_names_in_gtf = {line.split("\t")[0] for line in gtf if line.strip()}
        overlap = seq_names_in_genome & seq_names_in_gtf
        if not overlap:
            raise ValueError("No overlapping scaffolds found.")

        gtf.seek(0)  # Reset file pointer to the start of the file
        for line in gtf:
            if line.split("\t")[0] in overlap:
                out.write(line)

    logger.info(f"Extracted {len(overlap)} matching sequences from {gtf_in} into {gtf_out}")
    logger.debug("All sequence IDs from GTF: " + ", ".join(sorted(seq_names_in_gtf)))
    logger.info(f"Wrote matching lines to {gtf_out}")


def remove_features_without_transcript_id(gtf_in: str, gtf_out: str) -> None:
    """
    Removes gene rows with absent or empty transcript_id attributes from a GTF file.

    Args:
      gtf_in: Path to the input GTF file.
      gtf_out: The path to the output GTF file.
    """

    with open(gtf_in, "r") as f_in, open(gtf_out, "w") as f_out:
        for line in f_in:
            transcript_id_match = re.search(r'transcript_id "([^"]+)"', line)
            if transcript_id_match:
                f_out.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Filter GTF for various reasons""")
    parser.add_argument("--gtf", type=str, help="GTF file")
    parser.add_argument("--fasta", type=str, help="Genome fasta file")
    parser.add_argument(
        "-p",
        "--prefix",
        dest="prefix",
        default="genes",
        type=str,
        help="Prefix for output GTF files",
    )

    args = parser.parse_args()
    extract_genes_in_genome(args.fasta, args.gtf, args.prefix + "_in_genome.gtf")
    remove_features_without_transcript_id(args.prefix + "_in_genome.gtf", args.prefix + "_with_transcript_ids.gtf")
