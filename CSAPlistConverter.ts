
import {Sarif, Run, Result, Rule, CodeFlow, AnnotatedCodeLocation, File, Location} from "./sarif/Sarif"
import * as path from 'path';
import Uri from "vscode-uri"
import * as fs from 'fs'
import * as mime from 'mime'
import * as md5 from 'md5';
import * as plist from "./types/plist"
import Converter from './Converter';
var plistParser = require('plist');


export default class CSAPlistConverter extends Converter {

    _project_path: string;
    _input: plist.PlistJson;
    _output: Sarif;

    _files: Map<string,File> = new Map<string,File>();

    constructor(input: string, project_path: string, computeMd5: boolean) {
        super(project_path, computeMd5);
        this._input = plistParser.parse(input);
    }

    public convert(outputFileName: string) {
        let run: Run = {
            tool: {
                name: this._input.clang_version,
                fullName: this._input.clang_version,
            },
            results: [],
            rules: {}
        };
        this._input.diagnostics.forEach(diagnostic => {
            // create the Rule object if it doesn't already exist
            if (!(diagnostic.check_name in run.rules)) {
                let rule : Rule = {
                    id: diagnostic.check_name,
                    name: diagnostic.check_name,
                    
                }
                run.rules[diagnostic.check_name] = rule;
            }
            // create the Result object
            let res : Result = {
                message: diagnostic.description,
                ruleId: diagnostic.check_name,
                codeFlows: [this.genCodeFlow(diagnostic.path)],
                locations: [{
                    resultFile: {
                        uri: this.getUri(this._input.files[diagnostic.location.file]),
                        region: this.genRegion(diagnostic.location)                    }
                }] 
            };
            run.results.push(res);
        });
        // adding files that appear in results
        run.files = {};
        this._files.forEach((file,name) => {
            run.files[name] = file;
        });

        this._output.runs.push(run);
        let stringOutput = JSON.stringify(this._output, null, 2);
        if (outputFileName) {
            fs.writeFileSync(outputFileName,stringOutput);
        } else {
            console.log(stringOutput);
        }
    }

    private genCodeFlow(trace: plist.PathStep[]): CodeFlow {
        let locations: AnnotatedCodeLocation[] = [];
        trace.forEach(pathstep => {
            if (pathstep.edges) {
                pathstep.edges.forEach(edge => {
                });
            } else {
                let step : AnnotatedCodeLocation = {};
                step.message = pathstep.message;
                step.physicalLocation = {
                    uri: this.getUri(this._input.files[pathstep.location.file]),
                    region: pathstep.ranges? this.genRegionFromRanges(pathstep.ranges) : this.genRegion(pathstep.location)
                };
                
                locations.push(step)
            }
        }); 
        return {
            locations: locations
        };
    }

    private genRegion(location: plist.Location): any {
        return {
            startLine: location.line,
            startcolumn: location.col
        };
    }

    private genRegionFromRanges(plistRanges: plist.Location[][]): any {
        let region : {
            startLine?: number,
            startColumn?: number,
            endLine?: number, 
            endColumn?: number
        } = {};
        plistRanges.forEach(range => {
            let start = range[0];
            let end = range[1];
            if (!region.startLine || start.line < region.startLine) {
                region.startLine = start.line;
                region.startColumn = start.col;
            }
            if (start.line == region.startLine && start.col < region.startColumn) {
                region.startColumn = start.col;
            }
            if (!region.endLine || end.line > region.endLine) {
                region.endLine = end.line
                region.endColumn = end.col
            }
            if (end.line == region.endLine && end.col > region.endColumn) {
                region.endColumn = end.col
            }
        });
        return region;
    }

    private getUri(file: string): string {
        let absolutePath = path.join(this._project_path,file);
        let uri = Uri.file(absolutePath);
        let stringUri = uri.toString();
        if (!(stringUri in this._files)) {
            this._files.set(stringUri,{
                uri: stringUri,
                mimeType: mime.getType(stringUri),
                hashes: this._computeMd5 ? [{
                    value: md5(fs.readFileSync(uri.fsPath)),
                    algorithm: 'md5'
                }]: undefined
            });
        }
        return stringUri;
    }
}