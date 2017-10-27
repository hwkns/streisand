'use strict';

var del = require('del');
var gulp = require('gulp');
var gutil = require('gutil');
var webpack = require('webpack');
var connect = require('gulp-connect');
var WebpackDevServer = require('webpack-dev-server');

gulp.task('hot-load', function (callback) {
    var webpackConfig = require('./webpack.config.js');
    var config = Object.create(webpackConfig);
    new WebpackDevServer(webpack(config), {
        publicPath: config.output.publicPath,
        hot: true,
        historyApiFallback: true,
        quiet: false,
        noInfo: false,
        stats: 'minimal'
    }).listen(3000, 'localhost', function (err) {
        if (err) throw new gutil.PluginError('webpack-dev-server', err);
        gutil.log('[webpack-dev-server]', 'http://localhost:3000/webpack-dev-server/index.html');
    });
});

gulp.task('connect', function () {
    connect.server({ port: 4000 });
});

gulp.task('clean:modules', function () {
    return del(['node_modules']);
});

gulp.task('clean:dist', function () {
    return del(['dist']);
});

gulp.task('build', ['clean:dist'], function (callback) {
    var webpackConfig = require('./webpack.config.production.js');
    var config = Object.create(webpackConfig);
    webpack(config, function (error, stats) {
        if (error) {
            console.log(error);
            return callback(error);
        }
        var jsonStats = stats.toJson();
        if (jsonStats.errors.length > 0) {
            console.log(jsonStats.errors);
            return callback('There were build errors');
        }
        if (jsonStats.warnings.length > 0) {
            console.log('There were', jsonStats.warnings.length, 'warning(s)...');
        }
        console.log('Successfully built project');
        callback();
    });
})

gulp.task('dev', ['hot-load']);
gulp.task('default', ['build']);