'use strict';

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    clean: ["js/libs.js", "bower_components/", "ghostdriver.log"],
    bower: {
        install: { }
      },
    bower_concat: {
        all: {
            dest: 'js/libs.js',
            cssDest: 'css/libs.css',
            dependencies: {
              'bacon': 'jquery',
            }
          }
        },
    jasmine: {
        yourTask: {
          src:[ 'js/*.js' ],
          options: {
            specs: 'js_tests/*Spec.js',
          }
        }
      }
  });

  grunt.loadNpmTasks('grunt-contrib-jasmine');
  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-bower-concat');
  grunt.loadNpmTasks('grunt-contrib-clean');

  // Default task(s).
  grunt.registerTask('default', 
    ['clean', 'bower:install', 'bower_concat', 'jasmine']);

}
