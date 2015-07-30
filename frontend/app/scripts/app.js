;(function (angular) {
    'use strict';

    var app = angular.module('MainApp', [
        'MainRouter',
        'angular-loading-bar',

        'controllers.Menu',
        'controllers.Log',
        'controllers.Home',

        'services.Log',

        'directives.Pagination',
        'directives.showIf'
    ]);

    app.constant('Constants', {
        baseUrl: 'http://192.168.59.103/v1/logs/'
    });

    app.config(['$httpProvider', 'cfpLoadingBarProvider', function($httpProvider, cfpLoadingBarProvider) {
        cfpLoadingBarProvider.includeSpinner = false;
        $httpProvider.defaults.headers.common = {};
        $httpProvider.defaults.headers.post = {};
        $httpProvider.defaults.headers.put = {};
        $httpProvider.defaults.headers.patch = {};
    }]);

})(angular);
