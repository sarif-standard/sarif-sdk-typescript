import * as yargs from "yargs";
import InferConverter from "./InferConverter";
import CSAPlistConverter from "./CSAPlistConverter";
import Converter from "./Converter";
import * as infer from "./types/infer";
import * as fs from "fs";

class Startup {
    public static main(): number {
        let argv = yargs
        .usage('Usage: $0 <input file to convert> -f <plist|infer> [options]')
        .option('f', {required: true})
        .alias('f', 'format')
        .option('projectPath', {required: true})
        .nargs('o', 1)
        .describe('o', 'name of the SARIF output file')
        .boolean('noMd5')
        .describe('noMd5', 'use this flag to skip md5 computation of the source files')
        .help('h')
        .alias('h', 'help')
        .demandCommand(1)
        .argv;

        let data = fs.readFileSync(argv._[0]).toString();
        let projectpath = argv.projectPath;
        if (!projectpath) {
            projectpath = "./";
        }
        var converter: Converter;
        if (argv.f == 'plist') {
            converter = new CSAPlistConverter(data, projectpath, !argv.noMd5);
        }
        else if (argv.f == 'infer') {
            converter = new InferConverter(data, projectpath, !argv.noMd5);
        }
        else {
            console.error('no converter for format ' + argv.f + '. Please use plist or infer');
            return 1;
        }
        let outputFileName = argv.o;
        converter.convert(outputFileName);
        return 0;
    }
}

Startup.main();