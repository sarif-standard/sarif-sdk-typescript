import {Sarif, Run, Result, Rule, CodeFlow, AnnotatedCodeLocation, File, Location} from "./sarif/Sarif"
import * as path from 'path';
import {report, json_trace_item} from "./types/infer";
import Uri from "vscode-uri";
import * as fs from 'fs';
import * as mime from 'mime';
import * as md5 from 'md5';
import Converter from './Converter';

export default class InferConverter extends Converter {

    _current_input: report;
    _output: Sarif;

    _files: Map<string,File> = new Map<string,File>();

    constructor(project_path: string, computeMd5: boolean) {
        super(project_path, computeMd5);
    }

    public convert(input: string): void {
        this._current_input = JSON.parse(input);
        this._files.clear();
        let run: Run = {
            tool: {
                name: "Infer",
            },
            results: [],
            rules: {}
        };
        this._output.runs.push(run);
        this._current_input.forEach(k => {
            // create the Rule object if it doesn't already exist
            if (!(k.bug_type in run.rules)) {
                let rule : Rule = {
                    id: k.bug_type,
                    name: k.bug_type_hum
                }
                run.rules[k.bug_type] = rule;
            }
            // create the Result object
            let res : Result = {
                message: k.qualifier,
                level: this.kindToLevel(k.kind),
                ruleKey: k.bug_type,
                codeFlows: [this.bugTraceToCodeFlow(k.bug_trace)],
                // there is a single location in an Infer report
                locations: [{ 
                    resultFile: {
                        uri: this.getUri(k.file),
                        region: {
                            startLine: k.line,
                            startColumn: k.column
                        }
                    }
                }]
            };
            run.results.push(res);
        });
        // adding files that appear in results
        run.files = {};
        this._files.forEach((file,name) => {
            run.files[name] = file;
        });
    }

    public generateOutput(outputFileName: string) {
        let stringOutput = JSON.stringify(this._output, null, 2);
        if (outputFileName) {
            fs.writeFileSync(outputFileName,stringOutput);
        } else {
            console.log(stringOutput);
        }
    }

    private kindToLevel(kind: string): "warning" | "error" {
        switch(kind) {
            case "ERROR":
                return "error";
            default:
                return "warning";
        }
    }

    private bugTraceToCodeFlow(trace: json_trace_item[]): CodeFlow {
        let codeFlow: CodeFlow = {
            locations: [] 
        };
        let curStep = 1;
        trace.forEach(item => {
            let loc: AnnotatedCodeLocation = {
                step: curStep++,
                message: item.description,
                physicalLocation: {
                    uri: this.getUri(item.filename),
                    region: {
                        startLine: item.line_number,
                        startColumn: item.column_number
                    } 
                },
            }
            codeFlow.locations.push(loc);
        });
        return codeFlow
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
                }] : undefined
            });
        }
        return stringUri;
    }
}