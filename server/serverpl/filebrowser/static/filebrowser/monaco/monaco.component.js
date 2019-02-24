'use strict';

angular.module('editor').component('monaco', {
    templateUrl: '/static/filebrowser/monaco/monaco.component.html',
    controllerAs: 'monaco',
    controller: MonacoComponent
});

function MonacoComponent ($scope, EditorService, MonacoService) {
    const monaco = this;

    monaco.previewNode = angular.element(".monaco__preview");
    
    /** 
     * Hanldes resource close button click by asking confirmation and closes the resource if confirmed.
     * @param {Object} resource - the resource to close.
     * @param {Object} e - the javascript event object of the click.
    */
    monaco.didTapCloseResource = function(resource, e) {
        if (resource.changed) {
            EditorService.askConfirm({
                title: 'You will lose any unsaved changes, press Ctrl | Cmd + S to save !',
                targetEvent: e,
                confirmed: () => MonacoService.closeResource(resource)
            });
        } else {
            MonacoService.closeResource(resource);
        }
    }

    /**
     * Handles click on resource inside the editor by displaying the content of the resource.
     * @param {Object} resource - the resource to open.
     */
    monaco.didTapOpenResource = function(resource) {
        const current = monaco.selection();
        current.previewModeWidth = monaco.previewNode.width();
        MonacoService.openResource(resource).then(() => {
            if (resource.previewModeWidth) {
                monaco.previewNode.width(resource.previewModeWidth);
            } 
        });
    }
    /** Handles hide preview button click */
    monaco.didTapHidePreview = function() {
        monaco.selection().preview = undefined;
        monaco.previewNode.width(10);
    }

    /** Handles open preview button click */
    monaco.didTapOpenPreview = function() {
        MonacoService.preview().then(() => {
            monaco.previewNode.css({ width: '50%' });
        });
    }
    /** Handles show diff button click */
    monaco.didTapShowDiffEditor = function() {
        EditorService.showDiff(monaco.selection()).then(MonacoService.showDiffEditor);
    }

    /** Handles close diff button click */
    monaco.didTapCloseDiffEditor = function() {
        MonacoService.closeDiffEditor();
    }

    monaco.diffMode = function() {
        return monaco.selection() && monaco.selection().diffMode;
    }

    monaco.diffEditorEnabled = function() {
        const s = monaco.selection()
        return s && s.type === 'file' && !s.diffMode;
    }
    /** 
     * Gets a value indicating whether the selected resource can be previewed 
     * @returns {boolean} true if there is a selected resource and it can be previewed false otherwise 
     * */
    monaco.hasPreview = function() {
        return MonacoService.hasPreview();
    }

    /** 
     * Gets a value indicating whether there is any opened resource 
     * @returns {boolean} false if there is any opened resource true otherwise
    */
    monaco.isEmpty = function() {
        return MonacoService.isEmpty();
    }

    /** 
     * Gets a value indicating whether the given resource is the selected one 
     * @param {Object} resource - the resource to test.
     * @returns {boolean} true if the resource is the selected one false otherwise
     * */
    monaco.isSelection = function(resource) {
        return MonacoService.isSelection(resource);
    };

    /** 
     * Gets the html string representing the preview of the selected resource 
     * @returns {string} the preview value of the selected resource or undefined
     * */
    monaco.previewHtml = function() {
        if (monaco.selection()) {
            return monaco.selection().preview;
        }
        return undefined;
    } 
    
    /** 
     * Gets the list of the opened resources
     * @returns {Object[]} an array of resources.
     *  */
    monaco.resources = function() {
        return MonacoService.resources;
    }

    /** Gets a value indicating whether a long task is running */
    monaco.runningTask = function() {
        return MonacoService.runningTask;
    }

    /** Refreshs the component everytime a resource is opened|closed|changed... */
    MonacoService.resourcesChanged = function() {
        $scope.$apply();
    };
    
    /** 
     * Gets the selected resource inside the editor 
     * @returns {Object} The selected resource if it exists undefined otherwise.
     * */
    monaco.selection = function() {
        return MonacoService.selection;
    }
  
    MonacoService.loadEditor();

    EditorService.setResizable('.monaco__preview', function(node, e, startX, startY, startWidth, startHeight) {
        node.style.width = (startWidth + startX - e.clientX) + 'px';
        MonacoService.layout();
    });
}