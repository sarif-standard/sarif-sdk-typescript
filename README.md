

# Installation

You need Node.js and npm installed. You also need the Typescript compiler (tsc). If they are not:
```
sudo apt-get install nodejs npm
sudo npm install typescript
```

Then, in the directory where you have cloned the repo:
```
npm install
tsc -p tsconfig.json
```

# Running the converters

```
node out/main.js --help
```