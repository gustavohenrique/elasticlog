;(function (angular) {
    'use strict';

    angular
        .module('controllers.Home', [])
        .controller('HomeCtrl', HomeCtrl);

    HomeCtrl.$inject = ['$location'];

    function HomeCtrl ($location) {
        var vm = this;
        vm.indexName = '';
        vm.setIndexAndRedirect = setIndexAndRedirect;

        function setIndexAndRedirect () {
            localStorage.setItem('elasticlog_index', vm.indexName);
            $location.path('/logs');
        }

    }

})(angular);
