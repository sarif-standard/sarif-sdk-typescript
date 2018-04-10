# Installation

You need Node.js and npm installed. You also need the Typescript compiler (tsc). If they are not:
```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g typescript
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

# Troubleshooting

If you get errors when installing typescript, try:
```
npm config set strict-ssl false
```