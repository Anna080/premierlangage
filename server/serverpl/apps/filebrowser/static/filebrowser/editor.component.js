angular.module('editor')
.component('editor', {
    templateUrl: '/static/filebrowser/editor.component.html',
    controller: EditorComponent,
    controllerAs: 'editor'
});

function EditorComponent($scope, EditorService, MonacoService) {        
    const editor = this;
    editor.searchQuery = '';
    editor.searchResult = [];
    editor.searching = false;
    const consoleNode = angular.element('#console');

    EditorService.onLogAdded = function() {
        const height = consoleNode.height();
        if (height < 300) {
            consoleNode.height(400);
        }
       // $scope.$apply();
    }

    editor.logs = function() {
        return EditorService.logs;
    }

    editor.addFile = function() {
        EditorService.addFile(EditorService.resources[0]);
    }

    editor.addFolder = function() {
        EditorService.addFolder(EditorService.resources[0]);
    }

    editor.resources = function() {
        return EditorService.resources;
    };
   
    editor.inRepository = function() {
        return editor.selection() && editor.selection().repo;
    }
    
    editor.clearConsole = function() {
        EditorService.clearLogs();
    }

    editor.search = function() {
        editor.searching = true;
    }
   
    editor.selection = function() {
        return MonacoService.selection;
    }

    editor.repository = function() {
        return MonacoService.selection.repo;
    }

    editor.runningTask = function() {
        return EditorService.runningTask;
    }

    editor.showGitContextMenu = function(menu, event) {
        event.preventDefault();
        menu.open();
    }

    editor.updateSearch = function(event) {
        if (event.keyCode ===  27) { // esc
            editor.searching = false;
            editor.searchResult = [];
        } else if (event.keyCode === 13) { // enter
            editor.searchQuery = editor.searchQuery.toLowerCase();
            editor.searchResult = EditorService.findResources(resource => {
                return resource.type === 'file' && resource.name.toLowerCase().includes(editor.searchQuery);
            });
        }
    }

    window.onbeforeunload = function(e) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    };

    EditorService.loadResources();
    
    EditorService.setResizable('#explorer', function(node, e, startX, startY, startWidth, startHeight) {
        node.style.width = (startWidth + e.clientX - startX) + 'px';
        MonacoService.layout();
    });

    EditorService.setResizable('#console', function(node, e, startX, startY, startWidth, startHeight) {
        node.style.height = (startHeight - e.clientY + startY) + 'px';
        MonacoService.layout();
    });
}
