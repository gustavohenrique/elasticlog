;(function (angular) {
    'use strict';

    angular
        .module('services.Log', [])
        .service('logService', LogService);

    LogService.$inject = ['$http', '$q', 'Constants'];

    function LogService ($http, $q, Constants) {

        this.findAll = findAll;
        this.getIndexName = getIndexName;

        function findAll (perPage, page, paginationData) {
            var params = paginationData || {};
            var url = Constants.baseUrl + getIndexName() + '?1=1';
            if (params.sortField) {
                url += '&sort=' + params.sortField;
            }
            if (params.groupBy) {
                url += '&group_by=' + params.groupBy;
            }
            if (page > 0) {
                url += '&page=' + page;
            }
            if (perPage > 0) {
                url += '&per_page=' + perPage;
            }
            return $http.get(url);
        }

        function getIndexName () {
            try {
                return localStorage.getItem('elasticlog_index');
            }
            catch (e) {
                return '';
            }
        }

    }

})(angular);
