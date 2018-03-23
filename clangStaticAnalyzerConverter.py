#!/usr/bin/python

import argparse
import json
import plistlib
import sys
from sarif import sarif
import os
import mimetypes
import hashlib

def gen_uri(filename, args):
    if args.project_dir:
        path = os.path.normpath(str(args.project_dir) + "/" + filename)
    else:
        path = os.path.normpath(filename)
    return path

def gen_tool(plistInput):
    tool = sarif.tool()
    tool.name = "clang static analyzer"
    tool.fullName = plistInput["clang_version"]
    tool.language = "en"
    tool.version = plistInput["clang_version"]
    return tool

def gen_codeFlow(plistPath, plistFiles, args):
    codeFlow = sarif.codeFlow()
    codeFlow.locations = []
    step = 1
    for point in plistPath:
        if "edges" in point:
            if args.encode_edges:
                for edge in point["edges"]:
                    for arrow in ["start", "end"]:
                        startPlistRange = edge[arrow]
                        gen_region_from_ranges([startPlistRange])
                        annotatedCodeLocation = sarif.annotatedCodeLocation()
                        physicalLocation = sarif.physicalLocation()
                        annotatedCodeLocation.physicalLocation = physicalLocation
                        physicalLocation.uri = gen_uri(plistFiles[edge[arrow][0]["file"]], args)
                        physicalLocation.region = gen_region_from_ranges([startPlistRange])
                        annotatedCodeLocation.message = "edge " + arrow
                        annotatedCodeLocation.richMessage = "edge " + arrow
                        codeFlow.locations.append(annotatedCodeLocation)
        else:
            annotatedCodeLocation = sarif.annotatedCodeLocation()
            physicalLocation = sarif.physicalLocation()
            annotatedCodeLocation.physicalLocation = physicalLocation
            physicalLocation.uri = gen_uri(plistFiles[point["location"]["file"]], args)
            physicalLocation.region = gen_region(point["location"])
            if "ranges" in point:
                # refine region by looking at the ranges instead of location
                physicalLocation.region = gen_region_from_ranges(point["ranges"])
            annotatedCodeLocation.step = step
            step = step+1
            annotatedCodeLocation.message = point["message"]
            annotatedCodeLocation.richMessage = point["extended_message"]
            codeFlow.locations.append(annotatedCodeLocation)
    return codeFlow


def gen_result(plistDiagnostic, plistFiles, args):
    result = sarif.result()
    result.message = plistDiagnostic["description"]
    result.ruleId = plistDiagnostic["check_name"]
    if "location" in plistDiagnostic:
        region = gen_region(plistDiagnostic["location"])
        loc = sarif.location()
        result.locations = [loc]
        physicalLocation = sarif.physicalLocation()
        loc.resultFile = physicalLocation
        physicalLocation.region = region
        physicalLocation.uri = gen_uri(plistFiles[plistDiagnostic["location"]["file"]], args)
    if "path" in plistDiagnostic:
        codeFlow = gen_codeFlow(plistDiagnostic["path"], plistFiles, args)
        result.codeFlows = [codeFlow]
    return result

def gen_region_from_ranges(plistRanges):
    region = sarif.region()
    for plistRange in plistRanges:
        start = plistRange[0]
        end = plistRange[1]
        startLine = start["line"]
        startColumn = start["col"]
        endLine = end["line"]
        endColumn = end["col"]
        if not region.startLine or startLine < region.startLine:
            region.startLine = startLine
            region.startColumn = startColumn
        if startLine == region.startLine and startColumn < region.startColumn:
            region.startColumn = startColumn
        if not region.endLine or endLine > region.endLine:
            region.endLine = endLine
            region.endColumn = endColumn
        if endLine == region.endLine and endColumn > region.endColumn:
            region.endColumn = endColumn
    return region


def gen_region(plistLocation):
    region = sarif.region()
    region.startLine = plistLocation["line"]
    region.startColumn = plistLocation["col"]
    return region

def gen_location(loc):
    location = sarif.location()
    analysisTarget = sarif.physicalLocation()
    location.analysisTarget = analysisTarget

def populate_results(plistDiagnostics, plistFiles, sarifResults, args):
    for d in plistDiagnostics:
        result = gen_result(d, plistFiles, args)
        sarifResults.append(result)

def populate_files(plistFiles, sarifFiles, args):
    for f in plistFiles:
        sarifFile = sarif.file()
        sarifFile.uri = gen_uri(f, args)
        if os.path.isfile(sarifFile.uri):
            sarifFile.mimeType = mimetypes.guess_type(sarifFile.uri)[0]
            md5hash = sarif.hash()
            md5hash.value = hashlib.md5(open(sarifFile.uri,'rb').read()).hexdigest()
            md5hash.algorithm = "md5"
            sarifFile.hashes = [md5hash]
        sarifFiles[f] = sarifFile

def populateRun(plistMain, sarifRun, args):
    sarifRun.tool = gen_tool(plistMain)
    populate_results(plistMain["diagnostics"], plistMain["files"], sarifRun.results, args)
    populate_files(plistMain["files"], sarifRun.files, args)

def main(args):
    import glob
    plistFiles = glob.glob(args.clang_output_dir+"/*.plist")
    sarifLog = sarif.sarifLog()
    run = sarif.run()
    sarifLog.runs.append(run)
    run.files = {}
    run.results = []
    for plistFile in plistFiles:
        plistMain = plistlib.readPlist(plistFile)
        populateRun(plistMain, run, args)

    output = sarif.SarifEncoder(indent=4).encode(sarifLog)
    o = open(args.sarif_output, 'w')
    o.write(output)
    o.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("clang_output_dir", type=str,
                    help="directory that contains the plist files")
    parser.add_argument("sarif_output", type=str,
                    help="output")
    parser.add_argument("--project_dir", type=str,
                    help="project directory")
    parser.add_argument("--encode_edges", type=bool,
                    help="also encode clang edges in error traces")
    args = parser.parse_args()
    print args
    main(args)