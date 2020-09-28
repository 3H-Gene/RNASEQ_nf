# ![nf-core/rnaseq](docs/images/nf-core-rnaseq_logo.png)

[![Nextflow](https://img.shields.io/badge/nextflow-%E2%89%A520.07.1-brightgreen.svg)](https://www.nextflow.io/)
[![Nextflow DSL2](https://img.shields.io/badge/nextflow-DSL2-brightgreen.svg)](https://www.nextflow.io/docs/latest/dsl2.html)
[![GitHub Actions CI Status](https://github.com/nf-core/rnaseq/workflows/nf-core%20CI/badge.svg)](https://github.com/nf-core/rnaseq/actions)
[![GitHub Actions Linting Status](https://github.com/nf-core/rnaseq/workflows/nf-core%20linting/badge.svg)](https://github.com/nf-core/rnaseq/actions)

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](https://bioconda.github.io/)
[![Docker](https://img.shields.io/docker/automated/nfcore/rnaseq.svg)](https://hub.docker.com/r/nfcore/rnaseq)
[![Get help on Slack](http://img.shields.io/badge/slack-nf--core%20%23rnaseq-4A154B?logo=slack)](https://nfcore.slack.com/channels/rnaseq)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1400710.svg)](https://doi.org/10.5281/zenodo.1400710)

## Introduction

**nf-core/rnaseq** is a bioinformatics analysis pipeline used for RNA sequencing data.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It comes with docker containers making installation trivial and results highly reproducible.

## Pipeline summary

1. Merge re-sequenced FastQ files ([`cat`](http://www.linfo.org/cat.html); *if required*)
2. Read QC ([`FastQC`](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/))
3. UMI extraction ([`umi_tools`](https://github.com/CGATOxford/UMI-tools))
4. Adapter and quality trimming ([`Trim Galore!`](https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/))
5. Removal of ribosomal RNA ([`SortMeRNA`](https://github.com/biocore/sortmerna))
6. Choice of multiple alignment and quantification routes:
    1. [`STAR`](https://github.com/alexdobin/STAR) -> [`featureCounts`](http://bioinf.wehi.edu.au/featureCounts/)
    2. [`STAR`](https://github.com/alexdobin/STAR) -> [`RSEM`](https://github.com/deweylab/RSEM)
    3. [`HiSAT2`](https://ccb.jhu.edu/software/hisat2/index.shtml) -> [`featureCounts`](http://bioinf.wehi.edu.au/featureCounts/)
    4. [`Salmon`](https://combine-lab.github.io/salmon/)
7. Sort and index alignments ([`SAMtools`](https://sourceforge.net/projects/samtools/files/samtools/))
8. UMI-based deduplication ([`umi_tools`](https://github.com/CGATOxford/UMI-tools))
9. Duplicate read marking ([`picard MarkDuplicates`](https://broadinstitute.github.io/picard/))
10. Assembly and transcript quantification ([`StringTie`](https://ccb.jhu.edu/software/stringtie/))
11. Extensive quality control:
    1. [`RSeQC`](http://rseqc.sourceforge.net/)
    2. [`Qualimap`](http://qualimap.bioinfo.cipf.es/)
    3. [`dupRadar`](https://bioconductor.org/packages/release/bioc/html/dupRadar.html)
    4. [`Preseq`](http://smithlabresearch.org/software/preseq/)
    5. [`edgeR`](https://bioconductor.org/packages/release/bioc/html/edgeR.html)
12. Present QC for raw read, alignment, gene biotype, sample similarity, and strand-specificity checks ([`MultiQC`](http://multiqc.info/), [`R`](https://www.r-project.org/))

## Quick Start

1. Install [`nextflow`](https://nf-co.re/usage/installation)

2. Install either [`Docker`](https://docs.docker.com/engine/installation/) or [`Singularity`](https://www.sylabs.io/guides/3.0/user-guide/) for full pipeline reproducibility _(please only use [`Conda`](https://conda.io/miniconda.html) as a last resort; see [docs](https://nf-co.re/usage/configuration#basic-configuration-profiles). Note: This pipeline does not currently support running with Conda on macOS because the latest version of the `sortmerna` package is not available for this platform.)_

3. Download the pipeline and test it on a minimal dataset with a single command:

    ```bash
    nextflow run nf-core/rnaseq -profile test,<docker/singularity/conda/institute>
    ```

    > Please check [nf-core/configs](https://github.com/nf-core/configs#documentation) to see if a custom config file to run nf-core pipelines already exists for your Institute. If so, you can simply use `-profile <institute>` in your command. This will enable either `docker` or `singularity` and set the appropriate execution settings for your local compute environment.

4. Start running your own analysis!

    ```bash
    nextflow run nf-core/rnaseq -profile <docker/singularity/conda/institute> --input samplesheet.csv --genome GRCh37
    ```

See [usage docs](https://nf-co.re/rnaseq/usage) for all of the available options when running the pipeline.

### Documentation

The nf-core/rnaseq pipeline comes with documentation about the pipeline which you can read on the [nf-core website](https://nf-co.re/rnaseq) or find in the [`docs/` directory](docs).

### Credits

These scripts were originally written for use at the [National Genomics Infrastructure](https://ngisweden.scilifelab.se), part of [SciLifeLab](http://www.scilifelab.se/) in Stockholm, Sweden, by Phil Ewels ([@ewels](https://github.com/ewels)) and Rickard Hammarén ([@Hammarn](https://github.com/Hammarn)).

The pipeline was re-written in Nextflow DSL2 by Harshil Patel ([@drpatelh](https://github.com/drpatelh)) from [The Bioinformatics & Biostatistics Group](https://www.crick.ac.uk/research/science-technology-platforms/bioinformatics-and-biostatistics/) at [The Francis Crick Institute](https://www.crick.ac.uk/), London.

Many thanks to other who have helped out along the way too, including (but not limited to):
[@Galithil](https://github.com/Galithil),
[@pditommaso](https://github.com/pditommaso),
[@orzechoj](https://github.com/orzechoj),
[@apeltzer](https://github.com/apeltzer),
[@colindaven](https://github.com/colindaven),
[@lpantano](https://github.com/lpantano),
[@olgabot](https://github.com/olgabot),
[@jburos](https://github.com/jburos).

## Contributions and Support

If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).

For further information or help, don't hesitate to get in touch on the [Slack `#rnaseq` channel](https://nfcore.slack.com/channels/rnaseq) (you can join with [this invite](https://nf-co.re/join/slack)).

## Citation

If you use  nf-core/rnaseq for your analysis, please cite it using the following doi: [10.5281/zenodo.1400710](https://doi.org/10.5281/zenodo.1400710)

An extensive list of references for the tools used by the pipeline can be found in the [`CITATIONS.md`](CITATIONS.md) file.

You can cite the `nf-core` publication as follows:

> **The nf-core framework for community-curated bioinformatics pipelines.**
>
> Philip Ewels, Alexander Peltzer, Sven Fillinger, Harshil Patel, Johannes Alneberg, Andreas Wilm, Maxime Ulysse Garcia, Paolo Di Tommaso & Sven Nahnsen.
>
> _Nat Biotechnol._ 2020 Feb 13. doi: [10.1038/s41587-020-0439-x](https://dx.doi.org/10.1038/s41587-020-0439-x).
> ReadCube: [Full Access Link](https://rdcu.be/b1GjZ)
