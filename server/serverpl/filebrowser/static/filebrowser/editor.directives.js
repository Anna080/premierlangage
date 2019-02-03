'use strict';
angular.module('editor')
.directive('draggable', function() {
  return function(scope, element) {
    // this gives us the native JS object
    const el = element[0];
    
    el.draggable = true;
    
    el.addEventListener(
      'dragstart',
      function(e) {
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('Text', this.id);
        this.classList.add('drag');
        return false;
      },
      false
    );
    
    el.addEventListener(
      'dragend',
      function(e) {
        this.classList.remove('drag');
        return false;
      },
      false
    );
  }
})
.directive('droppable', function() {
  return {
    scope: {
      drop: '&'
    },
    link: function(scope, element) {
      // again we need the native object
      const el = element[0];
      
      el.addEventListener(
        'dragover',
        function(e) {
          e.dataTransfer.dropEffect = 'move';
          // allows us to drop
          if (e.preventDefault) e.preventDefault();
          this.classList.add('over');
          return false;
        },
        false
      );
      
      el.addEventListener(
        'dragenter',
        function(e) {
          this.classList.add('over');
          return false;
        },
        false
      );
      
      el.addEventListener(
        'dragleave',
        function(e) {
          this.classList.remove('over');
          return false;
        },
        false
      );
      
      el.addEventListener(
        'drop',
        function(e) {
          e.preventDefault();
          let file;

          if (e.dataTransfer.items) {
            for (let item of e.dataTransfer.items) {
              if (item.kind === 'file') {
                  file = item.getAsFile();
              }
            }
          } else if (e.dataTransfer.files.length > 0) {
            file = e.dataTransfer.files[0];
          }
          // Stops some browsers from redirecting.
          if (e.stopPropagation) e.stopPropagation();
          
          this.classList.remove('over');
         
          const binId = this.id;
          const data = e.dataTransfer.getData('Text');
          if (data || file) {
            // this.appendChild(item);
            // call the passed drop function
            scope.$apply(function(scope) {
              const fn = scope.drop();
              if ('undefined' !== typeof fn) {  
                if (file) {
                  fn(file, binId)
                } else {
                  const node = document.getElementById(data);
                  if (node) {
                    fn(node.id, binId);
                  }
                }         
              }
            });
          }
          return false;
        },
        false
      );
    }
  }
})
.directive('autoFocus', function($timeout) {
  return {
      link: function (scope, element, attrs) {
          attrs.$observe("autoFocus", function(newValue){
              if (newValue === "true")
                  $timeout(function(){element.focus()});
          });
      }
  };
});