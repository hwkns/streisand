# Introduction
The web front-end code for JumpCut.

The site is built with [webpack](https://webpack.github.io/). We are using [Typescript](https://www.typescriptlang.org/) to make collaboration and maintenance easier. The UI is built on top of the [React](https://facebook.github.io/react/) framework using [Redux](http://redux.js.org/) as our state container.

# Getting Started
This project uses npm as its package/dependency manager. So after cloning the project, you will want to install the current version of [node](https://nodejs.org/) (which includes npm). Once you have it installed you can run `npm install` in the project's root directory to install the project's dependencies.

## Building
We are using [gulp](http://gulpjs.com/) as our task toolkit and since it is one of our npm dependencies, it should already be available.

### Development
By default, the code is setup for developing. The project adds several helpful debugging tools including a development server that supports module hot loading. If you run `gulp dev` it will do an initial development build and startup up the web server. You can then navigate to `http://localhost:3000` and see the website. You will then be able to make changes to the code and the server will run incremental builds and update the site (usually) without you having to refresh the page.

### Production
In order to get the production ready files, all you need to do is run the default gulp command: `gulp`. This will remove any remnants of a previous build and then build the project without any of the development tools. It will then compress and uglify everything into a handful of files. All built files will be dumped in the '/dist' directory. If you want to see the result of the build, you can start a simple webserver by running `gulp connect` and navigating to `http://localhost:4000`. You will want to make sure you do not already have a development server running because they will fight for resources.

## Proxies
None of the APIs that this site is using are setup to work with localhost requests. Until they support CORS you will need to route all API traffic through a proxy. There is a proxy.js file in the root of the project for doing this.
- Run `node .\proxy.js "http://dev.ronzertnert.xyz:8000"` to start the proxy server for the site api.

## Deployment
For now the easiest way to deploy this project on the dev server is to clone it there and build it. Then point nginx to the index.html file.
Long term it would better to have a deploy command/script to dump all the necessary files into a /drop folder so that the whole project isn't needed on the server.