// Import generic module functions
include { initOptions; saveFiles; getSoftwareName } from './functions'

process GUNZIP {
    tag "$archive"
    publishDir "${params.outdir}",
        mode: params.publish_dir_mode,
        saveAs: { filename -> saveFiles(filename:filename, options:options, publish_dir:getSoftwareName(task.process), publish_id:'') }

    container "biocontainers/biocontainers:v1.2.0_cv1"
    //container  https://depot.galaxyproject.org/singularity/python:3.7.1

    //conda (params.conda ? "conda-forge::python=3.7.1" : null)

    input:
    path archive
    val  options

    output:
    path "$gunzip",       emit: gunzip
    path "*.version.txt", emit: version

    script:
    def software = getSoftwareName(task.process)
    def ioptions = initOptions(options)
    gunzip       = archive.toString() - '.gz'
    """
    gunzip --force $ioptions.args $archive
    echo \$(gunzip --version 2>&1) | sed 's/^.*(gzip) //; s/ Copyright.*\$//' > ${software}.version.txt
    """
}
