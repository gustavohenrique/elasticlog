;(function (angular) {
    'use strict';

    angular
        .module('controllers.Log', [])
        .controller('LogCtrl', LogCtrl);

    LogCtrl.$inject = [
        '$location', '$routeParams', 'logService'];

    function LogCtrl ($location, $routeParams, logService) {
        var vm = this;
        vm.indexName = logService.getIndexName();
        vm.paginationData = {
            perPage: 10,
            currentPage: 1,
            sortField: '-created_at'
        };
        vm.paginate = paginate; // called by directives
        vm.sort = sort;
        vm.groupBy = groupBy;
        vm.clearFilter = clearFilter;
        vm.hasLogs = hasLogs;

        paginate(vm.paginationData.currentPage);

        function paginate (pageNumber, perPage) {
            var paginationData = vm.paginationData || {};
            if (! perPage) {
                perPage = paginationData.perPage;
            }
            logService.findAll(perPage, pageNumber, paginationData)
            .success(function (res) {
                paginationData.items = res.items;
                paginationData.total = res.total;
                paginationData.totalPages = Math.ceil(paginationData.total / paginationData.perPage);
            })
            .error(function (res) {
                console.log('Error getting the index items', res);
            });
        }

        function groupBy (level) {
            vm.paginationData.groupBy = level;
            paginate(vm.paginationData.currentPage);
        }

        function clearFilter () {
            vm.paginationData.groupBy = null;
            paginate(vm.paginationData.currentPage);
        }

        function sort () {
            if (vm.paginationData.sortField[0] === '-') {
                vm.paginationData.sortField = vm.paginationData.sortField.replace('-', '');
            }
            else {
                vm.paginationData.sortField = '-' + vm.paginationData.sortField;
            }
            paginate(vm.paginationData.currentPage);
        }

        function hasLogs () {
            if (vm.paginationData.items && vm.paginationData.items.length > 0) {
                return true;
            }
            return false;
        }

    }

})(angular);
